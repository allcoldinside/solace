from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import FullTokenResponse, LoginRequest, MessageResponse, RefreshRequest, RegisterRequest
from security.auth import create_access_token, create_refresh_token, decode_token
from security.deps import current_user
from security.passwords import hash_password, verify_password
from storage.token_store import TokenStore
from storage.user_store import UserStore
from storage.tenant_store import TenantStore

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', response_model=MessageResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    await TenantStore(db).ensure_default(payload.tenant_id)
    s = UserStore(db)
    if await s.get_by_email(payload.email):
        raise HTTPException(status_code=400, detail='email exists')
    await s.create(payload.email, hash_password(payload.password), payload.role, payload.tenant_id)
    return MessageResponse(message='registered')

@router.post('/login', response_model=FullTokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await UserStore(db).get_by_email(payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='bad credentials')
    return FullTokenResponse(access_token=create_access_token(user.email, user.tenant_id, user.role), refresh_token=create_refresh_token(user.email, user.tenant_id, user.role))

@router.post('/refresh', response_model=FullTokenResponse)
async def refresh(payload: RefreshRequest):
    claims = decode_token(payload.refresh_token)
    if claims.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail='invalid token')
    return FullTokenResponse(access_token=create_access_token(claims['sub'], claims['tenant_id'], claims['role']), refresh_token=create_refresh_token(claims['sub'], claims['tenant_id'], claims['role']))

@router.get('/me')
async def me(user=Depends(current_user)):
    return {'email': user.email, 'role': user.role, 'tenant_id': user.tenant_id}

@router.post('/logout', response_model=MessageResponse)
async def logout(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    claims = decode_token(payload.refresh_token)
    await TokenStore(db).revoke(claims['jti'], claims.get('tenant_id','default'))
    return MessageResponse(message='logged out')
