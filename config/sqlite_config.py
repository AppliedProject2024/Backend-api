import sqlite3

#create a database file named feedback.db
DATABASE = 'feedback.db'

#connect to the database
def db_connect():
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