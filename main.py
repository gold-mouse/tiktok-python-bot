from flask import Flask, request, jsonify
from flask_cors import CORS

from constants import PORT
from chrome_actions import launch_driver, login, search, follow, favorite, leaveComment
from driver_model import driver_model

app = Flask(__name__, static_folder="views", static_url_path="")
CORS(app)

@app.route("/api/user-login", methods=["POST"])
def user_login():
    try:
        body = request.get_json()
        username = body.get("username", "")
        password = body.get("password", "")

        if username == "" or password == "":
            return "Missing payload", 400

        res = login(username, password)
            
        if res == None:
            return "Something went wrong", 500

        return jsonify(res), 200
    except Exception as e:
        print(e)
        return "Something went wrong", 500
    
@app.route("/api/get-users", methods=["GET"])
def get_users():
    return jsonify({ "status": True, "data": [{ "id": i + 1, "username": username } for i, username in enumerate(driver_model.get_keys())] }), 200

@app.route("/api/keyword-search", methods=["GET"])
def keyword_search():
    try:
        keyword = request.args.get("keyword", "")
        username = request.args.get("username", "")

        if keyword == "" or username == "":
            return "Missing payload", 400

        res = search(username=username, keyword=keyword)
            
        if res == None:
            return "Something went wrong", 500

        return jsonify(res), 200
    except Exception as e:
        print(e)
        return "Something went wrong", 500

@app.route("/api/follow-video", methods=["POST"])
def follow_video():
    try:
        body = request.get_json()
        username = body.get("username", "")
        link = body.get("link", "")

        if link == "" or username == "":
            return "Missing payload", 400

        res = follow(username=username, link=link)
            
        if res == None:
            return "Something went wrong", 500

        return jsonify(res), 200
    except Exception as e:
        print(e)
        return "Something went wrong", 500

@app.route("/api/save-video", methods=["POST"])
def save_video():
    try:
        body = request.get_json()
        username = body.get("username", "")
        link = body.get("link", "")

        if link == "" or username == "":
            return "Missing payload", 400

        res = favorite(username=username, link=link)
            
        if res == None:
            return "Something went wrong", 500

        return jsonify(res), 200
    except Exception as e:
        print(e)
        return "Something went wrong", 500

@app.route("/api/leave-comment", methods=["POST"])
def leave_comment():
    try:
        body = request.get_json()
        username = body.get("username", "")
        link = body.get("link", "")

        if link == "" or username == "":
            return "Missing payload", 400

        res = leaveComment(username=username, link=link)
            
        if res == None:
            return "Something went wrong", 500

        return jsonify(res), 200
    except Exception as e:
        print(e)
        return "Something went wrong", 500

@app.route("/api/open-driver", methods=["GET"])
def open_driver():
    username = request.args.get("username", "")

    if driver_model.get_driver(username) != None:
        return jsonify({"status": True, "message": f"Chrome already opened for {username}"})
        
    driver = launch_driver(username)
    
    driver_model.set_driver(username, driver)
    return jsonify({"status": True, "message": f"Chrome opened for {username}"})

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
