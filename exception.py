#exception.py
""" 날짜 형식 오류: YYYY-MM-DD (거래 날짜) 또는 YYYY-MM (월별 요약/예산) 형식이 맞지 않거나, 존재하지 않는 날짜(예: 2026-02-31)가 들어온 경우
금액 오류: 금액이 정수가 아니거나, 0 이하의 음수/0이 들어온 경우 (amount > 0 조건 위반)
타입 오류: 거래 타입이 income 또는 expense 이외의 값이 들어온 경우
카테고리 오류: 미리 정의되지 않은 미등록 카테고리가 입력된 경우
검색/조회 범위 오류: 기간 검색 시 시작일(--from)이 종료일(--to)보다 더 뒤에 있는 경우
파일 미존재 (File Not Found): transactions.jsonl, categories.json, budgets.json 등 저장 파일이 없을 때 깨지지 않고 빈 파일/기본 구조를 생성하며 동작해야 함
데이터 깨짐 / 파싱 오류 (JSONDecodeError, CSV Parse Error): JSONL 파일이나 외부 CSV 파일의 특정 줄이 손상되었을 때 전체 프로그램이 중단되지 않고 해당 오류를 격리/건너뛰거나 알림 처리
ID 미존재 오류: delete 또는 update 시 존재하지 않는 거래 ID(TX-XXXXXX)를 지정한 경우
예산 미설정 상태 요약: 해당 월에 설정된 예산이 없을 때 연산 오류가 나지 않고 미설정 또는 안내 문구 출력 """
""" 예외 처리 및 공통 데코레이터 """
from functools import wraps
import sys
import logging

logging.basicConfig(filename="app.log", level=logging.INFO, encoding="utf-8")

class DataError(Exception):
    def __init__(self, message: str, value_name=None, value=None):
        super().__init__(message)
        self.message = message
        self.value_name = value_name
        self.value = value

def handle_errors(func):
    """에러를 잡아서 힌트와 함께 깔끔하게 출력하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.info(f"실행: {func.__name__}")
            return func(*args, **kwargs)
        except DataError as e:
            print(f"[오류] {e.message}")
            if e.value_name and e.value is not None:
                print(f"👉 힌트: {e.value_name} 필드의 입력값 '{e.value}'을(를) 확인해 주세요.")
            sys.exit(1)
        except Exception as e:
            print(f"[시스템 오류] 처리 중 에러가 발생했습니다: {e}")
            logging.error(f"오류 발생: {e}", exc_info=True)
            sys.exit(2)
    return wrapper