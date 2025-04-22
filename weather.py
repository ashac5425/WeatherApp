from flask import jsonify
from jose import jwt
import requests
import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = ["RS256"]

def verify_token(token):
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if not rsa_key:
        raise Exception("RSA key not found")
    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=API_AUDIENCE,
        issuer=f"https://{AUTH0_DOMAIN}/"
    )
    return payload

def get_weather(token, city):
    try:
        verify_token(token)
        # Replace with actual weather fetching logic
        return jsonify({"city": city, "weather": "Sunny", "temperature": "25°C"})
    except Exception as e:
        return jsonify({"error": str(e)}), 401

def post_weather(token, data):
    try:
        verify_token(token)
        # Replace with actual logic to store weather data
        return jsonify({"message": f"Weather data for {data['city']} saved successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 401
