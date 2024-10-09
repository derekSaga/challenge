from fastapi.testclient import TestClient

from app.auth import authenticate_user
from app.main import app
from app.auth import verify_password
from jose import jwt
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException

client = TestClient(app)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def test_invalid_credentials():
    # Tentativa de login com credenciais inválidas
    response = client.post("/token", data={"username": "invaliduser", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "Invalid credentials"}}


def test_token_creation():
    # Garantir que o token seja criado corretamente com credenciais válidas
    login_response = client.post("/token", data={"username": "user", "password": "L0XuwPOdS5U"})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Acessar a rota protegida '/user' para garantir que o token é válido
    response = client.get("/user", headers=headers)
    assert response.status_code == 200


def test_invalid_token_signature():
    # Criar um token com uma assinatura inválida
    invalid_token = jwt.encode(
        {"sub": "user", "role": "user", "exp": datetime.now(UTC) + timedelta(minutes=30)},
        "wrong-secret-key",
        algorithm=ALGORITHM,
    )
    headers = {"Authorization": f"Bearer {invalid_token}"}

    # Acessar a rota protegida com um token de assinatura inválida
    response = client.get("/user", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_get_current_active_user():
    # Verifica se o usuário ativo é retornado corretamente
    login_response = client.post("/token", data={"username": "user", "password": "L0XuwPOdS5U"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Verifique se o usuário ativo é retornado corretamente
    response = client.get("/user", headers=headers)
    assert response.status_code == 200


def test_get_admin_user_without_privileges():
    # Login como 'user' e obtenção do token JWT
    login_response = client.post("/token", data={"username": "user", "password": "L0XuwPOdS5U"})
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Tentar acessar uma rota de administrador sem permissões
    response = client.get("/admin", headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Admin privileges required"}


def test_authenticate_user_valid_credentials():
    # Cenário com credenciais corretas
    form_data = {"username": "user", "password": "L0XuwPOdS5U"}
    result = authenticate_user(form_data)

    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_authenticate_user_invalid_username():
    # Cenário onde o nome de usuário é inválido
    form_data = {"username": "invaliduser", "password": "L0XuwPOdS5U"}

    try:
        authenticate_user(form_data)
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Invalid credentials"


def test_authenticate_user_invalid_password():
    # Cenário onde a senha está incorreta
    form_data = {"username": "user", "password": "wrongpassword"}

    try:
        authenticate_user(form_data)
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Invalid credentials"
