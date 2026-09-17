""" 달마다 예산을 설정하고 조회한다 """

class budget:
    def __init__(self):
        self.budgets = []  # {'month': 'YYYY-MM', 'money': 100000} 리스트로 관리

    def add_budget(self, month: str, money: int):
        for b in self.budgets:
            if b['month'] == month:
                b['money'] = int(money)
                print(f"[수정 완료] {month} 예산 {money}원")
                return
        self.budgets.append({'month': month, 'money': int(money)})
        print(f"[저장 완료] {month} 예산 {money}원")

    def get_budget(self, month: str):
        for b in self.budgets:
            if b['month'] == month:
                return b['money']
        return None