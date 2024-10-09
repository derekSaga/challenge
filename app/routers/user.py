from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user

router = APIRouter()


@router.get("/user", tags=["user"])
async def read_user_data(current_user: dict = Depends(get_current_active_user)):
    return {"message": f"Hello, {current_user['username']}! This is user data."}
