from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
from weather import get_weather, post_weather

load_dotenv()

app = Flask(__name__)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")

def get_access_token():
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": API_AUDIENCE,
        "grant_type": "client_credentials"
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getweather', methods=['GET'])
def get_weather_route():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    token = get_access_token()
    return get_weather(token, city)

@app.route('/postweather', methods=['POST'])
def post_weather_route():
    data = request.get_json()
    if not data or 'city' not in data or 'weather' not in data:
        return jsonify({"error": "City and weather data are required"}), 400
    token = get_access_token()
    return post_weather(token, data)


if __name__=="__main__":
    app.run(debug=True)
