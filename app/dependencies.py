from fastapi import Depends

from app.auth import get_current_user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    return current_user
