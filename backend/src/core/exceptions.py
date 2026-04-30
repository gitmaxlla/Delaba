from typing import cast
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RootEntityViolationError(AppError):
    pass


class LLMGenerationError(AppError):
    pass


class InstanceNotFound(AppError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


async def instance_not_found_handler(request: Request, exc: Exception):
    exc = cast(InstanceNotFound, exc)
    return JSONResponse(status_code=404, content={"message": exc.message})


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(InstanceNotFound, instance_not_found_handler)
