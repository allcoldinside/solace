"""Authentication routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register() -> dict:
    return {"message": "registration endpoint ready"}

@router.post("/login")
async def login() -> dict:
    return {"message": "login endpoint ready"}

@router.post("/refresh")
async def refresh() -> dict:
    return {"message": "refresh endpoint ready"}

@router.get("/me")
async def me() -> dict:
    return {"message": "me endpoint ready"}

@router.post("/logout")
async def logout() -> dict:
    return {"message": "logout endpoint ready"}
