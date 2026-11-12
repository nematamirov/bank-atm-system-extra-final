from storage import save_data
from utils import now_text, hash_password, check_password

HARD_LIMIT = 6        # 6 sehv -> kart bloklanir


def password_is_strong(password):
    if len(password) < 8:
        return False
    has_upper = False
    has_lower = False
    has_digit = False
    for ch in password:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
    return has_upper and has_lower and has_digit


def wrong_password(user):
    user["failed_attempts"] = user["failed_attempts"] + 1
    count = user["failed_attempts"]
    print("Incorrect password. Attempt: " + str(count) + "/" + str(HARD_LIMIT))

    if count >= HARD_LIMIT:
        user["blocked"] = True
        print("Maximum login attempts exceeded.")
        print("Your card has been blocked.")
        print("Please contact the bank administrator.")


def login(data):
    while True:
        username = input("Username (0 to exit): ").strip()
        if username == "0":
            return None

        if username not in data["users"]:
            print("Invalid username or password.")
            continue

        user = data["users"][username]

        if user["blocked"]:
            print("Your card has been blocked.")
            print("Please contact the bank administrator.")
            continue

        password = input("Password: ")
        if check_password(password, user["password_hash"]):
            user["failed_attempts"] = 0        # ugurlu giris sayaci sifirlayir
            user["last_login"] = now_text()
            save_data(data)
            return username

        wrong_password(user)
        save_data(data)                        # sayac fayla yazilir


def change_password(data, username):
    user = data["users"][username]

    old = input("Current password: ")
    if not check_password(old, user["password_hash"]):
        print("Wrong current password.")
        return

    new = input("New password: ")
    if not password_is_strong(new):
        print("Password must have at least 8 characters, one uppercase letter,")
        print("one lowercase letter and one digit.")
        return

    if check_password(new, user["password_hash"]):
        print("New password must be different from the old password.")
        return

    again = input("Repeat new password: ")
    if again != new:
        print("Passwords do not match.")
        return

    user["password_hash"] = hash_password(new)
    save_data(data)
    print("Password changed successfully.")