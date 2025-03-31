import sqlite3
from connect import *
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
one_month_from_now = today.replace(month = today.month + 1)

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
                """,(iid))
    
    result = cur.fetchone()
    
    # check if item exists
    if result is None:
        print("You cannot borrow an item that does not exist")
        
        # commit the db
        disconnect_from_db(db)
        return
    
    cur.execute("""
                SELECT quantity FROM ITEM 
                WHERE iid = ?
                """,(iid))
    
    quantity = cur.fetchone()
    
    # check if item is available
    if quantity == 0:
        print("This item is currently unavailable")
        # commit the db
        disconnect_from_db(db)
        return
    
    #can proceed with borrowing the item
    
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
                """, (iid))
    
    # select new quantity
    cur.execute("""
                SELECT quantity FROM ITEM 
                WHERE iid = ?
                """,(iid))
    
    quantity = cur.fetchone()
    
    # if quantity is 0, change item's status to unavailable
    if quantity == 0:
        cur.execute("""
                    UPDATE Item 
                    SET status = 'Unavailable'
                    WHERE iid = ?
                    """, (iid))
    
    # commit the db
    disconnect_from_db(db)
    
    print("You have successfully borrowed this item")
    

def return_item(uid, iid):
    db = connect_to_db()
    cur = db.cursor()
    
    # delete record of item being borrowed
    cur.execute("""
                DELETE FROM Record
                WHERE uid = ? AND iid = ?
                """, (uid, iid))
    
    # increment quantity of item now that it's back in stock
    cur.execute("""
                UPDATE Item 
                SET quantity = quantity + 1
                WHERE iid = ?
                """, (iid))
    
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
        
        # if item has 0 quantity, increment quantity and change status to Available
        if quantity == 0:
            cur.execute("""
                        UPDATE Item 
                        SET quantity = 1, status = 'Available'
                        WHERE iid = ?
                        """, (iid))
        
        # if item has quantity >0, increment quantity
        else:
            cur.execute("""
                        UPDATE Item 
                        SET quantity = quantity + 1
                        WHERE iid = ?
                        """, (iid))
    
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
    
    # see if user is a volunteer already
    cur.execute("""
                SELECT uid FROM Volunteer 
                WHERE uid = ?
                """,(uid))
    
    result = cur.fetchone()
    
    # if volunteer not found, register as new
    if result is None:
        cur.execute("""
                    INSERT INTO Volunteer (uid, total_hours, start_date)
                    VALUES (?, ?, ?)
                    """, (uid, 0, today))
        
    # volunteer already in database, add additional hours volunteered
    else:
        cur.execute("""
                    SELECT total_hours FROM Volunteer 
                    WHERE uid = ?
                    """,(uid))
        
        result = cur.fetchone()
        
        cur.execute("""
                    UPDATE Volunteer 
                    SET total_hours = total hours + ?
                    WHERE uid = ?
                    """, (hours, uid))
    
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
