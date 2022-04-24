import json
import requests
from .responser import pull_response


logins = "aff_report/data/login.txt"
accounts = "aff_report/data/accounts.txt"
invites = "aff_report/data/invites.txt"


def create_user(username,password,invite):
    'add new user'
    try:
        f = open(invites, "r")
        invite_keys = f.read()
        f.close
        invite_keys = invite_keys.split("\n")
        if invite in invite_keys: #Check invite keys
            f = open(logins, "r")
            text = f.read()
            f.close()
            f = open(accounts, "r")
            accs = f.read()
            f.close()
            users = json.loads(text)
            account_list = json.loads(accs)
            if username in users.keys():
                return pull_response(False,0,"User already exist")
            else:
                users[username] = {"login":username,"password":password}
                users = json.dumps(users)
                f = open(logins, "w")
                f.write(str(users))
                f.close()
                account_list[username] = {"api_list":{},"token":"newtoken"}
                account_list = json.dumps(account_list)
                f = open(accounts, "w")
                f.write(str(account_list))
                f.close()
            invite_keys.remove(invite)
            f = open(invites, "w")
            for el in invite_keys:
                f.write(el + "\n")
            f.close
            return pull_response(True,1,"New user created")
        else:
            return pull_response(False,0,"Invalid invite key")
    except: return pull_response(False,0,"Bad request (create_user)")


def add_api(username,api_name,api_key):
    'add API key to current user'
    try:
        url = f"https://api.hasoffers.com/Apiv3/json?api_key={api_key}&Target=Affiliate_Affiliate&Method=findById"
        r = requests.get(url)
        api_check = json.loads(r.text)
        f = open(accounts, "r")
        text = f.read()
        f.close()
        users = json.loads(text)
        if api_name in users[username]["api_list"]:
            return pull_response(False,0,"API access with this username already exist")
        elif api_check["response"]["status"] != 1:
            return pull_response(False,0,"Invalid API key")
        elif api_key in users[username]["api_list"].values():
            return pull_response(False,0,"API key already exist")
        else:
            if len(api_key) == 64:
                users[username]["api_list"][api_name] = api_key
                users = json.dumps(users)
                f = open(accounts, "w")
                f.write(str(users))
                f.close()
            else:
                return pull_response(False,0,"Invalid API key")
        return pull_response(True,1,"API access successfully added")
    except: return pull_response(False,0,"Bad request (add_api)")


def delete_api(username,api_name):
    'delete API key from user`s list'
    try:
        f = open(accounts, "r")
        text = f.read()
        f.close()
        users = json.loads(text)
        if api_name in users[username]["api_list"]:
            users[username]["api_list"].pop(api_name)
            users = json.dumps(users)
            f = open(accounts, "w")
            f.write(str(users))
            f.close()
            return pull_response(True,1,"API successfully delete")
        else:
            return pull_response(False,0,"API not found")
    except: return pull_response(False,0,"Bad request (delete_api)")


def show_api(username):
    'return all current user`s API keys'
    try:
        f = open(accounts, "r")
        text = f.read()
        f.close()
        users = json.loads(text)
        return pull_response(True,1,users[username]["api_list"])
    except: pull_response(False,0,"Bad request (show_api)")