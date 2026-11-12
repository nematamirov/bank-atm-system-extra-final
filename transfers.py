
from account_ops import reset_daily_if_new_day, MAX_TRANSFERS
from history import add_history
from storage import save_data
from utils import format_money, ask_amount


def find_user_by_account(data, account_number):
    
    for name in data["users"]:
        if data["users"][name]["account_number"] == account_number:
            return name, data["users"][name]
    return None, None


def transfer(data, sender_name):
    sender = data["users"][sender_name]
    reset_daily_if_new_day(sender)

    # Gunde max 5 ugurlu geden transfer. 6-cisi redd olunur.
    if sender["daily"]["transfer_count"] >= MAX_TRANSFERS:
        print("Transfer declined: daily limit of " + str(MAX_TRANSFERS)
              + " outgoing transfers reached.")
        return

    account = input("Recipient account number: ").strip()
    receiver_name, receiver = find_user_by_account(data, account)
    if receiver is None:
        print("Recipient account not found.")
        return
    if receiver_name == sender_name:
        print("You cannot transfer money to your own account.")
        return

    amount = ask_amount("Amount: ")
    if amount is None:
        return
    if amount > sender["balance"]:
        print("Transfer declined: insufficient funds.")
        return

    print("Sender: " + sender_name)
    print("Recipient account: " + account)
    print("Amount: " + format_money(amount) + " AZN")
    answer = input("Confirm transfer (Y/N): ").strip().upper()
    if answer != "Y":
        print("Transfer cancelled. No changes were made.")
        return

    # Butun yoxlamalar kecdi. Indi deyisiklikler (ATM pulu deyismir).
    sender_before = sender["balance"]
    receiver_before = receiver["balance"]
    sender["balance"] = sender["balance"] - amount
    receiver["balance"] = receiver["balance"] + amount
    sender["daily"]["transfer_count"] = sender["daily"]["transfer_count"] + 1

    add_history(data, sender, "Transfer Sent", -amount,
                sender_before, sender["balance"], 0, account)
    add_history(data, receiver, "Transfer Received", amount,
                receiver_before, receiver["balance"], 0, sender["account_number"])

    save_data(data)      # iki balans BIR defe yazilir

    print("")
    print("Transfer successful.")
    print("Sender new balance: " + format_money(sender["balance"]) + " AZN")
