import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, User
from app.api.auth import create_access_token

client = TestClient(app)


@pytest.fixture
def test_user_token():
    db = SessionLocal()
    user = db.query(User).filter(User.username == "billing_test_user").first()
    if not user:
        user = User(
            email="billing_test@example.com",
            username="billing_test_user",
            hashed_password="hashed_dummy_password",
            full_name="Billing Tester",
            plan="free",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": user.username})
    db.close()
    return token, user.id


def test_billing_status(test_user_token):
    token, _ = test_user_token
    response = client.get(
        "/billing/status",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "plan" in data
    assert "status" in data


def test_create_checkout_session(test_user_token):
    token, user_id = test_user_token
    response = client.post(
        "/billing/create-checkout-session",
        headers={"Authorization": f"Bearer {token}"},
        json={"plan": "pro"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "checkout_url" in data
    assert "session_id" in data
    assert data["mode"] in ["live", "simulation"]


def test_create_checkout_invalid_plan(test_user_token):
    token, _ = test_user_token
    response = client.post(
        "/billing/create-checkout-session",
        headers={"Authorization": f"Bearer {token}"},
        json={"plan": "ultra_invalid"},
    )
    assert response.status_code == 400


def test_customer_portal(test_user_token):
    token, _ = test_user_token
    response = client.post(
        "/billing/customer-portal",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "portal_url" in data


def test_stripe_webhook_upgrade(test_user_token):
    _, user_id = test_user_token
    webhook_payload = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "client_reference_id": str(user_id),
                "customer": "cus_test_mock_123",
                "subscription": "sub_test_mock_123",
                "metadata": {"plan": "pro", "user_id": str(user_id)},
            }
        },
    }
    response = client.post(
        "/billing/webhook",
        json=webhook_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

    # Verify user plan updated in DB
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    assert user.plan == "pro"
    assert user.stripe_customer_id == "cus_test_mock_123"
    db.close()


def test_stripe_webhook_cancellation(test_user_token):
    _, user_id = test_user_token
    webhook_payload = {
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "id": "sub_test_mock_123",
            }
        },
    }
    response = client.post(
        "/billing/webhook",
        json=webhook_payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

    # Verify user plan downgraded in DB
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    assert user.plan == "free"
    assert user.subscription_status == "cancelled"
    db.close()
