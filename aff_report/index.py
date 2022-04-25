import json
from flask import Flask, request
from flask_cors import CORS
from main.validation import check_login, set_token, check_token
from main.report import sub_start, geo_start
from main.controller import create_user, add_api, delete_api, show_api
from main.responser import pull_response

accounts = "data/accounts.txt"
app = Flask(__name__)
CORS(app)

print("Test branch")

@app.route('/sub_report', methods=(['POST']))
def affstat():
    'do report by aff_sub if received token and username == token and username in DB'
    try:
        postdata = request.json
        print(postdata)
        token = postdata["token"]
        username = postdata["username"]
        date_from = postdata["dateFrom"]
        date_to = postdata["dateTo"]
        if check_token(username, token):
            f = open(accounts, "r")
            text = f.read()
            f.close()
            account = json.loads(text)
            API_LIST = account[username]["api_list"]
            return sub_start(date_from, date_to, API_LIST)
        else:
            return pull_response(False,0,"Permission denied")
    except:
        return pull_response(False,0,"Bad request (affstat)")


@app.route('/geo_report', methods=(['POST']))
def geostat():
    'do report by geo if received token and username == token and username in DB'
    try:
        postdata = request.json
        print(postdata)
        token = postdata["token"]
        username = postdata["username"]
        date_from = postdata["dateFrom"]
        date_to = postdata["dateTo"]
        if check_token(username, token):
            f = open(accounts, "r")
            text = f.read()
            f.close()
            account = json.loads(text)
            API_LIST = account[username]["api_list"]
            return geo_start(date_from, date_to, API_LIST)
        else:
            return pull_response(False,0,"Permission denied")
    except:
        return pull_response(False,0,"Bad request (geostat)")


@app.route("/login", methods=(['POST']))
def do_login():
    'login and set token if username and password valid'
    try:
        postdata = request.json
        print(postdata)
        username = postdata["username"]
        password = postdata["password"]
        token = check_login(username, password)
        if token:
            return pull_response(True,1,{"token": token})
        else:
            return pull_response(False,0,"Permission denied")
    except:
       return pull_response(False,0,"Bad request (login)")


@app.route('/register', methods=(['POST']))
def register():
    'create new user'
    try:
        postdata = request.json
        print(postdata)
        username = postdata["username"]
        password = postdata["password"]
        invite = postdata["invite"]
        new_user = create_user(username,password,invite)
        return new_user
    except:
        return pull_response(False,0,"Bad request (register)")


@app.route('/add_api', methods=(['POST']))
def create_api():
    'add new API key into account'
    try:
        postdata = request.json
        print(postdata)
        token = postdata["token"]
        username = postdata["username"]
        api_name = postdata["apiName"]
        api_key = postdata["apiKey"]
        if check_token(username, token):
            return add_api(username,api_name,api_key)
    except:
        return pull_response(False,0,"Bad request (create_api)")


@app.route('/delete_api', methods=(['POST']))
def del_api():
    'delete API from account'
    try:
        postdata = request.json
        print(postdata)
        token = postdata["token"]
        username = postdata["username"]
        api_name = postdata["apiName"]
        if check_token(username, token):
            response = delete_api(username,api_name)
        return response
    except:
        return pull_response(False,0,"Bad request (del_api)")


@app.route('/show_api', methods=(['POST']))
def check_api():
    'show all API keys in account'
    try:
        postdata = request.json
        print(postdata)
        token = postdata["token"]
        username = postdata["username"]
        if check_token(username, token):
            response = show_api(username)
        return response
    except:
        return pull_response(False,0,"Bad request (check_api)")




while True:
    try:
        app.run()
    except:
        print("Connection lost")