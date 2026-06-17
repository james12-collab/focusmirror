import json
import os
import hashlib
import secrets

ACCOUNTS_FILE = 'accounts.json'

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return {}
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def signup(username, password):
    username = username.strip().lower()
    if len(username) < 2:
        return False, "Username must be at least 2 characters"
    if len(password) < 4:
        return False, "Password must be at least 4 characters"
    accounts = load_accounts()
    if username in accounts:
        return False, "Username already taken"
    hashed, salt = hash_password(password)
    accounts[username] = {
        "username": username,
        "display_name": username.capitalize(),
        "password_hash": hashed,
        "salt": salt
    }
    save_accounts(accounts)
    return True, username.capitalize()

def login(username, password):
    username = username.strip().lower()
    accounts = load_accounts()
    if username not in accounts:
        return False, "Account not found"
    acc = accounts[username]
    hashed, _ = hash_password(password, acc['salt'])
    if hashed != acc['password_hash']:
        return False, "Wrong password"
    return True, acc['display_name']