
from account_ops import (reset_daily_if_new_day, show_account_info, show_balance,deposit, withdraw, show_daily_limits)
from auth import login, change_password
from history import show_history
from storage import load_data, save_data
from transfers import transfer


def show_menu(username):
    print("====================================")
    print("          PYTHON BANKING SYSTEM")
    print("====================================")
    print("Welcome, " + username + "!")
    print("")
    print("1. View Account Information")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Transaction History")
    print("7. Daily Limits")
    print("8. Change Password")
    print("9. Logout")
    print("0. Exit")
    print("====================================")


def session(data, username):
    
    user = data["users"][username]
    reset_daily_if_new_day(user)
    save_data(data)

    while True:
        show_menu(username)
        choice = input("Select an option: ").strip()

        if choice == "1":
            show_account_info(username, user)
        elif choice == "2":
            show_balance(user)
        elif choice == "3":
            deposit(data, username)
        elif choice == "4":
            withdraw(data, username)
        elif choice == "5":
            transfer(data, username)
        elif choice == "6":
            show_history(user)
        elif choice == "7":
            show_daily_limits(user)
        elif choice == "8":
            change_password(data, username)
        elif choice == "9":
            print("Logged out.")
            return "logout"
        elif choice == "0":
            print("Goodbye!")
            return "exit"
        else:
            print("Invalid option. Please choose a number from the menu.")
        print("")


def main():
    data = load_data()
    while True:
        username = login(data)
        if username is None:           # istifadeci login ekraninda 0 yazdi
            print("Goodbye!")
            break
        result = session(data, username)
        if result == "exit":
            break


try:
    main()
except (KeyboardInterrupt, EOFError):
    print("")
    print("Program closed.")
