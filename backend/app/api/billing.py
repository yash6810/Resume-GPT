import os
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Header, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db, User
from app.api.auth import get_current_user

router = APIRouter(prefix="/billing", tags=["Billing & Subscriptions"])
logger = logging.getLogger(__name__)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_PRO_MONTHLY = os.getenv("STRIPE_PRICE_PRO_MONTHLY", "price_pro_monthly_999")
STRIPE_PRICE_ENTERPRISE = os.getenv("STRIPE_PRICE_ENTERPRISE", "price_enterprise_2999")


class CheckoutRequest(BaseModel):
    plan: str = "pro"  # pro, enterprise
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str
    mode: str  # "live" or "simulation"


class SubscriptionStatusResponse(BaseModel):
    plan: str
    status: str
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None


@router.post("/create-checkout-session", response_model=CheckoutResponse)
async def create_checkout_session(
    payload: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a Stripe checkout session for subscription upgrade."""
    plan_tier = payload.plan.lower()
    if plan_tier not in ["pro", "enterprise"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid plan '{payload.plan}'. Choose 'pro' or 'enterprise'.",
        )

    # If Stripe API key is configured, create a real Stripe Checkout Session
    if STRIPE_SECRET_KEY and not STRIPE_SECRET_KEY.startswith("sk_test_mock"):
        try:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY

            price_id = (
                STRIPE_PRICE_PRO_MONTHLY
                if plan_tier == "pro"
                else STRIPE_PRICE_ENTERPRISE
            )
            success_url = payload.success_url or "http://localhost:8000/?billing=success"
            cancel_url = payload.cancel_url or "http://localhost:8000/?billing=cancelled"

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{"price": price_id, "quantity": 1}],
                mode="subscription",
                customer_email=current_user.email,
                client_reference_id=str(current_user.id),
                metadata={"plan": plan_tier, "user_id": str(current_user.id)},
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return CheckoutResponse(
                checkout_url=session.url,
                session_id=session.id,
                mode="live",
            )
        except Exception as e:
            logger.error(f"Stripe error creating checkout session: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Payment gateway error: {str(e)}",
            )

    # In development/test mode without live keys, generate a valid simulated checkout session
    mock_session_id = f"cs_test_mock_{current_user.id}_{plan_tier}"
    mock_url = f"https://checkout.stripe.com/pay/{mock_session_id}"
    return CheckoutResponse(
        checkout_url=mock_url,
        session_id=mock_session_id,
        mode="simulation",
    )


@router.post("/customer-portal")
async def create_customer_portal(
    current_user: User = Depends(get_current_user),
):
    """Generate a link to the Stripe Customer Portal for billing management."""
    if not current_user.stripe_customer_id:
        # Return fallback manage URL
        return {"portal_url": "http://localhost:8000/#modal-pricing", "mode": "simulation"}

    if STRIPE_SECRET_KEY and not STRIPE_SECRET_KEY.startswith("sk_test_mock"):
        try:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY
            portal = stripe.billing_portal.Session.create(
                customer=current_user.stripe_customer_id,
                return_url="http://localhost:8000/",
            )
            return {"portal_url": portal.url, "mode": "live"}
        except Exception as e:
            logger.error(f"Stripe portal error: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Portal generation error: {str(e)}",
            )

    return {"portal_url": "https://billing.stripe.com/p/session/test_portal", "mode": "simulation"}


@router.get("/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
):
    """Get the current subscription tier and billing status of the authenticated user."""
    return SubscriptionStatusResponse(
        plan=current_user.plan,
        status=current_user.subscription_status,
        stripe_customer_id=current_user.stripe_customer_id,
        stripe_subscription_id=current_user.stripe_subscription_id,
    )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="stripe-signature"),
    db: Session = Depends(get_db),
):
    """Handle incoming Stripe webhook events."""
    payload_bytes = await request.body()

    event = None
    if STRIPE_WEBHOOK_SECRET and STRIPE_SECRET_KEY:
        try:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY
            event = stripe.Webhook.construct_event(
                payload_bytes, stripe_signature, STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:
            logger.error(f"Stripe webhook signature verification failed: {e}")
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        # Development / test webhook processing without signature requirement
        import json
        try:
            event = json.loads(payload_bytes.decode("utf-8"))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")

    event_type = event.get("type", "") if isinstance(event, dict) else getattr(event, "type", "")
    event_data = event.get("data", {}).get("object", {}) if isinstance(event, dict) else getattr(getattr(event, "data", None), "object", {})

    logger.info(f"Processing Stripe webhook event: {event_type}")

    if event_type == "checkout.session.completed":
        user_id = event_data.get("client_reference_id") or event_data.get("metadata", {}).get("user_id")
        plan = event_data.get("metadata", {}).get("plan", "pro")
        customer_id = event_data.get("customer")
        sub_id = event_data.get("subscription")

        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.plan = plan
                user.stripe_customer_id = customer_id
                user.stripe_subscription_id = sub_id
                user.subscription_status = "active"
                db.commit()
                logger.info(f"User {user.id} upgraded to {plan}")

    elif event_type in ["customer.subscription.deleted", "customer.subscription.cancelled"]:
        sub_id = event_data.get("id")
        if sub_id:
            user = db.query(User).filter(User.stripe_subscription_id == sub_id).first()
            if user:
                user.plan = "free"
                user.subscription_status = "cancelled"
                db.commit()
                logger.info(f"User {user.id} downgraded to free")

    return {"status": "success", "event": event_type}
