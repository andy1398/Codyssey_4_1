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
""" 데이터 저장, 로드 및 CSV 변환 모듈 """
import json
import csv
import os
import tempfile
from typing import Generator
from transaction import transaction

DATA_DIR = "./data"
TX_FILE = os.path.join(DATA_DIR, "transactions.jsonl")
CAT_FILE = os.path.join(DATA_DIR, "categories.json")
BUG_FILE = os.path.join(DATA_DIR, "budgets.json")

def ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

# [원자적 저장] 임시 파일 작성 후 교체
def safe_save_jsonl(filepath: str, data_list: list):
    ensure_dir()
    fd, temp_path = tempfile.mkstemp(dir=DATA_DIR, text=True)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        for item in data_list:
            f.write(json.dumps(item if isinstance(item, dict) else item.to_dict(), ensure_ascii=False) + '\n')
    os.replace(temp_path, filepath)

# [제너레이터 스트리밍] 한 줄씩 로드
def load_json_gen(filepath: str) -> Generator[transaction, None, None]:
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                yield transaction(
                    id=str(d["id"]),
                    money=int(d["money"]),
                    date=str(d["date"]),
                    category=str(d["category"]),
                    type=str(d["type"]),
                    memo=str(d.get("memo", "")),
                    tags=str(d.get("tags", ""))
                )
            except Exception:
                continue

# CSV 내보내기 (Export)
def export_to_csv(csv_path: str, transactions: list, month: str = None):
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ["date", "type", "category", "amount", "memo", "tags"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        count = 0
        for tx in transactions:
            if month and not tx.date.startswith(month):
                continue
            writer.writerow({
                "date": tx.date,
                "type": tx.type,
                "category": tx.category,
                "amount": tx.money,
                "memo": tx.memo,
                "tags": tx.tags
            })
            count += 1
    print(f"[완료] {csv_path} ({count} records)")

# CSV 가져오기 (Import)
def import_from_csv(csv_path: str, category_obj, tx_control):
    imported, skipped = 0, 0
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["category"] not in category_obj.categories:
                    skipped += 1
                    continue
                new_id = f"TX-{len(tx_control.transactions) + 1:06d}"
                tx = transaction(
                    id=new_id,
                    money=int(row["amount"]),
                    date=row["date"],
                    category=row["category"],
                    type=row["type"],
                    memo=row.get("memo", ""),
                    tags=row.get("tags", "")
                )
                tx_control.add_transaction(tx)
                imported += 1
        print(f"[완료] imported={imported}, skipped={skipped}")
    except FileNotFoundError:
        print("[오류] 가져올 CSV 파일이 없습니다.")