from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions.business_exceptions import EntityAlreadyExistsError, EntityNotFoundError

async def entity_already_exists_handler(request: Request, exc: EntityAlreadyExistsError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail},
    )

async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detail},
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(EntityAlreadyExistsError, entity_already_exists_handler)
    app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
