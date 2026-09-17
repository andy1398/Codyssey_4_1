import sys
import argparse
from transaction import transaction
from transactionControl import transactionControl
from catagory import Category
from budget import budget
from saveLoad import export_to_csv, import_from_csv
from exception import handle_errors

@handle_errors
def main():
    parser = argparse.ArgumentParser(prog="budget_app")
    parser.add_argument("command", choices=["add", "list", "search", "summary", "budget", "category", "delete", "export", "import"])
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--month")
    parser.add_argument("--amount", type=int)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--id")
    parser.add_argument("--out")
    parser.add_argument("--from", dest="date_from")
    parser.add_argument("--to", dest="date_to")

    args, _ = parser.parse_known_args()

    tx_control = transactionControl()
    cat_obj = Category()
    bug_obj = budget()

    if args.command == "add":
        date = input("날짜(YYYY-MM-DD): ").strip()
        tx_type = input("타입(income/expense): ").strip()
        category = input("카테고리: ").strip()
        money = int(input("금액(양수): ").strip())
        memo = input("메모(선택): ").strip()
        tags = input("태그(쉼표로 구분, 없으면 엔터): ").strip()
        
        tx_id = f"TX-{len(tx_control.transactions) + 1:06d}"
        tx = transaction(tx_id, money, date, category, tx_type, memo, tags)
        tx_control.add_transaction(tx)
        print(f"[저장 완료] id={tx_id}")

    elif args.command == "list":
        tx_control.list_transactions(args.limit)

    elif args.command == "summary":
        if not args.month:
            print("월(--month YYYY-MM)을 입력하세요.")
            return
        tx_control.summary(args.month, args.top, bug_obj)

    elif args.command == "budget":
        if args.month and args.amount:
            bug_obj.add_budget(args.month, args.amount)

    elif args.command == "category":
        sub = input("동작 선택 (add/list/remove): ").strip()
        if sub == "add":
            name = input("카테고리명: ").strip()
            cat_obj.add_category(name)
        elif sub == "list":
            cat_obj.list_categories()
        elif sub == "remove":
            name = input("삭제할 카테고리명: ").strip()
            cat_obj.remove_category(name, tx_control.transactions)

    elif args.command == "delete":
        if args.id:
            tx_control.delete(args.id)

    elif args.command == "export":
        if args.out:
            export_to_csv(args.out, tx_control.transactions, args.month)

    elif args.command == "import":
        if args.date_from:
            import_from_csv(args.date_from, cat_obj, tx_control)

if __name__ == "__main__":
    main()