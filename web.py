from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
database = "library.db"

def fetch_all_data():
    conn = sqlite3.connect(database)
    
    # converts extracted plain tuples to a row object
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # table names in library.db
    tables = ["User", "Item", "Record", "Event", "Personnel", "RegisterFor", "Volunteer"]
    # initialize empty dictionary for table:data pairing
    data = {}

    # for each table, selects all data and populates the data dictionary
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            data[table] = cursor.fetchall()
        except sqlite3.Error:
            data[table] = []

    conn.close()
    return data

@app.route("/")
def index():
    data = fetch_all_data()
    return render_template("index.html", data=data)

def create_webpage():
    print("Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True)
