from fastapi import Request
from fastapi.responses import JSONResponse


async def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse({'detail': str(exc)}, status_code=500)
