#main.py

from transaction import transaction
from transactionControl import transactionControl
from catagory import Category
from budget import budget

type=input("타입: ")
amount=input("금액: ")
category=input("카테고리: ")
date=input("날짜: ")
memo=input("메모: ")
tags=input("태그: ")
id=input("ID: ")
Ob_category=Category(category,type,id)
Ob_person = transaction(id, amount, date, memo, tags)

print("예산을 설정하시겠습니까? (Y/N)")
answer = input().strip().upper()
if answer == "Y":
    month=input("예산을 설정할 월을 입력하세요(YYYY-MM): ")
    amount=input("예산 금액을 입력하세요: ")
    id=input("ID: ")
    Ob_budget = budget(month, amount,id)
else:
    print("예산 설정을 건너뜁니다.")