from initialize import *
from app import app

if __name__ == "__main__":
    
    # if file exists, don't re-initialize the database
    if os.path.isfile("library.db"):
        db = connect_to_db()
    # else create and initialize a new db
    else:
        db = connect_to_db()
        initialize_tables(db)
        populate_initial_data(db)
        
    disconnect_from_db(db)
        
    print("Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True)