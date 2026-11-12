
from utils import format_money, now_text


def add_history(data, user, type_name, amount, before, after, fee, other_account):
    
    # Unikal ID: TXN0001, TXN0002 ... (sayac butun banka aiddir)
    number = data["next_id"]
    txn_id = "TXN" + str(number).zfill(4)
    data["next_id"] = number + 1

    now = now_text()
    record = {
        "id": txn_id,
        "date": now,
        "type": type_name,
        "amount": amount,              # cixan pul menfi, gelen pul musbet
        "balance_before": before,
        "balance_after": after,
        "fee": fee,
        "other_account": other_account,
    }
    user["history"].append(record)
    user["last_transaction"] = now


def show_history(user):
  
    history = user["history"]
    if len(history) == 0:
        print("No transactions yet.")
        return

    stop = len(history) - 10           # 10-dan az varsa menfi olur
    if stop < 0:
        stop = 0

    for i in range(len(history) - 1, stop - 1, -1):    # axirdan evvele
        r = history[i]
        print("------------------------------------")
        print("ID: " + r["id"])
        print("Date: " + r["date"])
        print("Type: " + r["type"])
        if r["other_account"] != "":
            print("Other account: " + r["other_account"])
        print("Amount: " + format_money(r["amount"]) + " AZN")
        if r["fee"] > 0:
            print("Fee: " + format_money(r["fee"]) + " AZN")
        print("Balance before: " + format_money(r["balance_before"]) + " AZN")
        print("Balance after: " + format_money(r["balance_after"]) + " AZN")
    print("------------------------------------")
