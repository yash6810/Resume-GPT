import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    if "text/html" in response.headers.get("content-type", ""):
        assert "<!DOCTYPE html>" in response.text or "ResumeGPT" in response.text
    else:
        data = response.json()
        assert "message" in data or "version" in data


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ResumeGPT"


def test_parse_no_file():
    response = client.post("/parse")
    assert response.status_code == 422  # Validation error


def test_analyze_empty():
    response = client.post("/analyze", json={})
    assert response.status_code == 422  # Validation error


def test_rewrite_empty():
    response = client.post("/rewrite", json={})
    assert response.status_code == 422  # Validation error


def test_export_empty():
    response = client.post("/export", json={})
    assert response.status_code == 422  # Validation error


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User",
        },
    )
    assert response.status_code in [200, 400]  # 400 if user already exists


def test_login_invalid():
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/login", json={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_cover_letter_empty():
    """Test cover letter generation with empty data."""
    response = client.post("/cover-letter/generate", json={})
    assert response.status_code == 422


def test_cover_letter_generate():
    """Test cover letter generation."""
    response = client.post(
        "/cover-letter/generate",
        json={
            "resume_text": "Software Engineer with 5 years of Python experience",
            "job_description": "Looking for a Python developer",
            "company_name": "Tech Corp",
            "position": "Senior Developer",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "cover_letter" in data


def test_cover_letter_export_empty():
    """Test cover letter export with empty data."""
    response = client.post("/cover-letter/export", json={})
    assert response.status_code == 422


def test_pdf_export_empty():
    """Test PDF export with empty data."""
    response = client.post("/export/pdf", json={})
    assert response.status_code == 422


def test_pdf_export():
    """Test PDF export."""
    response = client.post(
        "/export/pdf",
        json={
            "resume_text": "John Doe\nSoftware Engineer\n\nExperience\n- Built web apps",
            "applied_changes": [],
        },
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_builder_templates():
    """Test builder templates endpoint."""
    response = client.get("/builder/templates")
    assert response.status_code == 200
    data = response.json()
    # Response might be {"templates": [...]} or just [...]
    templates = data.get("templates", data) if isinstance(data, dict) else data
    assert len(templates) == 7  # Should have 7 templates now
    template_ids = [t["id"] for t in templates]
    assert "executive" in template_ids
    assert "tech" in template_ids
    assert "academic" in template_ids


def test_auth_password_reset_and_gdpr_deletion():
    """Test forgot-password, reset-password, change-password, and GDPR user deletion."""
    import uuid
    uid = uuid.uuid4().hex[:6]
    username = f"user_{uid}"
    email = f"user_{uid}@example.com"
    initial_password = "initial_secret_123"

    # 1. Register User
    reg_res = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": initial_password,
            "full_name": "Test Lifecycle User",
        },
    )
    assert reg_res.status_code == 200

    # 2. Login User
    login_res = client.post(
        "/auth/login",
        json={"username": username, "password": initial_password},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Change Password
    new_pwd = "new_secret_456"
    change_res = client.post(
        "/auth/change-password",
        headers=headers,
        json={"old_password": initial_password, "new_password": new_pwd},
    )
    assert change_res.status_code == 200

    # 4. Forgot Password Flow
    forgot_res = client.post(
        "/auth/forgot-password",
        json={"email": email},
    )
    assert forgot_res.status_code == 200
    reset_token = forgot_res.json().get("reset_token")
    assert reset_token is not None

    # 5. Reset Password via Token
    reset_pwd = "reset_secret_789"
    reset_res = client.post(
        "/auth/reset-password",
        json={"token": reset_token, "new_password": reset_pwd},
    )
    assert reset_res.status_code == 200

    # 6. Verify Login with Reset Password
    rel_res = client.post(
        "/auth/login",
        json={"username": username, "password": reset_pwd},
    )
    assert rel_res.status_code == 200
    new_token = rel_res.json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}

    # 7. GDPR Delete Account
    del_res = client.delete("/auth/me", headers=new_headers)
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "deleted"

    # 8. Verify Account No Longer Exists
    fail_login = client.post(
        "/auth/login",
        json={"username": username, "password": reset_pwd},
    )
    assert fail_login.status_code == 401


def test_structured_logging_headers():
    """Verify that structured logging middleware sets tracing headers."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "x-request-id" in response.headers
    assert "x-response-time-ms" in response.headers


