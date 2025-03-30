from connect import *

def initialize_tables(database):
    cursor = database.cursor()
    
    # sql statements for creating table stored at sql\create_tables.sql
    with open("sql\\create_tables.sql", "r") as f:
        create_table_statements = f.read()
    
    statements = create_table_statements.split(';')
    
    # cursor executes each statement one at a time
    for statement in statements:
        cursor.execute(statement)
    
    database.commit()
    
    print("Tables initialized successfully")
    
    return

def populate_initial_data(database):
    cursor = database.cursor()
    
    # sql statements for inserting data stored at sql\insert_statements.sql
    with open("sql\\insert_statements.sql", "r") as f:
        insert_statements = f.read()
    
    statements = insert_statements.split(';')
    
    # cursor executes each statement one at a time
    for statement in statements:
        cursor.execute(statement)
    
    database.commit()
    
    print("Data populated successfully")
    
    return 