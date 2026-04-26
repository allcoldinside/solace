from fastapi import APIRouter
router = APIRouter(prefix='/system', tags=['system'])
@router.get('/info')
async def info(): return {'name':'SOLACE','version':'1.0.0'}
