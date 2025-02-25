from flask import Flask
from flask_cors import CORS
from app.auth_routes import auth_bp
from app.firebase_config import *

#create flask app
def create_app():
    app = Flask(__name__)
    CORS(app) #enable CORS
    
    #register auth blueprint
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app