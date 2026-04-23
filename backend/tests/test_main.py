import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "cover_letter_generate" in data["endpoints"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


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
