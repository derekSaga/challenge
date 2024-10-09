from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_access_user_route_with_valid_token():
    # Login como 'user' e obtenção do token JWT
    login_response = client.post("/token", data={"username": "user", "password": "L0XuwPOdS5U"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Acessando a rota protegida '/user'
    response = client.get("/user", headers=headers)
    assert response.status_code == 200


def test_access_admin_route_with_valid_token():
    # Login como 'admin' e obtenção do token JWT
    login_response = client.post("/token", data={"username": "admin", "password": "JKSipm0YH"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Acessando a rota protegida '/admin'
    response = client.get("/admin", headers=headers)
    assert response.status_code == 200


def test_access_admin_route_as_user():
    # Login como 'user' e obtenção do token JWT
    login_response = client.post("/token", data={"username": "user", "password": "L0XuwPOdS5U"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Tentativa de acessar a rota '/admin' com o token de 'user'
    response = client.get("/admin", headers=headers)
    assert response.status_code == 403
