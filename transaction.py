#transaction.py
from dataclasses import dataclass
""" 돈의 흐름 구조도(변경 기능은 없음. 정의만)
카테고리,메모,태그,날짜,금액,타입(수입/지출) """

from exception import DataError

@dataclass
class transaction:
    id: int
    money: int
    date: str
    memo: str
    tags: str
    
    def __post_init__(self):
        """객체가 생성된 직후 자동으로 실행되는 검증 메서드"""
        self.validate_types()
        self.validate_values()
        
    def validate_types(self):
        """1. 타입 검증 (money가 float/int 인지, date가 str 인지 등)"""
        # (변수명, 기대하는 타입)
        expected_types = {
            "id": int,
            "money": int,
            "date": str,
            "memo": str,
            "tags": str,
        }

        for field_name, expected_type in expected_types.items():
            actual_value = getattr(self, field_name)
            
            # isinstance로 타입 검사
            if not isinstance(actual_value, expected_type):
                raise DataError(
                    message=f"{field_name}의 타입은 {expected_type} 이어야 합니다.",
                    value_name=field_name,
                    value=actual_value
                )

    def validate_values(self):
        """2. 값 유효성 검증 (금액이 양수인지, 날짜 형식이 맞는지 등)"""
        if self.money <= 0:
            raise DataError(
                message="금액은 0보다 큰 양수여야 합니다.",
                value_name="money",
                value=self.money
            )
        
        if self.id <= 0:
            raise DataError(
                message="ID는 1 이상의 정수여야 합니다.",
                value_name="id",
                value=self.id
            )
    
    
       
    # def validate_type(self,name):
    #     # self.__dict__에 인스턴스 변수들이 {'변수명': 값} 형태로 들어있음
    #     if name in self.__dict__ and type(name)!=사용자 입력값의 형식:
    #         target_value = self.__dict__[name]
    #         raise DataError(message="{value_name}의 형식은 {target_value}입니다",            
    #                         value_name=변수이름,
    #                         value=target_value)
    #     else
    #         print("변수가 없어요")
            
    # def validate_value(self,name):
    #         # self.__dict__에 인스턴스 변수들이 {'변수명': 값} 형태로 들어있음
    #         if name in self.__dict__ and name!=사용자 입력값:
    #             target_value = self.__dict__[name]
    #             raise DataError(message="{value_name}의 형식은 {target_value}입니다",            
    #                             value_name=변수이름,
    #                             value=target_value)
    #         else
    #             print("변수가 없어요")
            
            
            #변수가 없다고 알림 
        """조건문에 내가 만든 검증 함수를 넣어. 내가 예외처리 파일에 만든 함수에 올려
        """
