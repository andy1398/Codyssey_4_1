#transactionControl.py
""" 돈의 흐름 조작
추가, 삭제, 출력??, 검색, 수정,  """

from datetime import datetime
from exception import ValueError


#용돈 기입장
class transactionControl:
    def __init__(self):
        self.transactions = []
        
#내역 추가
    def add_transaction(self,Ob_transaction):
        self.transactions.append(Ob_transaction)

#거래 삭제  
    def delete(self, id):
        num=len(self.transactions)
        for i in range(num):
            if self.transactions[i].id==id:
                del self.transactions[i]
                return
        print("해당 ID의 거래를 찾을 수 없습니다.")
        
#카테고리,메모,태그,날짜,금액,타입으로 검색
    def search(self):
        date_from=input("검색 조건을 입력하세요(시작 기간): ")
        date_to=input("검색 조건을 입력하세요(종료 기간): ")
        category=input("검색 조건을 입력하세요(카테고리): ")
        type=input("검색 조건을 입력하세요(타입): ")
        memo=input("검색 조건을 입력하세요(메모 키워드): ")
        tags=input("검색 조건을 입력하세요(태그): ")        
        filter1=self.date(date_from,date_to)
        filter2=self.category(category,filter1)
        filter3=self.type(type,filter2)
        filter4=self.memo(memo,filter3)
        Ob_filter5=self.tags(tags,filter4)
        return Ob_filter5

    def date(self, var_date_from:str, var_date_to:str):
        filtered=[]
       
        try:
            # 1. 입력받은 문자열 날짜를 datetime 객체로 변환
            from_dt = datetime.strptime(var_date_from, "%Y-%m-%d")
            to_dt = datetime.strptime(var_date_to, "%Y-%m-%d")
        except ValueError:
            print("날짜 형식이 올바르지 않습니다. (YYYY-MM-DD 형식으로 입력해주세요)")
            return filtered

        # 시작일이 종료일보다 뒤에 있는 예외 케이스 체크
        if from_dt > to_dt:
            print("시작 기간이 종료 기간보다 이후일 수 없습니다.")
            return filtered

        # 2. 거래 내역 순회하며 범위 조건 검색 (한 줄 비교)
        for tx in self.transactions:
            try:
                tx_dt = datetime.strptime(tx.date, "%Y-%m-%d")

                # datetime 객체끼리는 바로 범위를 비교(<=)할 수 있습니다.
                if from_dt <= tx_dt <= to_dt:
                    filtered.append(tx)
            except ValueError:
                # 거래 데이터 내부의 날짜가 잘못된 경우 건너뜀
                continue

        return filtered
    
    
    def category(self, var_category:str, Ob_filtered:list):
        result=[]
        num=len(Ob_filtered)
        for i in range(num):
            if Ob_filtered[i].category==var_category:
                result.append(Ob_filtered[i])
        return result   
        
    def type(self, var_type,Ob_filtered):
        result=[]
        num=len(Ob_filtered)
        for i in range(num):
            if Ob_filtered[i].type==var_type:
                result.append(Ob_filtered[i])
        return result

    def memo(self, var_memo,Ob_filtered):
        result=[]
        num=len(Ob_filtered)
        for i in range(num):
            if Ob_filtered[i].memo==var_memo:
                result.append(Ob_filtered[i])
        return result

    def tags(self, var_tags,Ob_filtered):
        result=[]
        num=len(Ob_filtered)
        for i in range(num):
            if Ob_filtered[i].tags==var_tags:
                result.append(Ob_filtered[i])
        return result
        
#수정     
    def modify(self, id):
        num=len(self.transactions)
        for i in range(num):
            if self.transactions[i].id==id:
                print("거래를 수정합니다. 수정하지 않을 항목은 Enter를 눌러 건너뛰세요.")
                type=input("타입: ").strip()
                amount=input("금액: ").strip()
                category=input("카테고리: ").strip()
                date_from=input("시작 날짜: ").strip()
                date_to=input("종료 날짜: ").strip()
                memo=input("메모: ").strip()
                tags=input("태그: ").strip()
                if type:
                    self.transactions[i].type=type
                if amount:
                    self.transactions[i].amount=amount
                if category:
                    self.transactions[i].category=category
                if date_from:
                    self.transactions[i].date_from=date_from
                if date_to:
                    self.transactions[i].date_to=date_to
                if memo:
                    self.transactions[i].memo=memo
                if tags:
                    self.transactions[i].tags=tags
                return
        print("해당 ID의 거래를 찾을 수 없습니다.")

#출력
    def show(self,id):
        num=len(self.transactions)
        for i in range(num):
            if self.transactions[i].id==id:
                return self.transactions[i]
        print("해당 ID의 거래를 찾을 수 없습니다.")

#월별요약
    """ top은 지출 금액이 가장 큰 상위 N개 카테고리   """
    def summary(self,top,Ob_budget,Ob_category):
        month=input("월별 요약을 원하는 월을 입력하세요(YYYY-MM): ")
        num=len(self.transactions)
        total_income=0
        total_expenses=0
        
        for i in range(num):   
            if self.transactions[i].date[0:7] == month[0:7]:
                self.transactions[i].money

# 예산이 설정되어 있다면 예산 대비 사용률(%),초과 여부(초과 시 경고 문구) 를 함께 출력해야 합니다.


"""transactionControl객체, 찾는 조건(month,top), budget객체)
        """ 