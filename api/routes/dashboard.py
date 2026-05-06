from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/dashboard', tags=['dashboard'])


@router.get('', response_class=HTMLResponse)
async def dashboard_home() -> str:
    path = Path('panel/templates/dashboard_mvp.html')
    return path.read_text(encoding='utf-8')
