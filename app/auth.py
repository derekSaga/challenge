from datetime import UTC
from datetime import datetime
from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Configurações do JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, password):
    return plain_password == password


def authenticate_user(form_data):
    username = form_data.get("username")
    password = form_data.get("password")
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_data = {
        "sub": user["username"],
        "role": user["role"],
        "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"username": username, "role": role}


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    return current_user


async def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user
