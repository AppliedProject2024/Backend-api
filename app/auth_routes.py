from flask import Blueprint, request, jsonify, make_response
import requests
import os
from firebase_admin import auth
from app.firebase_config import FIREBASE_API_KEY
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from flask_jwt_extended import (
create_access_token, 
create_refresh_token,
set_access_cookies, 
set_refresh_cookies, 
jwt_required,
get_jwt_identity
)


#auth blueprint
auth_bp = Blueprint("auth_bp", __name__)

#SMTP credentials
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

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
        
        #create JWT tokens
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        
        #return user data if vaild and set jwt
        resp = make_response(jsonify({"email": email}))
        set_access_cookies(resp, access_token) #store in cookie
        set_refresh_cookies(resp, refresh_token)#store in cookie
        return resp, 200
    #return error if request was not successful
    else:
        return jsonify({"error": "Invalid email or password"}), 403
    
#register route
@auth_bp.route("/register", methods=["POST"])
def register():
    #get email and password from request
    data = request.json
    email, password = data["email"], data["password"]
    
    #send request to firebase auth REST API
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    #send request
    response = requests.post(url, json=payload)

    #check if request was successful
    if response.status_code == 200:
        user_data = response.json()

        #send verification email
        try:
            user = auth.get_user_by_email(email)
            verification_link = auth.generate_email_verification_link(user.email)

            sendVerificationEmail(email, verification_link)

            return jsonify({"email": email, "idToken": user_data["idToken"]}), 200
        except Exception as e:
            return jsonify({"error": f"Error sending verification email: {str(e)}"}), 500
      
    else:
        return jsonify({"error": "Invalid email or password"}), 403

#send verification email
def sendVerificationEmail(email, verification_link):
    try:
        #set up emal message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = "Email Verification - IDontKnowMyDocument AI"

        #body
        body = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>Thank you for signing up to IDontKnowMyDocument AI!</p>
            <p>Please find below a link to verify your email address:</p>
            <a href="{verification_link}">Verify Email</a>
            <p>Thank you! We hope you enjoy using our Application!</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        #connect to SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()#secure connection
        server.login(EMAIL_USER, EMAIL_PASS)#login to email
        server.sendmail(EMAIL_USER, email, msg.as_string())#send email
        server.quit()#close connection

        return "Verification email sent successfully!"
    except Exception as e:
        return f"Error sending verification email: {str(e)}"
    

#refresh route
@auth_bp.route("/refresh", methods=["POST"])
#requir a refresh token so access token can be reset
@jwt_required(refresh=True)
def refresh():
    try:
        #get current user through refresh token
        current_user = get_jwt_identity()
        if current_user is None:
            return jsonify({"error": "User not found"}), 403
        #create new access token
        access_token = create_access_token(identity=current_user)

        #return new access token
        resp = make_response(jsonify({"message": "Token refreshed"}))
        set_access_cookies(resp, access_token)

        return resp, 200
    except Exception as e:
        return jsonify({"error": f"Error refreshing token: {str(e)}"}), 500
    
#test
@auth_bp.route("/test" , methods=["GET"])
@jwt_required()
def test():
    response = request.cookies
    response_token = response.get("refresh_token_cookie")
    print(f"refresh_token " + response_token)
    return jsonify({"message": "Test route"}), 200
