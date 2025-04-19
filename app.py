from flask import Flask, request, jsonify
from constants import BASE_URL, API_KEY, fetch_weather
from auth import token_required, generate_token
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:8080'


app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") 
@app.route("/")
def home():
    return " Weather App is Running"

@app.route("/login", methods=["POST"])
def login():
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

