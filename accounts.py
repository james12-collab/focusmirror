from firebase_db import create_account, verify_login, get_account, account_exists

def signup(username, password, age_group='unknown', ai_consent=False):
    return create_account(username, password, age_group, ai_consent)

def login(username, password):
    return verify_login(username, password)