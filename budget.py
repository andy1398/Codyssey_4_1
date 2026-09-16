""" 달마다 예산을 설정하고 조회한다   """
#buget.py

class budget:
    def __init__(self, month, money):
        self.budget = []
    def add_budget(self, month, money):
        num=len(self.budget)
        for i in range(num):
            if self.budget[i].month==month:
                print("이미 해당 달의 예산이 존재합니다. 수정하려면 Y/N를 입력하세요.")
                choice = input().upper()
                self.modify_budget(money,i)
                return
        self.budget.append({'month': month, 'money': money})

    def modify_budget(self, money,index):
        self.budget[index].money=money