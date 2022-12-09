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

    cur.execute("select * from users where email='" + email +"';")

    try:
        if not (passHash.hexdigest() == cur.fetchall()[0][4]):
            print ("user is not registered or the password you entered was invalid")
        else:
            print ("logged you in!")
            break
    except:
        print("user is not registered or the password you entered was invalid")


# now that we are logged in we can store user data
cur.execute("select user_id from users where email='" + email +"';")
UID = cur.fetchall()[0][0]
_cart = [] # make them a new cart that they can store a bunch of books in

def printBooks(Query):
    cur.execute("select author, title, price, genre, qty, book_id from book " + Query + " order by sales DESC;")
    results = cur.fetchall()
    ind = 0

    while(1):
        for i in range(0, 10):
            if ind + i < len(results):
                print("---")
                current = results[ind+i]
                print (current[0] + "\t" + current[1] + "\t\t" + str(current[2]) + "$\nISBN:" + str(current[5]) + "\t" + current[3] + "\tin stock: " + str(current[4]) + "\n")

        print("type a book's ISBN to add it to your cart. Type 'exit' to stop viewing your query")
        if ind > 0:
            print ("to return to the previous page, type 'p'")
        if ind+1 < len(results):
            print ("to see the next page, type 'n'")
        userChoice = input()
        if userChoice == "p":
            ind += 10
        elif userChoice == "n":
            ind += 10
        elif userChoice == "exit" or userChoice == "quit" or userChoice == "q":
            return
        else:
            cur.execute("select author, title, price, genre, qty, book_id from book where book_id = '" + userChoice +"';")
            results = cur.fetchall()
            if len(results) > 0:
                qty = input("how many copies would you like to add to your cart?")
                _cart.append((results[0], qty))

def requestBooks(publisher, book):
    cur.execute("select email from publisher where pub_name='" + publisher + "';")
    print("\n=== server sending email to " + str(cur.fetchall()[0][0]) + " for more copies of ISBN " + str(book))
    return

def payRoyalties(publisher, amount):
    cur.execute("select bank_num from publisher where pub_name='" + publisher + "';")
    print("\n=== server sending " + str(amount) + "$ to bank acc. " + str(cur.fetchall()[0][0]))
    return

def orderCart(shipping_addr, billing_addr):
    theTime = datetime.now()
    # Place an order
    cur.execute("insert into orders VALUES ( '" + str(shipping_addr) + "','" + str(billing_addr) + "', 'processing', 'http://exampletrackinglink.com/order=" + str(hashlib.sha256(theTime.strftime("%D-%M:%S").encode()).hexdigest()[1:10]) + "','" + str(theTime.strftime("%Y-%m-%d %H:%M:%S-07")) +"', null, '" + str(UID) + "');")

    cur.execute("select order_num from orders where start_t='" + str(theTime.strftime("%Y-%m-%d %H:%M:%S-07")) + "';")
    order_number = cur.fetchall()[0][0]
    for book in _cart: # now go through and make the holds
        cur.execute("update book set qty= qty - " + str(book[1]) + " where book_id = " + str(book[0][5]) + ";")
        cur.execute("update book set sales= sales + " + str(book[1])+ " where book_id = " + str(book[0][5]) + ";")
        cur.execute("insert into holds VALUES (" + str(book[0][5]) + ", " + str(order_number) + ", " + str(book[1]) + ");")

        #NOTE: all this code is theoretically running on a server, not on the client's PC!
        cur.execute("select publisher, pb_royalty, price, qty from book where book_id='" + str(book[0][5]) + "';")
        result = cur.fetchall()[0] #points to a single tuple

        payRoyalties(result[0], (float(result[1]) * float(result[2]) * float(book[1])))

        # check if we need to restock
        if(result[3] < 10):
            requestBooks(result[0], book[0][5])

    conn.commit()
    _cart.clear()
    return

def checkout():
    print("== your cart ==")
    totalCost = 0
    for book in _cart:
        totalCost += (float(book[1]) * float(book[0][2]))
        print (book[0][1] + " x" + str(book[1]).ljust(35) + f'{(float(book[1]) * float(book[0][2])):.2f}' + "$")
    print("--------------------")
    print("total" + "\t\t\t\t" + f'{(float(totalCost)):.2f}' + "$")

    toBuy = input("do you want to place an order for these books? Y/n")
    if toBuy == "Y" or toBuy == "y":
        def_shipping_addr = input("would you like to use the default shipping address? Y/n")
        if def_shipping_addr == "Y" or def_shipping_addr == "y":
            cur.execute("select shipping_addr from users where user_id = '" + str(UID) +"'")
            shipping_addr = cur.fetchall()[0][0]
        else:
            shipping_addr = input("what shipping address would you like to use?")

        def_billing_addr = input("Is the billing address the same as the shipping address? Y/n")
        if def_billing_addr == "Y" or def_billing_addr == "y":
            billing_addr = shipping_addr
        else:
            billing_addr = input("what billing address would you like to use?")

        orderCart(shipping_addr, billing_addr)

    else: # don't want to buy books yet
        return

# weird place to define functions, I know, but this is where it makes the most sense
def browse():
    while(1):
        print("\n\n== browser view ==")
        print("what would you like to search by?\n1. author\n2. title\n3. Genre\n4. ISBN\n5. Popular")
        if(len(_cart) > 0):
            print ("6. Checkout")
        #no switch statements in my old python version
        searchType = input()
        if searchType == "1":
            searchString = "author"
        elif searchType == "2":
            searchString = "title"
        elif searchType == "3":
            searchString = "genre"
        elif searchType == "4":
            searchString = "book_id"
        elif searchType == "5":
            printBooks("")
            continue
        elif searchType == "6":
            checkout()
            return
        else:
            print ("returning to selection screen")
            return

        searchTerm = input("please enter your search term: ")
        printBooks("where " + searchString + " like '%" + searchTerm +"%'")

def orders():
    cur.execute("select * from orders where user_id='" + str(UID) +"' order by start_t ASC;")
    results = cur.fetchall()
    print("you have " + str(len(results)) + " orders")
    for res in results:
        print("Order Number: " + str(res[0]) +"\t status: " + str(res[3]) + "\t" + str(res[4]))
    # NOTE: could make it possible for you to see more info, hence why select *


while(1):
    # Actual user prompt
    UserPrompt = input("what would you like to do?\n1. browse books\n2. view current orders\n3. logout\n")

    if UserPrompt == "1":
        browse()
    elif UserPrompt == "2":
        orders()
    else:
        break

