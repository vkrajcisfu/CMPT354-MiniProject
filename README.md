# CMPT354-MiniProject
Library database mini-project for CMPT 354 with Huang Pan and Victor Krajci

Requires Flask to be installed
Requires flask-wtf wtforms to be installed

Run the code in main.py to generate the database 'library.db'

The database is generated from an initial list of CREATE TABLE statements in sql\create_table.sql

The data is populated from an initial list of INSERT INTO statements in sql\insert_statements.sql

While the program is running, the database contents are displayed on a Flask server at http://127.0.0.1:5000

A navigation bar at the top allows the user to interact with the database.

There is a home page, a View Database page which allows you to view the up-to-date database in entirety,
and an additional eight pages for the user to interact with the database.

The user can:

View the library database
Search for (find) an item in the library
Borrow an item from the library
Return an item to the library
Donate an item to the library
Search for (find) events at the library
Register for events at the library
Volunteer for the library
Ask for help from a librarian (returns contact information)

All of the forms on the webpage guarantee that the inputs are valid (well formed, and within the database).
Otherwise, a ValueError is raised and displayed to the user after submitting the form.

For the flask portion, I used this recommended tutorial from the assignment page as a resource for creating the webpage: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

