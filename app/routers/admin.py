from fastapi import APIRouter, Depends
from app.auth import get_admin_user

router = APIRouter()


@router.get("/admin", tags=["admin"])
async def read_admin_data(current_user: dict = Depends(get_admin_user)):
    return {"message": f"Hello, {current_user['username']}! This is admin data."}
