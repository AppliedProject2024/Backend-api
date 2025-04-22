import sqlite3
import os

#create a database file named feedback.db
DATABASE = os.getenv('DATABASE', 'feedback.db')

#connect to the database
def db_connect():
    #check if the database file exists
    db_dir = os.path.dirname(DATABASE)

    #if the directory does not exist create it
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    #connect to the database
    connect = sqlite3.connect(DATABASE)
    #return rows as dictionaries
    connect.row_factory = sqlite3.Row
    #return connection
    return connect

def init_db():
    #connect to the database
    with db_connect() as connect:
        #create feedback table
        connect.execute(
            '''CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            feedback_type TEXT NOT NULL, 
            feedback TEXT NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
        )
        #commit changes
        connect.commit()