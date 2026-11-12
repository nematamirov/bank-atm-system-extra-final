
import json
import os
from utils import today_text, hash_password

# Faylin yeri: layihe qovlugundaki data/bank_data.json
FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(FOLDER, "bank_data.json")

# (istifadeci adi, sifre, hesab nomresi, acilis balansi qepikle)
DEFAULT_USERS = [
    ("user01", "Test@123", "10010001", 250000),
    ("user02", "Test@456", "10010002", 150000),
    ("user03", "Test@789", "10010003", 300000),
]


def create_user(password, account_number, balance):
  
    user = {
        "password_hash": hash_password(password),
        "account_number": account_number,
        "balance": balance,
        "blocked": False,
        "failed_attempts": 0,
        "lockout_until": 0,          # 0 = gozleme yoxdur
        "last_login": "",
        "last_transaction": "",
        "daily": {
            "date": today_text(),
            "deposit_total": 0,
            "withdraw_total": 0,
            "transfer_count": 0,
        },
        "history": [],
    }
    return user


def create_default_data():
    data = {"atm_cash": 500000, "next_id": 1, "users": {}}
    for item in DEFAULT_USERS:
        username = item[0]
        data["users"][username] = create_user(item[1], item[2], item[3])
    return data


def data_is_valid(data):
   
    if "atm_cash" not in data or "next_id" not in data or "users" not in data:
        return False
    if data["atm_cash"] < 0:
        return False
    needed = ["password_hash", "account_number", "balance", "blocked",
              "failed_attempts", "lockout_until", "daily", "history"]
    for username in data["users"]:
        user = data["users"][username]
        for key in needed:
            if key not in user:
                return False
    return True


def save_data(data):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    file = open(DATA_FILE, "w", encoding="utf-8")
    json.dump(data, file, indent=4)
    file.close()


def load_data():
    
    try:
        file = open(DATA_FILE, "r", encoding="utf-8")
        data = json.load(file)
        file.close()
        if data_is_valid(data):
            return data
        print("Data file is invalid. Creating default data.")
    except FileNotFoundError:
        pass                          # ilk isleme: fayl yoxdur
    except (json.JSONDecodeError, TypeError, KeyError):
        print("Data file is damaged. Creating default data.")

    data = create_default_data()
    save_data(data)
    return data
