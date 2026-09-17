#transaction.py
from dataclasses import dataclass
""" 돈의 흐름 구조도(변경 기능은 없음. 정의만)
카테고리,메모,태그,날짜,금액,타입(수입/지출) """

from exception import DataError

@dataclass
class transaction:
    id: str
    money: int
    date: str
    category: str
    type: str  # income / expense
    memo: str = ""
    tags: str = ""
    
    def __post_init__(self):
        # 금액 검증
        if int(self.money) <= 0:
            raise DataError("금액은 0보다 큰 양수여야 합니다.", "money", self.money)
        # 타입 검증
        if self.type not in ("income", "expense"):
            raise DataError("타입은 'income' 또는 'expense'여야 합니다.", "type", self.type)

    def to_dict(self):
        return {
            "id": self.id,
            "money": int(self.money),
            "date": self.date,
            "category": self.category,
            "type": self.type,
            "memo": self.memo,
            "tags": self.tags
        }
            
            #변수가 없다고 알림 
        """조건문에 내가 만든 검증 함수를 넣어. 내가 예외처리 파일에 만든 함수에 올려
        """
