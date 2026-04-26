from fastapi.testclient import TestClient

from app.infrastructure.config.settings import get_settings
from app.main import app


def test_seeded_admin_can_login_with_password():
    settings = get_settings()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": settings.admin_email,
                "password": settings.admin_password,
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["is_admin"] is True
    assert payload["access_state"] == "approved"
    assert payload["access_token"]
