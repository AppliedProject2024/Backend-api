from flask import Blueprint, request, jsonify
import requests
import os
from firebase_admin import auth
from app.firebase_config import FIREBASE_API_KEY

#auth blueprint
auth_bp = Blueprint("auth_bp", __name__)

#login route
@auth_bp.route("/login", methods=["POST"])
def login():
    #get email and password from request
    data = request.json
    email, password = data["email"], data["password"]

    #send request to firebase auth REST API
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    #send request
    response = requests.post(url, json=payload)

    #check if request was successful
    if response.status_code == 200:
        #get user data
        user_data = response.json()
        #get user by email
        user = auth.get_user_by_email(email)
        #check if email is verified
        if not user.email_verified:
            return jsonify({"error": "Email not verified"}), 403
        
        #return user data if vaild
        return jsonify({"email": email, "idToken": user_data["idToken"]}), 200
    #return error if request was not successful
    else:
        return jsonify({"error": "Invalid email or password"}), 403