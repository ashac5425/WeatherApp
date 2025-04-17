# # auth.py
# from flask import request, jsonify
# import os 
# from dotenv import load_dotenv

# load_dotenv()
# OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")

# # Simulated valid OAuth 2.0 token (replace with your actual token or validation logic)


# def token_required(func):
#     def wrapper(*args, **kwargs):
#         auth_header = request.headers.get("Authorization")

#         if not auth_header or not auth_header.startswith("Bearer "):
#             return jsonify({"error": "Missing or invalid Authorization header"}), 401

#         token = auth_header.split(" ")[1]
#         if token != OAUTH_TOKEN:
#             return jsonify({"error": "Invalid or expired token"}), 403

#         return func(*args, **kwargs)
#     wrapper.__name__ = func.__name__
#     return wrapper


# jwt_auth.py
import jwt
import datetime
from flask import request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET_KEY")

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def token_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = decoded["user_id"]  # Optional: attach user info to request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
