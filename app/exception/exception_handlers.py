from starlette import status

from app.exception.base_custom_exception import BaseCustomException
from app.exception.custom_error import CustomError
from app.exception.invalid_exception import InvalidException
from app.models.error_response import ErrorResponse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidException)
    async def invalid_exception_handler(request: Request, exc: InvalidException):
        response = ErrorResponse(
            code=exc.custom_error.code,
            detail=exc.custom_error.detail,
            result=exc.result
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response.to_dict()
        )

    @app.exception_handler(BaseCustomException)
    async def base_exception_handler(request: Request, exc: BaseCustomException):
        response = ErrorResponse(
            code=exc.custom_error.code,
            detail=exc.custom_error.detail,
            result=exc.result
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response.to_dict()
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        response = ErrorResponse(
            code=CustomError.UNKNOWN_ERROR.code,
            detail=CustomError.UNKNOWN_ERROR.detail,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.to_dict()
        )