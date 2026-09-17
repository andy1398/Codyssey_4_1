#saveLoad.py
""" 내보내기(Export): 가계부 데이터를 CSV 파일로 추출하여 Excel로 열거나 다른 사람과 공유하는 기능입니다. (예: "2024년 1월 지출 내역만 CSV로 추출")
가져오기(Import): 금융기관/카드사 앱에서 다운로드받은 내역이나 이전 백업 CSV를 한 번에 가계부로 불러오는 기능입니다.
csv 로 변환해야됨

제너레이터를 구현해서 저장할때나 가져올때 한줄씩 처리하도록 구현해야됨"""
# saveLoad.py
# saveLoad.py
"""
[데이터 저장 및 변환 모듈]
- JSONL (JSON Lines): 한 줄에 하나의 JSON 객체를 저장하여 가계부 내부 메인 저장소로 사용합니다.
- CSV Export: 저장된 JSON/JSONL 데이터를 읽어서 엑셀(Excel) 등에서 열람 가능한 CSV 파일로 전환/내보내기 합니다.
- Generator(yield): 대용량 데이터 처리 시 메모리 과부하를 방지하기 위해 한 줄씩 스트리밍 처리합니다.
"""

import json
import csv
from typing import List, Generator
from transaction import transaction
from budget import budget
from catagory import Category
# ==========================================
# 1. JSON (JSONL) 내부 데이터 관리
# ==========================================

def _transaction_to_dict_gen(transactions: List[transaction]) -> Generator[dict, None, None]:
    """[제너레이터] transaction 객체 리스트를 순회하며 딕셔너리 형태로 한 줄씩 내보냅니다."""
    for tx in transactions:
        yield {
            "id": tx.id,
            "money": tx.money,
            "date": tx.date,
            "memo": tx.memo,
            "tags": tx.tags
        }

def save_json(filepath: str, transactions: List[transaction]):
    """가계부 내역을 JSONL 파일로 안전하게 저장 (메인 저장소)"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in _transaction_to_dict_gen(transactions):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f" 데이터가 성공적으로 저장되었습니다: {filepath}")

def load_json_gen(filepath: str) -> Generator[transaction, None, None]:
    """[제너레이터] JSONL 파일에서 한 줄씩 읽어와 transaction 객체로 불러옵니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    yield transaction(
                        id=int(data["id"]),
                        money=float(data["money"]),
                        date=str(data["date"]),
                        memo=str(data["memo"]),
                        tags=str(data["tags"])
                    )
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    print(f"경고: {line_num}번째 줄 손상된 데이터 건너뜀 -> {e}")
                    continue
    except FileNotFoundError:
        print(f"ℹ {filepath} 파일이 없습니다. 빈 상태로 시작합니다.")


# ==========================================
# 2. JSON 기반 데이터 -> CSV 변환 및 내보내기 (Export)
# ==========================================

def export_json_to_csv(json_filepath: str, csv_filepath: str):
    """
    저장되어 있는 JSONL 파일을 읽어서 CSV 파일로 변환 내보내기
    (엑셀에서 한글이 깨지지 않도록 utf-8-sig 인코딩을 적용)
    """
    fieldnames = ["id", "money", "date", "memo", "tags"]

    try:
        # 1. JSONL 파일 읽기 제너레이터 연결
        tx_generator = load_json_gen(json_filepath)

        # 2. CSV 파일 쓰기
        with open(csv_filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader() # 헤더(열 이름) 작성

            count = 0
            # load_json_gen에서 한 줄씩 읽어온 객체를 CSV row로 즉시 변환해서 작성
            for tx in tx_generator:
                writer.writerow({
                    "id": tx.id,
                    "money": tx.money,
                    "date": tx.date,
                    "memo": tx.memo,
                    "tags": tx.tags
                })
                count += 1

        print(f"📊 CSV 내보내기 완료! (총 {count}건): {csv_filepath}")

    except FileNotFoundError:
        print(f" 내보낼 데이터 파일({json_filepath})이 존재하지 않습니다.")
    except Exception as e:
        print(f" CSV 내보내기 중 오류 발생: {e}")


def export_memory_to_csv(transactions: List[transaction], csv_filepath: str):
    """현재 메모리(프로그램) 상의 transaction 목록을 즉시 CSV로 내보내기"""
    fieldnames = ["id", "money", "date", "memo", "tags"]
    
    with open(csv_filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for tx_dict in _transaction_to_dict_gen(transactions):
            writer.writerow(tx_dict)
            
    print(f"CSV 추출 완료: {csv_filepath}")