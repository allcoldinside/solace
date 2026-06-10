from fastapi import APIRouter, Depends

from security.deps import current_user, tenant_scoped_user

router = APIRouter(prefix='/system', tags=['system'])


@router.get('/info')
async def info():
    return {'name': 'SOLACE', 'version': '1.0.0'}


@router.get('/protected')
async def protected(_user=Depends(current_user)):
    return {'status': 'ok'}


@router.get('/tenant-access')
async def tenant_access(_user=Depends(tenant_scoped_user)):
    return {'status': 'ok'}
