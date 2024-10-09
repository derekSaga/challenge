from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login():
    response = client.post(
        "/token", data={"username": "user", "password": "L0XuwPOdS5U"}
    )  # Use 'data' instead of 'json'
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_login():
    response = client.post(
        "/token", data={"username": "user", "password": "wrongpassword"}
    )  # Use 'data' instead of 'json'
    assert response.status_code == 400


def test_access_user_route():
    login_response = client.post("/token", data={"username": "user", "password": "L0XuwPOdS5U"})  # Use 'data'
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/user", headers=headers)
    assert response.status_code == 200


def test_access_admin_route_as_user():
    login_response = client.post("/token", data={"username": "user", "password": "L0XuwPOdS5U"})  # Use 'data'
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/admin", headers=headers)
    assert response.status_code == 403
