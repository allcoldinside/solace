from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import FullTokenResponse, LoginRequest, MessageResponse, RefreshRequest, RegisterRequest
from security.auth import create_access_token, create_refresh_token, decode_token
from security.deps import current_user
from security.passwords import hash_password, verify_password
from security.audit import write_audit
from storage.token_store import TokenStore
from storage.user_store import UserStore
from storage.tenant_store import TenantStore
from storage.membership_store import MembershipStore

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', response_model=MessageResponse)
async def register(payload: RegisterRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await TenantStore(db).ensure_default(payload.tenant_id)
    s = UserStore(db)
    if await s.get_by_email(payload.email):
        raise HTTPException(status_code=400, detail='email exists')
    user = await s.create(payload.email, hash_password(payload.password), payload.role, payload.tenant_id)
    await MembershipStore(db).add(user.user_id, payload.tenant_id, payload.role)
    await write_audit(
        db,
        tenant_id=payload.tenant_id,
        actor_user_id=user.user_id,
        action='auth.register',
        resource_type='user',
        resource_id=user.user_id,
        metadata_json={'role': payload.role, 'email': payload.email},
        request=request,
    )
    return MessageResponse(message='registered')

@router.post('/login', response_model=FullTokenResponse)
async def login(payload: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    user = await UserStore(db).get_by_email(payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='bad credentials')
    await write_audit(
        db,
        tenant_id=user.tenant_id,
        actor_user_id=user.user_id,
        action='auth.login',
        resource_type='auth_session',
        resource_id=user.user_id,
        metadata_json={'role': user.role},
        request=request,
    )
    return FullTokenResponse(access_token=create_access_token(user.email, user.tenant_id, user.role), refresh_token=create_refresh_token(user.email, user.tenant_id, user.role))

@router.post('/refresh', response_model=FullTokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    claims = decode_token(payload.refresh_token)
    if claims.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail='invalid token')
    if await TokenStore(db).is_revoked(claims['jti']):
        raise HTTPException(status_code=401, detail='token revoked')
    return FullTokenResponse(access_token=create_access_token(claims['sub'], claims['tenant_id'], claims['role']), refresh_token=create_refresh_token(claims['sub'], claims['tenant_id'], claims['role']))

@router.get('/me')
async def me(user=Depends(current_user)):
    return {'email': user.email, 'role': user.role, 'tenant_id': user.tenant_id}

@router.post('/logout', response_model=MessageResponse)
async def logout(payload: RefreshRequest, request: Request, db: AsyncSession = Depends(get_db)):
    claims = decode_token(payload.refresh_token)
    tenant_id = claims.get('tenant_id', 'default')
    await TokenStore(db).revoke(claims['jti'], tenant_id)
    await write_audit(
        db,
        tenant_id=tenant_id,
        actor_user_id=claims.get('sub', 'unknown'),
        action='auth.logout',
        resource_type='auth_session',
        resource_id=claims.get('jti', 'unknown'),
        metadata_json={'jti': claims.get('jti')},
        request=request,
    )
    return MessageResponse(message='logged out')
