from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_pending_review_user_can_login_but_cannot_create():
    with TestClient(app) as client:
        email = f"pending-{uuid4().hex[:8]}@example.com"
        password = "StrongPassword123!"

        register_response = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password},
        )
        assert register_response.status_code == 200
        assert register_response.json()["access_state"] == "pending_review"

        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert login_response.status_code == 200
        assert login_response.json()["access_state"] == "pending_review"

        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        create_response = client.post(
            "/api/v1/creation/sessions",
            json={"grammar_text": "〜ものの"},
            headers=headers,
        )
        assert create_response.status_code == 403
        assert create_response.json()["error"]["code"] == "approval_pending"
