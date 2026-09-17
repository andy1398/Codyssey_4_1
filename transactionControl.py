#transactionControl.py
""" 돈의 흐름 조작
추가, 삭제, 출력??, 검색, 수정,  """
""" 거래 내역 조작 컨트롤러 """
from saveLoad import load_json_gen, safe_save_jsonl, TX_FILE

class transactionControl:
    def __init__(self):
        # 파일에서 제너레이터 스트리밍으로 기본 데이터 불러오기
        self.transactions = list(load_json_gen(TX_FILE))

    def save(self):
        safe_save_jsonl(TX_FILE, self.transactions)

    def add_transaction(self, tx):
        self.transactions.append(tx)
        self.save()

    # 목록 출력 (list)
    def list_transactions(self, limit: int = 10):
        # 최신순 정렬
        sorted_txs = sorted(self.transactions, key=lambda x: x.date, reverse=True)[:limit]
        for tx in sorted_txs:
            print(f"{tx.id} | {tx.date} | {tx.type:<7} | {tx.category:<8} | {tx.money:,}원 | {tx.memo}")

    # 삭제 (delete)
    def delete(self, tx_id: str):
        for i, tx in enumerate(self.transactions):
            if tx.id == tx_id:
                del self.transactions[i]
                self.save()
                print(f"[삭제 완료] id={tx_id}")
                return
        print("[오류] 해당 ID의 거래를 찾을 수 없습니다.")

    # 검색 (search)
    def search(self, date_from=None, date_to=None, category=None, tx_type=None, memo=None, tags=None):
        results = []
        for tx in reversed(self.transactions):
            if date_from and tx.date < date_from:
                continue
            if date_to and tx.date > date_to:
                continue
            if category and tx.category != category:
                continue
            if tx_type and tx.type != tx_type:
                continue
            if memo and memo not in tx.memo:
                continue
            if tags and tags not in tx.tags:
                continue
            results.append(tx)

        for tx in results:
            print(f"{tx.id} | {tx.date} | {tx.type:<7} | {tx.category:<8} | {tx.money:,}원 | {tx.memo}")

    # 월별 요약 (summary)
    def summary(self, month: str, top_n: int, budget_obj):
        income, expense = 0, 0
        cat_expense = {}

        for tx in self.transactions:
            if tx.date.startswith(month):
                if tx.type == "income":
                    income += tx.money
                else:
                    expense += tx.money
                    cat_expense[tx.category] = cat_expense.get(tx.category, 0) + tx.money

        if income == 0 and expense == 0:
            print(f"[{month}] 해당 달의 데이터가 없습니다.")
            return

        print(f"총 수입: {income:,}원")
        print(f"총 지출: {expense:,}원")
        print(f"잔   액: {income - expense:,}원")

        # 예산 연동 및 초과 경고
        b_amount = budget_obj.get_budget(month)
        if b_amount:
            rate = (expense / b_amount) * 100
            print(f"예   산: {b_amount:,}원 (사용률 {rate:.1f}%)")
            if expense > b_amount:
                print("⚠️ [경고] 월 예산을 초과했습니다!")

        # 카테고리 TOP N
        top_cats = sorted(cat_expense.items(), key=lambda x: x[1], reverse=True)[:top_n]
        print(f"\n지출 TOP {top_n}")
        for idx, (cat, amt) in enumerate(top_cats, 1):
            print(f"{idx}) {cat} {amt:,}원")