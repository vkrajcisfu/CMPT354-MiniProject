import sqlite3
from connect import *
from datetime import datetime

"""
User-interfacing functions live here. FlaskForms check if inputs are the correct type.
I have also done checks to make sure inputs fall within the restrictions of the database.
Example: This program will check if a User ID is valid (i.e. within the database) before doing any database modifications.

If an input is invalid, a ValueError is raised, and that is displayed to the user after submitting the form.
"""

today = datetime.today().strftime('%Y-%m-%d')
one_month_from_now = datetime.today()
one_month_from_now = one_month_from_now.replace(month = one_month_from_now.month + 1).strftime('%Y-%m-%d')

def find_item(query):
    db = connect_to_db()
    cur = db.cursor()
    
    cur.execute("""
                SELECT * FROM Item
                WHERE LOWER(title) LIKE ? OR LOWER(item_type) LIKE ?
                """, ('%' + query + '%', '%' + query + '%'))
    
    # get all rows matching the query
    result = cur.fetchall()
    
    # commit the db
    disconnect_from_db(db)
    
    print("Here are the items matching your query")
    return result


def borrow_item(uid, iid):
    db = connect_to_db()
    cur = db.cursor()
    
    # find if item exists in database
    cur.execute("""
                SELECT iid FROM ITEM 
                WHERE iid = ?
                """,(iid,))
    
    result = cur.fetchone()
    
    # check if item exists
    if result is None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You cannot borrow an item that does not exist")
    
    # find if user exists in database
    cur.execute("""
                SELECT uid FROM User 
                WHERE uid = ?
                """,(uid,))
    
    result = cur.fetchone()
    
    # check if user exists
    if result is None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You did not submit a valid User ID")
    
    cur.execute("""
                SELECT quantity FROM ITEM 
                WHERE iid = ?
                """,(iid,))
    
    quantity = cur.fetchone()
    
    if quantity:
        quantity = quantity[0]
    
        # check if item is available
        if quantity == 0:
            
            # commit the db
            disconnect_from_db(db)
            raise ValueError("This item is currently unavailable")
    
    # can proceed with borrowing the item
    
    # create record that item has been borrowed
    cur.execute("""
                INSERT INTO Record (uid, iid, borrow_date, return_date, fine_amount)
                VALUES (?, ?, ?, ?, ?)
                """, (uid, iid, today, one_month_from_now, 0))
    
    # decrement quantity
    cur.execute("""
                UPDATE Item 
                SET quantity = quantity - 1
                WHERE iid = ?
                """, (iid,))
    
    # select new quantity
    cur.execute("""
                SELECT quantity FROM ITEM 
                WHERE iid = ?
                """,(iid,))
    
    quantity = cur.fetchone()
    
    if quantity:
        quantity = quantity[0]
    
        # if quantity is 0, change item's status to unavailable
        if quantity == 0:
            cur.execute("""
                        UPDATE Item 
                        SET status = 'Unavailable'
                        WHERE iid = ?
                        """, (iid,))
    
    # commit the db
    disconnect_from_db(db)
    
    print("You have successfully borrowed this item")
    

def return_item(uid, iid):
    db = connect_to_db()
    cur = db.cursor()
    
    # find if item exists in database
    cur.execute("""
                SELECT iid FROM ITEM 
                WHERE iid = ?
                """,(iid,))
    
    result = cur.fetchone()
    
    # check if item exists
    if result is None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You cannot return an item that does not exist")
    
    # find if user exists in database
    cur.execute("""
                SELECT uid FROM User 
                WHERE uid = ?
                """,(uid,))
    
    result = cur.fetchone()
    
    # check if user exists
    if result is None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You did not submit a valid User ID")
    
    # get oldest rid from the given uid and iid
    # in case one user took out two of the same item
    cur.execute("""
                SELECT rid FROM Record
                WHERE uid = ? AND iid = ?
                ORDER BY borrow_date ASC
                LIMIT 1
                """, (uid, iid))
    
    rid = cur.fetchone()
    rid = rid[0]
    
    # delete record of item being borrowed
    cur.execute("""
                DELETE FROM Record
                WHERE rid = ?
                """, (rid,))
    
    # select quantity
    cur.execute("""
                SELECT quantity FROM ITEM 
                WHERE iid = ?
                """,(iid,))
    
    quantity = cur.fetchone()
    
    if quantity:
        quantity = quantity[0]
    
        # if quantity is 0, change item's status to available
        if quantity == 0:
            cur.execute("""
                        UPDATE Item 
                        SET status = 'Available'
                        WHERE iid = ?
                        """, (iid,))
    
    # increment quantity of item now that it's back in stock
    cur.execute("""
                UPDATE Item 
                SET quantity = quantity + 1
                WHERE iid = ?
                """, (iid,))
    
    # commit the db
    disconnect_from_db(db)
    
    print("You have successfully returned this item")
    

def donate_item(title, item_type):
    db = connect_to_db()
    cur = db.cursor()
    
    # find if item exists in database already
    cur.execute("""
                SELECT iid, quantity FROM ITEM 
                WHERE LOWER(title) = LOWER(?) AND LOWER(item_type) = LOWER(?)
                """,(title, item_type))
    
    result = cur.fetchone()
    
    # item not in database, add it
    if result is None:
        cur.execute("""
                    INSERT INTO Item (title, item_type, status, added_date, quantity)
                    VALUES (?, ?, ?, ?, ?)
                    """, (title, item_type, "Available", today, 1))
        
    # item in database
    else:
        iid, quantity = result
        
        if quantity:
            quantity = quantity[0]
            
            # if item has 0 quantity, increment quantity and change status to Available
            if quantity == 0:
                cur.execute("""
                            UPDATE Item 
                            SET quantity = 1, status = 'Available'
                            WHERE iid = ?
                            """, (iid,))
            
            # if item has quantity >0, increment quantity
            else:
                cur.execute("""
                            UPDATE Item 
                            SET quantity = quantity + 1
                            WHERE iid = ?
                            """, (iid,))
    
    # commit the db
    disconnect_from_db(db)
    
    print("Thank you for donating this item")
    

def find_event(query):
    db = connect_to_db()
    cur = db.cursor()
    
    cur.execute("""
                SELECT * FROM Event
                WHERE LOWER(event_name) LIKE ? OR LOWER(event_type) LIKE ? OR LOWER(audience) LIKE ?
                """, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    
    # get all rows matching the query
    result = cur.fetchall()
    
    # commit the db
    disconnect_from_db(db)
    
    print("Here are the events matching your query")
    
    return result


def register_event(uid, eid):
    db = connect_to_db()
    cur = db.cursor()
    
    # find if user exists in database
    cur.execute("""
                SELECT uid FROM User 
                WHERE uid = ?
                """,(uid,))
    
    result = cur.fetchone()
    
    # check if user exists
    if result is None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You did not submit a valid User ID")
    
    # find if event exists in database
    cur.execute("""
                SELECT eid FROM Event
                WHERE eid = ?
                """,(eid,))
    
    result = cur.fetchone()
    
    # check if event exists
    if result is None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You did not submit a valid Event ID")
    
    # find if user has already registered for this event
    cur.execute("""
                SELECT uid, eid FROM RegisterFor
                WHERE uid = ? AND eid = ?
                """,(uid, eid,))
    
    result = cur.fetchone()
    
    # check if user has registered already
    if result is not None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You have already registered for this event")
    
    cur.execute("""
                INSERT INTO RegisterFor (uid, eid, register_date)
                VALUES (?, ?, ?)
                """, (uid, eid, today))
    
    # commit the db
    disconnect_from_db(db)
    
    print("You have successfully registered for the event")
    

def volunteer(uid, hours):
    db = connect_to_db()
    cur = db.cursor()
    
    # find if user exists in database
    cur.execute("""
                SELECT uid FROM User 
                WHERE uid = ?
                """,(uid,))
    
    result = cur.fetchone()
    
    # check if user exists
    if result is None:
        
        # commit the db
        disconnect_from_db(db)
        raise ValueError("You did not submit a valid User ID")
    
    # see if user is a volunteer already
    cur.execute("""
                SELECT vid FROM Volunteer 
                WHERE uid = ?
                """,(uid,))
    
    result = cur.fetchone()
    
    # if volunteer not found, register as new
    if result is None:
        cur.execute("""
                    INSERT INTO Volunteer (uid, total_hours, start_date)
                    VALUES (?, ?, ?)
                    """, (uid, hours, today))
        
    # volunteer already in database, add additional hours volunteered
    else:
        vid = result[0]
        
        cur.execute("""
                    UPDATE Volunteer 
                    SET total_hours = total_hours + ?
                    WHERE vid = ?
                    """, (hours, vid))
    
    # commit db
    disconnect_from_db(db)
    
    print("Thank you for volunteering")

def ask_help():
    db = connect_to_db()
    cur = db.cursor()
    
    cur.execute("""
                SELECT name, occupation, email, phone_number FROM Personnel
                WHERE occupation = 'Librarian' OR occupation = 'Assistant Librarian'
                """)
    
    result = cur.fetchall()
    
    # commit the db
    disconnect_from_db(db)
    
    print("Here is who you can contact for help")
    return result

def fetch_all_data():
    db = connect_to_db()
    
    # converts extracted plain tuples to a row object
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # table names in library.db
    tables = ["User", "Item", "Record", "Event", "Personnel", "RegisterFor", "Volunteer"]
    # initialize empty dictionary for table:data pairing
    data = {}

    # for each table, selects all data and populates the data dictionary
    for table in tables:
        try:
            cur.execute(f"SELECT * FROM {table}")
            data[table] = cur.fetchall()
        except sqlite3.Error:
            data[table] = []

    disconnect_from_db(db)
    return data