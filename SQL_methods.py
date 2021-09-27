import psycopg2

# Project contains basic functions of Postgresql, using psycopg2 library

# Typing the specifics of the database
dbname = input("Write your database name please:")
username = input("Write your username please:")
password = input("Write your password please:")


# Function which shows whole database
def show_all():
    conn = psycopg2.connect(dbname=dbname, user=username, password=password)
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    list_of_clients = c.fetchall()
    for client in list_of_clients:
        print(client)
    conn.commit()
    conn.close()


# Adding person to table, to add more people use list
def add_person(firstname, lastname, email):
    conn = psycopg2.connect(dbname=dbname, user=username, password=password)
    c = conn.cursor()
    c.execute(f"INSERT INTO clients VALUES ('{firstname}','{lastname}','{email}')")
    conn.commit()
    conn.close()


# Deleting person from database
def delete_person(firstname_to_del, lastname_to_del):
    conn = psycopg2.connect(dbname=dbname, user=username, password=password)
    c = conn.cursor()
    c.execute(f"DELETE FROM clients WHERE first_name = '{firstname_to_del}' AND last_name = '{lastname_to_del}'")
    conn.commit()
    conn.close()


show_all()
