from datetime import UTC
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI
from fastapi import HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response
from jose import jwt

from app.routers import admin, user

app = FastAPI()
app.include_router(user.router)
app.include_router(admin.router)

# Fake database of users for the example
fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(form_data: OAuth2PasswordRequestForm):
    user_in = fake_users_db.get(form_data.username)
    if user_in and user_in["password"] == form_data.password:
        return user_in
    return None


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Custom OpenAPI schema to prevent recursion error
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="This is a custom OpenAPI schema for JWT Bearer authentication",
        routes=app.routes,
    )
    # Adding JWT Bearer token support to OpenAPI
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Set custom OpenAPI schema
app.openapi = custom_openapi


# Endpoint to generate JWT token using username and password
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in = authenticate_user(form_data)
    if not user_in:
        raise HTTPException(status_code=400, detail={"error": "Invalid credentials"})

    # Create JWT token
    access_token = create_access_token(data={"sub": user_in["username"], "role": user_in["role"]})
    return {"access_token": access_token, "token_type": "bearer"}


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "OK", "timestamp": datetime.now(UTC)}
