from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Float,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - supports both SQLite and PostgreSQL
# Set DATABASE_URL in .env to switch between them
# SQLite: DATABASE_URL=sqlite:///./resumegpt.db
# PostgreSQL: DATABASE_URL=postgresql://user:password@localhost:5432/resumegpt


def get_database_url():
    """Get database URL from environment or default to SQLite."""
    return os.getenv("DATABASE_URL", "sqlite:///./resumegpt.db")


DATABASE_URL = get_database_url()

# Configure engine based on database type
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )
else:
    # SQLite configuration (default)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    resume_history = relationship(
        "ResumeHistory", back_populates="user", cascade="all, delete-orphan"
    )


class ResumeHistory(Base):
    __tablename__ = "resume_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_name = Column(String, nullable=False)
    job_description = Column(Text, nullable=True)
    ats_score = Column(Float, nullable=True)
    matched_skills = Column(JSON, nullable=True)  # List of matched skills
    missing_skills = Column(JSON, nullable=True)  # List of missing skills
    recommendations = Column(JSON, nullable=True)  # List of recommendations
    resume_text = Column(Text, nullable=True)  # Full resume text
    analysis_data = Column(JSON, nullable=True)  # Full analysis results
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resume_history")


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    position_title = Column(String, nullable=False)
    job_description = Column(Text, nullable=True)
    job_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    salary_range = Column(String, nullable=True)
    status = Column(
        String, default="applied"
    )  # applied, screening, interview, offer, rejected, accepted
    ats_score = Column(Float, nullable=True)
    resume_used = Column(String, nullable=True)  # Name of resume used
    notes = Column(Text, nullable=True)
    applied_date = Column(DateTime, default=datetime.utcnow)
    follow_up_date = Column(DateTime, nullable=True)
    interview_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="job_applications")


# Update User model to include job_applications relationship
User.job_applications = relationship(
    "JobApplication", back_populates="user", cascade="all, delete-orphan"
)


class ABTest(Base):
    __tablename__ = "ab_tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_description = Column(Text, nullable=True)
    resume_a = Column(Text, nullable=False)
    resume_b = Column(Text, nullable=False)
    score_a = Column(Float, nullable=False)
    score_b = Column(Float, nullable=False)
    winner = Column(String, nullable=True)  # a, b, none
    platform = Column(
        String, default="generic"
    )  # linkedin, indeed, greenhouse, generic
    outcome = Column(String, default="pending")  # pending, callback, no_callback
    outcome_notes = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    outcome_recorded_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="ab_tests")


# Update User model to include ab_tests relationship
User.ab_tests = relationship(
    "ABTest", back_populates="user", cascade="all, delete-orphan"
)


# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
