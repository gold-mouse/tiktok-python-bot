from time import sleep
from flask import Flask, request, jsonify
from flask_cors import CORS

from constants import PORT
from chrome_actions import launch_driver, login, search
from model import driver_model

app = Flask(__name__, static_folder="views", static_url_path="")
CORS(app)

@app.before_request
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

@app.route("/api/user-login", methods=["POST"])
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
    
@app.route("/api/get-users", methods=["GET"])
def get_users():
    return jsonify({ "status": True, "data": [{ "id": i + 1, "username": username } for i, username in enumerate(driver_model.get_usernames_from_driverkyes())] }), 200

@app.route("/api/keyword-search", methods=["GET"])
def keyword_search():
    try:
        keyword = request.args.get("keyword", "")
        username = request.args.get("username", "")

        if keyword == "" or username == "":
            return jsonify({ "status": False, "message": "Missing payload" })

        res = search(username=username, keyword=keyword)

        return jsonify(res), 200
    except Exception as e:
        print(e)
        return jsonify({ "status": False, "message": "Something went wrong" })

@app.route("/api/close-driver", methods=["GET"])
def close_driver():
    username = request.args.get("username", "")
    
    driver = driver_model.get_driver(username)

    if driver != None:
        driver.quit()
        driver_model.remove_driver(username)

    return jsonify({"status": True, "message": f"Chrome closed for {username}"})

@app.route("/api/test", methods=["GET"])
def test():
    username = request.args.get("username", "")
    launch_driver(username)
    print(username, "-------->>>>good")
    return "test", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
