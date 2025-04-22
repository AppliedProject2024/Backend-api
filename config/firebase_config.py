import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import os
import json

#load environment variables
load_dotenv('Keys.env')

#firebase API key
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

def initialise_firebase():
    firebase_key_path = os.getenv('FIREBASE_KEY_PATH')
    firebase_key_json = os.getenv('FIREBASE_KEY_JSON')
    
    #if running in a cloud environment with JSON in env var
    if firebase_key_json:
        try:
            service_account_info = json.loads(firebase_key_json)
            cred = credentials.Certificate(service_account_info)
        except json.JSONDecodeError:
            print("Error: FIREBASE_KEY_JSON environment variable contains invalid JSON")
            raise
    #if using a local file path
    elif firebase_key_path and os.path.exists(firebase_key_path):
        cred = credentials.Certificate(firebase_key_path)
    else:
        print("Error: No valid Firebase credentials found")
        raise ValueError("Firebase credentials not provided")
    
    #initialise Firebase app
    firebase_admin.initialize_app(cred)

#initialise Firebase when the module is imported
initialise_firebase()