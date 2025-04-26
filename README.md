# StudyBuddy-AI Backend API
This repo contains the codebase for the Flask API Backend of StudyBuddy-AI. Here you will find the main inner working of the system including the key technology behind the application Retrieval augmented generation. The Flask API handles all proccesses within the application including authenication, document processing, AI interactions and handling user feedback. The endpoints or routes for this applications can be found in the "routes" directory, with the main funtionality located in the "app" directory. The config directory showcases the configuration of Firebase authenication, ChromaDB, SQLite and OpenAI API.

## Endpoints: 
1. Authentication Endpoints
  - /auth/login: Authenticates users and issues access and refresh tokens
  - /auth/register: Creates new user accounts
  - /auth/check-session: Verifies active user sessions
2. Document Management endpoints
  - /file/upload: Processes and stores uploaded PDF documents
  - /file/extract: Retrieves a list of users documents
  - /file/delete: Removes all document chunks associated with a specific
from the ChromaDB database
3. Query Endpoints
  - /ask/query: Handles general questions about documents
  - /ask/summary: Generates customised summaries of document contents
  - /ask/mcq: Creates multiple choice questions based on documents
4. Feedback Endpoints
  - /feedback/submit: Collect user feedback on system functions and
  stores it in a SQLite database

## Cloning and running locally
If you wish to clone this repository for local hosting there is some steps involved in order to achieve this.
### Python version and package requirments.
This application was developed using Python version 3.12.10 with a number of added packages you will be required to install these packages in order to run the application. These pacakges are alreay outline in the 'requirments.txt and can be installed using 'pip install -r requirements.txt'
### Envoirment Variables
This application uses a number of envoirment variables, examples of the variables used can be seen in 'Example.env' these you will need to fill these in as follows
- ENVIRONMENT: This should be set to 'development' for local hosting
- FIREBASE_API_KEY and FIREBASE_KEY_PATH: These keys can be generated for the Firebase console you will be required to create a new project within Firebase and generate the key and JSON credentials file from this project this can be done at the [Firebase website](https://firebase.google.com)
- EMAIL variables: To get these environment variables you need to create an email account and get the SMTP settings.
  - EMAIL_HOST is the mail server address 
  - EMAIL_PORT is the server port
  - EMAIL_USER is your email address
  - EMAIL_PASS is your email account password or app-specific password
- JWT_SECRET_KEY: This is a random secret string you can create yourself. It is used in orderto verify login tokens securely it is easiest to use a generator to create on [here](https://jwtsecret.com/generate)
- OPEN_API_KEY: This is provided by OpenAI. You will need to [sign into your OpenAI account](https://openai.com) going to the API section and creating a new secret key.
- DATABASE and CHROMA_PATH: These are simply the location of which the ChromaDB and SQLite database will be located with in the projects directory.
