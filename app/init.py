from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.auth_routes import auth_bp
from app.feedback_routes import feedback_bp
from config.firebase_config import *
from datetime import timedelta
import os
from config.sqlite_config import init_db

#create flask app
def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:8501"],) #enable CORS

    #load environment variables
    load_dotenv('Keys.env')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY #set JWT secret key
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"] #set JWT token location
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False #set JWT cookie csrf false
    app.config["JWT_TOKEN_HTTPONLY"] = True  #set JWT token httponly(most secure)
    app.config["JWT_COOKIE_SECURE"] = False #set JWT cookie secure (false for deveploment)
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"  #set JWT cookie samesite(most pratical)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15) #set JWT access token expiry time
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7) #set JWT refresh token expiry time(refresh resets access token expiry time)

    jwt = JWTManager(app) #initialise JWT manager
    init_db() #initial database
    
    #register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(feedback_bp, url_prefix="/feedback")

    return app