from flask import Flask,request,jsonify
import requests

app =Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:8080'

API_KEY='7bb6ca1a8cb9a599184fb0c16436341c'

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/")
def home():
    return "App is successfully built :)"

@app.route("/getweather", methods=["GET"])
def getweather():
    city = request.args.get("q")  # Get city from query parameter (?q=cityname)

    if not city:
        return jsonify({"error": "Please provide a city name using ?q=your_city"}), 400

    # Request weather data from OpenWeatherMap
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    

    # Handle city not found
    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch data from OpenWeatherMap (Status Code: {response.status_code})"}), 500

    data = response.json()
    print(type(data))
    if data.get("cod") != 200:
        return jsonify({"error": f"City '{city}' not found!"}), 404
    # Filter required data
    filtered_data = {
    "city": data.get("name", "Unknown City"),
    "temperature": data.get("main", {}).get("temp", "N/A"),
    "humidity": data.get("main", {}).get("humidity", "N/A"),
    "wind": data.get("wind", {}).get("speed", "N/A"),
    }
    return jsonify(filtered_data)

@app.route('/postweather', methods=['POST'])
def postweather():
    # Parse JSON data from the request body
    data = request.get_json()

    if not data or "city" not in data:
        return jsonify({"error": "No city name provided"}), 400

    city_name = data["city"]

    # Fetch weather data from OpenWeatherMap API
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    weather_data = response.json()

    if response.status_code != 200:
        return jsonify({"error": weather_data.get("message", "Failed to fetch weather data")}), response.status_code

    # Extract relevant weather information
    result = {
        "city": weather_data.get("name", "N/A"),
        "temperature": weather_data["main"].get("temp", "N/A"),
        "humidity": weather_data["main"].get("humidity", "N/A"),
        "wind": weather_data["wind"].get("speed", "N/A")
    }

    return jsonify(result)


if __name__=="__main__":
    app.run(debug=True)
   






# def getweather(city):  # ✅ Use function parameter instead of request.args.get()
    
#     if not city:
#         return jsonify({"error": "Please provide a city name"}), 400
    
#     # Send request to OpenWeatherMap API
#     params = {"q": city, "appid": api_key, "units": "metric"}
#     response = requests.get(BASE_URL, params=params)
#     data = response.json()

#     # Check if city is found
#     if data.get("cod") != 200:
#         return jsonify({"error": f"City '{city}' not found!"}), 404

#     # Extract relevant data
#     filtered_data = {
#         "city": data["name"],
#         "temperature": data["main"]["temp"],
#         "humidity": data["main"]["humidity"],
#         "wind_speed": data["wind"]["speed"],
#         "description": data["weather"][0]["description"]
#     }

#     return jsonify(filtered_data)
