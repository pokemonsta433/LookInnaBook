import psycopg2
from datetime import datetime

# setup -- could do this more securely with less hardcoded stuff but this should in theory be run on a secured server anyways
user_name = 'postgres'
password = 'pass'
hostname = 'localhost'
port = '5432'
db_name = 'Final_Project'
conn = psycopg2.connect(dbname=db_name, user=user_name, password=password,
        host=hostname, port=port) # should usually require SSL but I don't have an SSL setup for this database

cur = conn.cursor()

# cur.execute("select * from book")
# cur.fetchall()
import hashlib

# login loop
while(1):
    print("hello, please log in")
    email = input("Email: ")
    passHash = hashlib.sha256(input("Password: ").encode()) # should use getpass but I'm running on a jupyter notebook because postgres is on my windows machine so it doesn't too much matter right now

    print (passHash.hexdigest())
    cur.execute("select passwd from owners where email='" + email +"';")

    try:
        if not (passHash.hexdigest() == cur.fetchall()[0][0]):
            print ("owners is not registered or the password you entered was invalid")
        else:
            print ("logged you in!")
            break
    except:
        print("owners is not registered or the password you entered was invalid")

while(1):
    # now that we are logged in we can store user data
    print("adding book:")
    ISBN = input("ISBN: ")
    author = input("author: ")
    title = input("title: ")
    Publisher = input("Publisher: ")
    price = input("price: ")
    qty = input("qty: ")
    genre = input("genre: ")
    pages = input("pages: ")
    Publisher_royalties = input("Publisher_royalties: ")


    cur.execute("insert into book VALUES ( " + ISBN + ",'" + author + "','" + title + "','" + Publisher + "'," + price + "," + qty + ",'" + genre + "'," + pages + "," + Publisher_royalties + ");")

    if input("do you want to add another book? Y/n") == "n":
        break

conn.commit()
conn.close()
