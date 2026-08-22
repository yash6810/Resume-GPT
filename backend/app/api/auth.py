import os
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

from app.core.database import get_db, User
from app.models.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
)

router = APIRouter()

# Security configuration - use environment variable
INSECURE_FALLBACK_SECRET = "resumegpt-secret-key-change-in-production"


def get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET")
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "production":
        if not secret or secret == INSECURE_FALLBACK_SECRET or len(secret) < 32:
            raise RuntimeError(
                "FATAL SECURITY ERROR: JWT_SECRET environment variable is missing, using insecure default, "
                "or shorter than 32 characters in production mode. "
                "Generate a cryptographically secure key with: openssl rand -hex 32"
            )
        return secret
    if not secret:
        return INSECURE_FALLBACK_SECRET
    return secret


SECRET_KEY = get_jwt_secret()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing (using sha256_crypt for clean Python 3.13 compatibility)
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/auth/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/auth/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    # Find user by username
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/auth/me", response_model=UserResponse)
def update_user_profile(
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile"""
    if full_name:
        current_user.full_name = full_name
    if email:
        # Check if email already exists
        if (
            db.query(User)
            .filter(User.email == email, User.id != current_user.id)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        current_user.email = email

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/auth/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Initiate self-service password reset."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        # Prevent user enumeration by returning a uniform success message
        return {
            "status": "success",
            "message": "If that email is registered, a secure reset token has been generated.",
        }

    # Generate 15-minute password reset token
    reset_token = create_access_token(
        data={"sub": user.username, "purpose": "password_reset"},
        expires_delta=timedelta(minutes=15),
    )
    return {
        "status": "success",
        "message": "If that email is registered, a secure reset token has been generated.",
        "reset_token": reset_token,  # Included for client handling / automated email simulation
    }


@router.post("/auth/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using a valid reset token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired reset token",
    )
    try:
        token_payload = jwt.decode(payload.token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = token_payload.get("sub")
        purpose: str = token_payload.get("purpose")
        if username is None or purpose != "password_reset":
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    if len(payload.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 6 characters long",
        )

    user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    return {"status": "success", "message": "Password has been successfully updated"}


@router.post("/auth/change-password")
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change password for the authenticated user."""
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password",
        )
    if len(payload.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 6 characters long",
        )

    current_user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    return {"status": "success", "message": "Password changed successfully"}


@router.delete("/auth/me")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """GDPR Compliance: Permanently purge current user account and all associated resumes, applications, and logs."""
    user_id = current_user.id
    db.delete(current_user)
    db.commit()
    return {
        "status": "deleted",
        "user_id": user_id,
        "message": "Account and all associated resume data permanently purged.",
    }
