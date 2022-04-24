import json
import datetime
import hashlib
from .responser import pull_response


logins = "aff_report/data/login.txt"
accounts = "aff_report/data/accounts.txt"


def check_login(log, password):
    'if received username and password == same in DB, generate and return token'
    try:
        f = open(logins, "r")
        text = f.read()
        f.close()
        account = json.loads(text)
        if log in account.keys():
            if account[log]["login"] == log and account[log]["password"] == password:
                token = hashlib.md5((log + password + str(datetime.date.today())).encode("utf-8")).hexdigest().upper()
                set_token(log, token)
                print("Login Success")
                return token
        print("Login Fail")
        return False
    except:
        return pull_response(False,0,"Bad request (check login)")


def set_token(user, token):
    'set new token into user`s profile'
    try:
        f = open(accounts, "r")
        text = f.read()
        f.close()
        account = json.loads(text)
        account[user]["token"] = token
        account = json.dumps(account)

        f = open(accounts, "w")
        f.write(str(account))
        f.close()
    except:
        return pull_response(False,0,"Bad request (set token)")


def check_token(user, token):
    'return True if received token equal DB token'
    f = open(accounts, "r")
    text = f.read()
    f.close()
    account = json.loads(text)
    try:
        if account[user]["token"] == token:
            return True
        return False
    except:
        return False