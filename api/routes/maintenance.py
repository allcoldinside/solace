from fastapi import APIRouter
router = APIRouter(tags=['maintenance'])
@router.get('/maintenance')
async def maintenance(): return {'status':'ok','maintenance':False}
