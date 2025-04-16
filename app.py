from flask import Flask,request,jsonify
import requests
from constants import BASE_URL, API_KEY, fetch_weather
from auth import token_required

app =Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:8080'


@app.route("/")
def home():
    return "App is successfully built :)"

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
    data = request.get_json()
    if not data or "city" not in data:
        return jsonify({"error": "No city name provided"}), 400

    city = data["city"]
    result, status, message = fetch_weather(city)
    if not result:
        return jsonify({"error": message}), status

    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)
   


