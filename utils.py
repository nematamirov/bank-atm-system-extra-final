
import hashlib
import random
from datetime import datetime, date




def format_money(cents):
    
    manat = abs(cents) // 100
    qepik = abs(cents) % 100
    if qepik < 10:
        qepik_text = "0" + str(qepik)
    else:
        qepik_text = str(qepik)
    text = str(manat) + "." + qepik_text
    if cents < 0:
        text = "-" + text
    return text


def amount_to_cents(text):
   
    text = text.strip()
    text = text.replace(",", ".")      # 12,50 yazanlar ucun
    parts = text.split(".")            # '12.50' -> ['12', '50']

    if len(parts) > 2:                 # iki noqte olmaz: 1.2.3
        return None

    manat = parts[0]
    if len(parts) == 2:
        qepik = parts[1]
    else:
        qepik = ""

    if not manat.isdigit():            # herf, menfi isare, bos metn
        return None
    if qepik != "" and not qepik.isdigit():
        return None
    if len(qepik) > 2:                 # 2-den cox onluq olmaz
        return None

    if qepik == "":
        qepik = "00"
    elif len(qepik) == 1:
        qepik = qepik + "0"            # 5.5 -> 5.50

    cents = int(manat) * 100 + int(qepik)
    if cents <= 0:                     # sifir qebul olunmur
        return None
    return cents


def ask_amount(question):
 
    cents = amount_to_cents(input(question))
    if cents is None:
        print("Invalid amount. Enter a positive number with at most two decimal places.")
    return cents


def today_text():
    return str(date.today())           # meselen '2026-11-12'


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------- Sifre hash-i ----------
# Sifreni faylda aciq yazmiriq. Evezine 'duzen$hash' yazilir.
# salt = her istifadeci ucun tesaduf metn. Eyni sifre olsa bele hash ferqli cixir.

def make_salt():
    letters = "abcdefghijklmnopqrstuvwxyz0123456789"
    salt = ""
    for i in range(10):
        salt = salt + random.choice(letters)
    return salt


def hash_with_salt(password, salt):
    text = salt + password
    return hashlib.sha256(text.encode()).hexdigest()


def hash_password(password):
    """Yeni sifre ucun 'salt$hash' metni yaradir."""
    salt = make_salt()
    return salt + "$" + hash_with_salt(password, salt)


def check_password(password, saved):
    """Yazilan sifre saxlanan hash-e uygundurmu?"""
    parts = saved.split("$")
    salt = parts[0]
    saved_hash = parts[1]
    return hash_with_salt(password, salt) == saved_hash
