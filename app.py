from flask import Flask, request, jsonify
import requests
from constants import BASE_URL, API_KEY, fetch_weather
from auth import token_required, generate_token
import jwt
import datetime
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:8080'


app.config['SECRET_KEY'] = os.getenv("JWT_SECRET_KEY") 
@app.route("/")
def home():
    return "JWT Auth Weather App is Running"

@app.route("/login", methods=["POST"])
def login():
    # In real apps, you'd validate username/password
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    token = generate_token(user_id=username)
    return jsonify({"token": token})

@app.route("/getweather", methods=["GET"])
@token_required
def getweather():
    city = request.args.get("q")
    if not city:
        return jsonify({"error": "Please provide a city name using ?q=your_city"}), 400

    data, status, message = fetch_weather(city)
    if not data:
        return jsonify({"error": message}), status

    return jsonify(data)

@app.route("/postweather", methods=["POST"])
@token_required
def postweather():
    body = request.get_json()
    if not body or "city" not in body:
        return jsonify({"error": "City name is required in JSON body"}), 400

    city = body["city"]
    data, status, message = fetch_weather(city)
    if not data:
        return jsonify({"error": message}), status

    return jsonify(data)



if __name__=="__main__":
    app.run(debug=True)




# from flask import Flask,request,jsonify
# import requests
# from constants import BASE_URL, API_KEY, fetch_weather
# from auth import token_required

# app =Flask(__name__)
# app.config['SERVER_NAME'] = '127.0.0.1:8080'


# @app.route("/")
# def home():
#     return "App is successfully built :)"

# @app.route("/getweather", methods=["GET"])
# @token_required
# def getweather():
#     city = request.args.get("q")
#     if not city:
#         return jsonify({"error": "Please provide a city name using ?q=your_city"}), 400

#     data, status, message = fetch_weather(city)
#     if not data:
#         return jsonify({"error": message}), status

#     return jsonify(data)

# @app.route("/postweather", methods=["POST"])
# @token_required
# def postweather():
#     data = request.get_json()
#     if not data or "city" not in data:
#         return jsonify({"error": "No city name provided"}), 400

#     city = data["city"]
#     result, status, message = fetch_weather(city)
#     if not result:
#         return jsonify({"error": message}), status

#     return jsonify(result)

   


