from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from security.auth import decode_token
from storage.membership_store import MembershipStore
from storage.token_store import TokenStore
from storage.user_store import UserStore

bearer = HTTPBearer(auto_error=True)


async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    try:
        claims = decode_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token') from exc
    if claims.get('type') != 'access':
        raise HTTPException(status_code=401, detail='invalid token type')
    if await TokenStore(db).is_revoked(claims['jti']):
        raise HTTPException(status_code=401, detail='token revoked')
    user = await UserStore(db).get_by_email(claims['sub'])
    if not user:
        raise HTTPException(status_code=401, detail='user not found')
    return user


async def tenant_scoped_user(
    x_tenant_id: str | None = Header(default=None, alias='X-Tenant-ID'),
    user=Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    tenant_id = x_tenant_id or user.tenant_id
    if user.role == 'admin':
        return user
    if tenant_id == user.tenant_id:
        return user
    has_access = await MembershipStore(db).has_membership(user.user_id, tenant_id)
    if not has_access:
        raise HTTPException(status_code=403, detail='tenant access denied')
    return user


def require_role(role: str) -> Callable:
    async def checker(user=Depends(current_user)):
        if user.role != role and user.role != 'admin':
            raise HTTPException(status_code=403, detail='forbidden')
        return user

    return checker
