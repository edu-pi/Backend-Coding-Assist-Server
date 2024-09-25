import re
import subprocess
import tempfile
import textwrap

from app.exception.custom_error import CustomError
from app.exception.invalid_exception import InvalidException


def check(code):
    # 들여쓰기 제거
    code = textwrap.dedent(code)

    # 임시 파일을 생성하여 코드 저장
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    # PyFlakes 명령어를 subprocess를 통해 실행
    result = subprocess.run(
        ['flake8', temp_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # 임시 파일 삭제
    subprocess.run(['rm', temp_file_path])

    if result.returncode != 0:
        syntax_error_message = extract_error_message(result.stdout)

        raise InvalidException(
            custom_error=CustomError.STATIC_SYNTAX_ERROR,
            result={"error": syntax_error_message}
        )

    return True


def extract_error_message(error_string):
    # [행:열: error message] 형태로 추출
    pattern = r"(\d+:\d+: [^\n]+)"

    # 정규 표현식을 사용하여 매칭된 부분 추출
    match = re.search(pattern, error_string)

    if match:
        return match.group(1)  # 매칭된 부분을 반환
    else:
        return "No match found."