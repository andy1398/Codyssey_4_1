#category.py
""" 카테고리 관리 """
""" 카테고리 관리 """
""" 카테고리 관리 """
from exception import DataError

class Category:
    def __init__(self):
        # 기본 카테고리 목록
        self.categories = ["식비", "교통비", "주거비", "급여", "기타"]

    def add_category(self, name: str):
        if name in self.categories:
            raise DataError("이미 존재하는 카테고리입니다.", "category", name)
        self.categories.append(name)
        print(f"[저장 완료] category={name}")

    def remove_category(self, name: str, active_transactions: list):
        if name not in self.categories:
            raise DataError("존재하지 않는 카테고리입니다.", "category", name)
        
        # 참조 검증: 사용 중인 카테고리 삭제 막기
        for tx in active_transactions:
            if tx.category == name:
                raise DataError(f"카테고리 '{name}'은(는) 사용 중이므로 삭제할 수 없습니다.")
        
        self.categories.remove(name)
        print(f"[삭제 완료] category={name}")

    def list_categories(self):
        print("=== 카테고리 목록 ===")
        for c in self.categories:
            print(f"- {c}")