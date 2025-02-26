from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.auth_routes import auth_bp
from app.firebase_config import *
from datetime import timedelta
import os

#create flask app
def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True) #enable CORS

    #load environment variables
    load_dotenv('Keys.env')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY #set JWT secret key
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"] #set JWT token location
    app.config["JWT_TOKEN_HTTPONLY"] = True  #set JWT token httponly
    app.config["JWT_COOKIE_SECURE"] = False #set JWT cookie secure 
    app.config["JWT_COOKIE_SAMESITE"] = "None"  #set JWT cookie samesite
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15) #set JWT access token expiry time
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7) #set JWT refresh token expiry time

    jwt = JWTManager(app) #initialise JWT manager
    
    #register auth blueprint
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app