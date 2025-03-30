from initialize import *
from web import create_webpage
import os.path

# if file exists, don't re-initialize the database
if os.path.isfile("library.db"):
    db = connect_to_db()
else:
    db = connect_to_db()
    initialize_tables(db)
    populate_initial_data(db)

create_webpage()