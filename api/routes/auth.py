"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import FullTokenResponse, LoginRequest, MessageResponse, RefreshRequest, RegisterRequest
from security.auth import create_access_token, create_refresh_token, decode_token
from security.deps import current_user
from storage.tenant_store import TenantStore
from storage.token_store import TokenStore
from storage.user_store import UserStore

router = APIRouter(prefix="/auth", tags=["auth"])


def build_tokens(user) -> FullTokenResponse:
    access, _, _ = create_access_token(user.user_id, user.tenant_id, user.role)
    refresh, _, _ = create_refresh_token(user.user_id, user.tenant_id, user.role)
    return FullTokenResponse(access_token=access, refresh_token=refresh, expires_in=1800)


@router.post("/register", response_model=FullTokenResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> FullTokenResponse:
    store = UserStore(db)
    if await store.get_by_email(payload.email):
        raise HTTPException(status_code=409, detail="email already registered")
    await TenantStore(db).get_or_create(payload.tenant_id)
    user = await store.create(payload.email, payload.password, payload.tenant_id, payload.role)
    return build_tokens(user)


@router.post("/login", response_model=FullTokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> FullTokenResponse:
    user = await UserStore(db).authenticate(payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return build_tokens(user)


@router.post("/refresh", response_model=FullTokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> FullTokenResponse:
    data = decode_token(payload.refresh_token)
    if data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="refresh token required")
    if await TokenStore(db).is_revoked(str(data.get("jti"))):
        raise HTTPException(status_code=401, detail="token revoked")
    user = await UserStore(db).get_by_user_id(str(data.get("sub")))
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")
    return build_tokens(user)


@router.get("/me")
async def me(user=Depends(current_user)) -> dict:
    return {"user_id": user.user_id, "email": user.email, "tenant_id": user.tenant_id, "role": user.role}


@router.post("/logout", response_model=MessageResponse)
async def logout(payload: RefreshRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> MessageResponse:
    data = decode_token(payload.refresh_token)
    await TokenStore(db).revoke(str(data.get("jti")), user.tenant_id)
    return MessageResponse(message="logged out")
