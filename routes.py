import logging
import requests
from fastapi import APIRouter
from starlette.responses import JSONResponse

from models.error_code import ErrorCode
from models.error_response import ErrorResponse
from models.success_reponse import SuccessResponse
from services.request_code import RequestCode
from services.syntax_checker import check_code, extract_error_message
from settings import Settings

router = APIRouter()

# init logging
logger = logging.getLogger('uvicorn.logger')
logger.setLevel(logging.INFO)


@router.post("/edupi_syntax/v1/check/static")
async def syntax_check(code: RequestCode):
    return_code, stdout = check_code(code.source_code)

    # 문법 오류가 있을 때
    if return_code != 0:
        syntax_error_message = extract_error_message(stdout)

        error_response = ErrorResponse(
            code=ErrorCode.STATIC_SYNTAX_ERROR.code,
            detail_message=ErrorCode.STATIC_SYNTAX_ERROR.message,
            result=syntax_error_message
        )
        logger.info(f"Fail syntax check [code : {code.source_code}, reason: {syntax_error_message}]")

        return JSONResponse(
            status_code=400,
            content=error_response.to_dict()
        )

    # 시각화 분석 엔진으로 코드 분석 요청
    else:
        analysis_result = requests.post(
            Settings.ENGINE_SERVER,
            json={"source_code": code.source_code}
        )

        success_response = SuccessResponse(
            detail_message="success code analysis",
            result=analysis_result.json()
        )

        return JSONResponse(
            status_code=200,
            content=success_response.to_dict()
        )
