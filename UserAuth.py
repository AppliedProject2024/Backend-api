import firebase_admin
import requests
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import os

load_dotenv('Keys.env')

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

#initialize firebase app
def initFirebaseApp():
    #initialize firebase app if not already initialized
    if not firebase_admin._apps:
        #create a firebase app if not already created
        cred = credentials.Certificate(r".\firebase_credentials.json")
        #initialize firebase app
        firebase_admin.initialize_app(cred)