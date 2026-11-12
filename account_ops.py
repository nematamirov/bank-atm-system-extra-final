
from history import add_history
from storage import save_data
from utils import format_money, ask_amount, today_text


DAILY_DEPOSIT_MAX = 200000     # gunde max depozit
FREE_WITHDRAW = 50000          # komissiyasiz cekme: 500 AZN
DAILY_WITHDRAW_MAX = 100000    # gunde max cekme: 1000 AZN
FEE_PERCENT = 2                # komissiya faizi
MAX_TRANSFERS = 5              # gunde max gedan transfer


def reset_daily_if_new_day(user):
    
    daily = user["daily"]
    if daily["date"] != today_text():
        daily["date"] = today_text()
        daily["deposit_total"] = 0
        daily["withdraw_total"] = 0
        daily["transfer_count"] = 0


def show_account_info(username, user):
    print("Account Holder : " + username)
    print("Account Number : " + user["account_number"])
    print("Available Balance: " + format_money(user["balance"]) + " AZN")
    if user["blocked"]:
        print("Account Status: Blocked")
    else:
        print("Account Status: Active")


def show_balance(user):
    print("Available Balance: " + format_money(user["balance"]) + " AZN")


def deposit(data, username):
    user = data["users"][username]
    reset_daily_if_new_day(user)
    daily = user["daily"]

    amount = ask_amount("Deposit amount: ")
    if amount is None:
        return

    remaining = DAILY_DEPOSIT_MAX - daily["deposit_total"]
    print("Deposited today: " + format_money(daily["deposit_total"]) + " AZN")
    print("Requested deposit: " + format_money(amount) + " AZN")
    print("Daily deposit maximum: " + format_money(DAILY_DEPOSIT_MAX) + " AZN")
    print("Remaining deposit allowance: " + format_money(remaining) + " AZN")

    # Limiti asirsa BUTUN emeliyyat redd olunur (meblegi azaltmaq olmaz)
    if amount > remaining:
        print("")
        print("Deposit declined: daily limit would be exceeded.")
        print("Account balance and ATM cash remain unchanged.")
        return

    before = user["balance"]
    user["balance"] = user["balance"] + amount
    data["atm_cash"] = data["atm_cash"] + amount       # depozit ATM-e pul qoyur
    daily["deposit_total"] = daily["deposit_total"] + amount
    add_history(data, user, "Deposit", amount, before, user["balance"], 0, "")
    save_data(data)

    print("")
    print("Deposit successful.")
    print("New balance: " + format_money(user["balance"]) + " AZN")
    print("Remaining deposit allowance: "
          + format_money(DAILY_DEPOSIT_MAX - daily["deposit_total"]) + " AZN")


def calculate_fee(already_withdrawn, amount):
   
    free_left = FREE_WITHDRAW - already_withdrawn      # komissiyasiz nece qalib
    if free_left < 0:
        free_left = 0

    taxable = amount - free_left                       # komissiya tutulan hisse
    if taxable < 0:
        taxable = 0

    fee = (taxable * FEE_PERCENT + 50) // 100          # 2%, +50 yuvarlaqlasdirir
    return fee


def withdraw(data, username):
    user = data["users"][username]
    reset_daily_if_new_day(user)
    daily = user["daily"]

    amount = ask_amount("Withdrawal amount: ")
    if amount is None:
        return

    already = daily["withdraw_total"]
    fee = calculate_fee(already, amount)

    # Evvelce HAMI yoxlanir, hec bir sey deyismeden
    if already + amount > DAILY_WITHDRAW_MAX:
        print("Withdrawal declined: daily withdrawal limit would be exceeded.")
        print("Remaining withdrawal allowance: "
              + format_money(DAILY_WITHDRAW_MAX - already) + " AZN")
        return

    if amount + fee > user["balance"]:
        print("Withdrawal declined: insufficient balance (including commission).")
        return

    if amount > data["atm_cash"]:
        print("Transaction declined: insufficient ATM cash.")
        return

    # Hamisi kecdi, indi deyisiklikler:
    before = user["balance"]
    user["balance"] = user["balance"] - amount - fee   # hesabdan pul + komissiya
    data["atm_cash"] = data["atm_cash"] - amount       # ATM-den yalniz verilen pul
    daily["withdraw_total"] = already + amount         # komissiya sayilmir

    add_history(data, user, "Withdrawal", -amount, before, before - amount, fee, "")
    if fee > 0:
        add_history(data, user, "Withdrawal Commission", -fee,
                    before - amount, user["balance"], fee, "")
    save_data(data)

    print("Withdrawal successful.")
    print("Cash paid out: " + format_money(amount) + " AZN")
    print("Withdrawal commission: " + format_money(fee) + " AZN")
    print("Amount deducted from account: " + format_money(amount + fee) + " AZN")
    print("New balance: " + format_money(user["balance"]) + " AZN")


def show_daily_limits(user):
    reset_daily_if_new_day(user)
    d = user["daily"]

    free_left = FREE_WITHDRAW - d["withdraw_total"]
    if free_left < 0:
        free_left = 0

    print("=========== DAILY LIMITS ===========")
    print("Deposit used:        " + format_money(d["deposit_total"])
          + " / " + format_money(DAILY_DEPOSIT_MAX) + " AZN")
    print("Deposit remaining:   "
          + format_money(DAILY_DEPOSIT_MAX - d["deposit_total"]) + " AZN")
    print("Cash withdrawn:      " + format_money(d["withdraw_total"])
          + " / " + format_money(DAILY_WITHDRAW_MAX) + " AZN")
    print("Cash withdrawal remaining: "
          + format_money(DAILY_WITHDRAW_MAX - d["withdraw_total"]) + " AZN")
    print("Fee-free cash remaining: " + format_money(free_left) + " AZN")
    print("Outgoing transfers:  " + str(d["transfer_count"]) + " / " + str(MAX_TRANSFERS))
    print("====================================")
