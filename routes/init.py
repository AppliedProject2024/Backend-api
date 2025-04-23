from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.feedback_routes import feedback_bp
from routes.processing_routes import file_bp
from routes.query_routes import query_bp
from config.firebase_config import *
from datetime import timedelta
import os
from config.sqlite_config import init_db
import logging

#create flask app
def create_app():
    app = Flask(__name__)

    allowed_origins = [
        "http://localhost:8501", #local development
        "https://*.streamlit.app", #production domain
    ]

    CORS(app, supports_credentials=True, origins=allowed_origins) #enable CORS

    #load environment variables
    load_dotenv('Keys.env')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    #add logging configuration
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    #add request logging middleware
    @app.before_request
    def log_request_info():
        app.logger.info('Request: %s %s %s', request.method, request.path, request.data)
    
    @app.after_request
    def log_response_info(response):
        app.logger.info('Response: %s', response.status)
        return response
    
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY #set JWT secret key
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"] #set JWT token location
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False #set JWT cookie csrf false
    app.config["JWT_TOKEN_HTTPONLY"] = True  #set JWT token httponly(most secure)
    app.config["JWT_COOKIE_SECURE"] = True if os.getenv("ENVIRONMENT") == "production" else False #set JWT cookie secure(only for production)
    app.config["JWT_COOKIE_SAMESITE"] = "Strict" if os.getenv("ENVIRONMENT") == "production" else "Lax" #set JWT cookie samesite
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15) #set JWT access token expiry time
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7) #set JWT refresh token expiry time(refresh resets access token expiry time)

    jwt = JWTManager(app) #initialise JWT manager
    init_db() #initial database
    
    #register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(feedback_bp, url_prefix="/feedback")
    app.register_blueprint(file_bp, url_prefix="/file")
    app.register_blueprint(query_bp, url_prefix="/ask")

    return app