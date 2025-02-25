import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv('Keys.env')

#firebase api key and path
FIREBASE_API_PATH = os.getenv('FIREBASE_KEY_PATH')
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

#initialise firebase app
cred = credentials.Certificate(FIREBASE_API_PATH)
firebase_admin.initialize_app(cred)
