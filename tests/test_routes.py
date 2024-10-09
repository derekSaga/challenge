from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_access_user_route_with_valid_token():
    # Fazer login como 'user' e obter o token JWT
    login_response = client.post("/token", json={"username": "user", "password": "L0XuwPOdS5U"})
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Acessar a rota protegida '/user'
    response = client.get("/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, user! This is user data."}


def test_access_admin_route_with_valid_token():
    # Fazer login como 'admin' e obter o token JWT
    login_response = client.post("/token", json={"username": "admin", "password": "JKSipm0YH"})
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Acessar a rota protegida '/admin'
    response = client.get("/admin", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, admin! This is admin data."}


def test_access_user_route_without_token():
    # Tentar acessar a rota '/user' sem fornecer o token JWT
    response = client.get("/user")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_access_admin_route_without_token():
    # Tentar acessar a rota '/admin' sem fornecer o token JWT
    response = client.get("/admin")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_access_admin_route_as_user():
    # Fazer login como 'user' e obter o token JWT
    login_response = client.post("/token", json={"username": "user", "password": "L0XuwPOdS5U"})
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Tentar acessar a rota '/admin' com o token de um usuário comum
    response = client.get("/admin", headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}
