from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_register_login_and_creation_flow():
    with TestClient(app) as client:
        email = f"flow-{uuid4().hex[:8]}@example.com"
        password = "StrongPassword123!"

        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
                "invite_code": "DEMO-ACCESS",
            },
        )
        assert register_response.status_code == 200
        assert register_response.json()["access_state"] == "approved"

        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert login_response.status_code == 200
        login_payload = login_response.json()
        assert login_payload["access_state"] == "approved"
        assert login_payload["access_token"]

        headers = {"Authorization": f"Bearer {login_payload['access_token']}"}
        create_response = client.post(
            "/api/v1/creation/sessions",
            json={"grammar_text": "〜にちがいない", "description": "test flow"},
            headers=headers,
        )
        assert create_response.status_code == 200
        session_payload = create_response.json()
        assert session_payload["id"].startswith("ses_")

        follow_response = client.post(
            f"/api/v1/creation/sessions/{session_payload['id']}/follow-up",
            json={"question": "add more examples"},
            headers=headers,
        )
        assert follow_response.status_code == 200
        assert follow_response.json()["follow_up_history"] == ["add more examples"]

        complete_response = client.post(
            f"/api/v1/creation/sessions/{session_payload['id']}/complete",
            headers=headers,
        )
        assert complete_response.status_code == 200
        grammar_id = complete_response.json()["card_id"]

        recent_response = client.post(
            f"/api/v1/user/recent-views/{grammar_id}",
            headers=headers,
        )
        assert recent_response.status_code == 204

        favorite_response = client.post(
            f"/api/v1/user/favorites/{grammar_id}",
            headers=headers,
        )
        assert favorite_response.status_code == 200
        assert favorite_response.json()["is_favorite"] is True

        my_grammar_response = client.get("/api/v1/user/my-grammar", headers=headers)
        assert my_grammar_response.status_code == 200
        assert any(item["id"] == grammar_id for item in my_grammar_response.json()["items"])
