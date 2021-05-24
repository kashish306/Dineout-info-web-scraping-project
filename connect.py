import sqlite3

def connect(dbname):
    conn = sqlite3.connect(dbname)
    conn.execute("CREATE TABLE IF NOT EXISTS _DINEOUT_ (LOCATION TEXT, DETAILS TEXT, TOTALOFFERS TEXT, OFFERDETAILS TEXT)")
    print("Table created")
    conn.close()

def insert_into_table(dbname, values):
    conn = sqlite3.connect(dbname)
    insert_sql = ("INSERT INTO _DINEOUT_ (LOCATION, DETAILS, TOTALOFFERS, OFFERDETAILS) VALUES(?, ?, ?, ?)")
    conn.execute(insert_sql, values)
    conn.commit()
    conn.close()

def get_info(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM _DINEOUT_ ")
    table_data = cur.fetchall()

    for record in table_data:
        print(record)

    conn.close()
