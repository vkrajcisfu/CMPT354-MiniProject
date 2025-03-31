import sqlite3

database = "library.db"

def connect_to_db():
    conn = sqlite3.connect(database)
    
    print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
    
    if conn:
        return conn
    else:
        print("Error opening database")
    
def disconnect_from_db(database):
    if database:
        database.commit()
        database.close()
        print("Closed database successfully")
