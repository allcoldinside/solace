from fastapi import APIRouter, Depends
from security.deps import current_user
router = APIRouter(prefix='/graph', tags=['graph'])
@router.get('')
async def graph(_=Depends(current_user)): return {'status':'stub','replaceable':True}
