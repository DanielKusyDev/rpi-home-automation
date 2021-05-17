import json

from fastapi import HTTPException
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

NotFound = HTTPException(status_code=404, detail="Item not found")


async def validation_error_handler(_: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(json.loads(exc.json()), status_code=400)
