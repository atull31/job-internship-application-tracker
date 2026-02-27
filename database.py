import sqlite3 ##helps to interact with SQLite databases
def create_conn():
    conn = sqlite3.connect('applications.db') #this file automatically gets created
    return conn #and a connection is created between our code and database
def create_table():
    conn = create_conn() #function calling
    cur = conn.cursor() #cursor executes sql commands
    ## creates table of all the given columns if the table doesn't exist already
    cur.execute("""
                CREATE TABLE IF NOT EXISTS applications
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    company
                    TEXT,
                    role
                    TEXT,
                    location
                    TEXT,
                    link
                    TEXT,
                    source
                    TEXT,
                    status
                    TEXT,
                    notes
                    TEXT,
                    date_applied
                    TEXT
                )
                """)
    conn.commit()
    conn.close()
if __name__ == '__main__':
    create_table()
    print("Database and Table created successfully")
