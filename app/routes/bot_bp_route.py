from time import sleep
from flask import Blueprint, jsonify, request
from app.model import driver_model
from app.services.chrome_auto_service import launch_driver, login, search

bot_bp = Blueprint('bot', __name__)

@bot_bp.before_request
def before_request_middleware():
    open_chrome_endpoints = [
        "user_login",
        "keyword_search",
    ]
    if request.endpoint in open_chrome_endpoints:
        username = request.args.get("username", "")
        if request.method == "POST":
            body = request.get_json()
            username = body.get("username", "")

        if username == "":
            return jsonify({ "status": False, "message": "Missing payload" })
        
        isExist = driver_model.check_driver(username)

        if not isExist:
            driver = launch_driver(username)
            driver_model.set_driver(username, driver)
            sleep(7)

@bot_bp.route("/user-login", methods=["POST"])
def user_login():
    try:
        body = request.get_json()
        username = body.get("username", "")
        password = body.get("password", "")

        if username == "" or password == "":
            return jsonify({ "status": False, "message": "Missing payload" })

        res = login(username, password)
            
        return jsonify(res), 200
    except Exception as e:
        print(e)
        return jsonify({ "status": False, "message": "Something went wrong" })
    
@bot_bp.route("/get-users", methods=["GET"])
def get_users():
    return jsonify({ "status": True, "data": [{ "id": i + 1, "username": username } for i, username in enumerate(driver_model.get_usernames_from_driverkyes())] }), 200

@bot_bp.route("/keyword-search", methods=["GET"])
def keyword_search():
    try:
        keyword = request.args.get("keyword", "")
        username = request.args.get("username", "")
        comment = request.args.get("comment", "Wonderful, I like it")

        if keyword == "" or username == "":
            return jsonify({ "status": False, "message": "Missing payload" })

        res = search(username=username, keyword=keyword, comment=comment)

        return jsonify(res), 200
    except Exception as e:
        print(e)
        return jsonify({ "status": False, "message": "Something went wrong" })

@bot_bp.route("/close-driver", methods=["GET"])
def close_driver():
    username = request.args.get("username", "")
    
    driver_model.remove_driver(username)

    return jsonify({"status": True, "message": f"Chrome closed for {username}"})

@bot_bp.route("/test", methods=["GET"])
def test():
    username = request.args.get("username", "")
    launch_driver(username)
    print(username, "-------->>>>good")
    return "test", 200
