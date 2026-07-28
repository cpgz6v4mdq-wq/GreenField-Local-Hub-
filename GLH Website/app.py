#Modules Imported
from flask import Flask, render_template, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
#Assign app
app = Flask(__name__)

#Secret key is stored here. Please change it before sending it into production
app.secret_key = "Change_secret_key"

#Route for home
@app.route("/")
def home():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    #Selects 3 products from the products table in the database
    products = cursor.execute("SELECT * FROM products").fetchmany(3)
    farms = cursor.execute("SELECT * FROM producer_farms").fetchmany(3)
    db.close()
    print(type(session.get("loyalty")))
    loyalty = session.get("loyalty")
    if "user" not in session:
        return render_template("base.html", user=session.get("user"), user_type=session.get("type"), products=products, loyalty=loyalty, farms=farms)
    
    if "customer" in session.get("type"):
        return render_template("base.html", user=session.get("user"), user_type=session.get("type"), products=products, loyalty=int(loyalty), farms=farms)
    
    return render_template("base.html", user=session.get("user"), user_type=session.get("type"), products=products, loyalty=loyalty, farms=farms)

@app.route("/shop", methods=["POST", "GET"])
def shop():
    #If request is made the shop will select the category from the database that the user has chosen
    if request.method == "POST":
        db = sqlite3.connect("database.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        category = request.form["category"]
        
        products = cursor.execute("SELECT * FROM products WHERE category = ?", (category,)).fetchall()
        db.close()
    #If user does not request the shop will display all products
    else:
        db = sqlite3.connect("database.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        products = cursor.execute("SELECT * FROM products").fetchall()
        
        db.close()
    loyalty = session.get("loyalty")
    if "user" not in session: #Checks if user is not in session
        return render_template("shop.html", user=session.get("user"), user_type=session.get("type"), products=products, loyalty=loyalty)
    if "customer" in session.get("type"): #Checks if customer is in session
        return render_template("shop.html", user=session.get("user"), user_type=session.get("type"), products=products, loyalty=int(loyalty))
    return render_template("shop.html", user=session.get("user"), user_type=session.get("type"), products=products, loyalty=loyalty)

@app.route("/map")
def map():
    #Displays all the producers on the map page
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    farms = cursor.execute("SELECT * FROM producer_farms").fetchall()
    db.close()
    return render_template("map.html", user=session.get("user"), user_type=session.get("type"), farms=farms)

#Route for supporting local farms
@app.route("/support_local_farms")
def support_local_farms():
    return render_template("supportLocals.html", user=session.get("user"), user_type=session.get("type"))

@app.route("/login_signup")
def login_signup():
    if "user" in session: #if user is in session it prevents them from accessing the login page
        return redirect("/")
    
    return render_template("login.html")

#Gets the route for customer signups
@app.route("/customer_signup", methods=["POST", "GET"])
def customer_signup():
    if "user" in session:
        return redirect("/")
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"].lower().replace(" ", "")
        password = request.form["password"]
        if len(name) < 1: #Checks if user has entered a name
            return render_template("login.html", display_message="Please enter a name")
        if len(name) > 50:
            return render_template("login.html", display_message="Name is too long")
        if len(password) < 6: #checks if password is less then 6 characters or more
            return render_template("login.html", display_message="Password must be 6 characters or longer")
        if len(password) > 30: #Checks idf the password exceeds 30 characters
            return render_template("login.html", display_message="Passsword exceeds the length of 30 characters")
        if len(email) > 256: #Checks if email exceeds 256 characters
            return render_template("login.html", display_message="Email exceeds 256 characters. Please enter a valid email")
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT email from customer_users WHERE email = ?", (email,))
        email_exists = cursor.fetchone()
        if email_exists:
            return render_template("login.html", display_message="Email already exists. Please login")
        cursor.execute("INSERT INTO customer_users (name, email, password) VALUES(?,?,?)", (name, email, generate_password_hash(password)))
        cursor.execute("SELECT email from customer_users WHERE email = ?", (email,))
        user_exists = cursor.fetchone()
        db.commit()
        db.close()
        if user_exists:
            return render_template("login.html", display_message="Account has been created. Please login")
    else:
        return redirect("/login_signup")
    return render_template("login.html")

#Gets the route for producer signups
@app.route("/producer_signup", methods=["POST", "GET"])
def producer_signup():
    if "user" in session:
        return redirect("/")
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"].lower().replace(" ", "")
        password = request.form["password"]
        if len(name) < 1: #Checks if user has entered a name
            return render_template("login.html", display_message="Please enter a name")
        if len(name) > 50:
            return render_template("login.html", display_message="Name is too long")
        if len(password) < 6: #checks if password is less then 6 characters or more
            return render_template("login.html", display_message="Password must be 6 characters or longer")
        if len(password) > 30: #Checks idf the password exceeds 30 characters
            return render_template("login.html", display_message="Passsword exceeds the length of 30 characters")
        if len(email) > 256: #Checks if email exceeds 256 characters
            return render_template("login.html", display_message="Email exceeds 256 characters. Please enter a valid email")
        db = sqlite3.connect("database.db")
        cursor = db.cursor() #Connects the database
        cursor.execute("SELECT email from producer_users WHERE email = ?", (email,))
        email_exists = cursor.fetchone()
        if email_exists: #Checking if email exists to ensure that there are no duplicates
            return render_template("login.html", display_message="Email already exists. Please login")
        cursor.execute("INSERT INTO producer_users (name, email, password) VALUES(?,?,?)", (name, email, generate_password_hash(password))) #Insers the email, name, and hashed password into the database
        cursor.execute("SELECT email from producer_users WHERE email = ?", (email,))
        user_exists = cursor.fetchone()
        db.commit() #pushes updates and closes the database to prevent any further updates
        db.close()
        if user_exists:
            return render_template("login.html", display_message="Account has been created. Please login")
    else:
        return redirect("/login_signup")
    return render_template("login.html")

@app.route("/customer_login", methods=["GET", "POST"])
def customer_login():
    if "user" in session: #if user is in session it prevents them from accessing the login page
        return redirect("/")
    if request.method == "POST":
        email = request.form["email"].lower().replace(" ", "") #gets email from form
        password = request.form["password"] #gets password from form
        db = sqlite3.connect("database.db") #connects to the database
        cursor = db.cursor()
        cursor.execute("SELECT name, email, password, loyalty FROM customer_users WHERE email = ?", (email,)) #Selects customer information from database
        user = cursor.fetchone() #Fetches user information
        
        if user and check_password_hash(user[2], password): #Checks if user exists and if the password is correct by checking the hash
            session["user"] = user[0] #Assigns users name to session
            session["email"] = user[1] #Assigns users email to session
            session["type"] = "customer"
            session["loyalty"] = user[3]
            return redirect("/") #returns redirect to homepage
        else:
            return render_template("login.html", display_message="Password or email is incorrect")
    else:
        return redirect("/login_signup")
    return render_template("login.html")


@app.route("/producer_login", methods=["GET", "POST"])
def producer_login():
    if "user" in session: #if user is in session it prevents them from accessing the login page
        return redirect("/")
    if request.method == "POST":
        email = request.form["email"].lower().replace(" ", "") #gets email from form
        password = request.form["password"] #gets password from form
        db = sqlite3.connect("database.db") #connects to the database
        cursor = db.cursor()
        cursor.execute("SELECT name, email, password FROM producer_users WHERE email = ?", (email,)) #Selects customer information from database
        user = cursor.fetchone() #Fetches user information
        
        if user and check_password_hash(user[2], password): #Checks if user exists and if the password is correct by checking the hash
            session["user"] = user[0] #Assigns users name to session
            session["email"] = user[1] #Assigns users email to session
            session["type"] = "producer"
            
            return redirect("/") #returns redirect to homepage
        else:
            return render_template("login.html", display_message="Password or email is incorrect")
    else:
        return redirect("/login_signup")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    #If user is not in session they will be redirected to the homepage
    if "user" not in session:
        return redirect("/login_signup")
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    email = session.get("email")
    




    
    
    
    cursor.execute("SELECT email, new from producer_users WHERE email = ?", (email,))
    producer_new = cursor.fetchone()
    print(producer_new)
    #if producer is in session it will display 3 products from the database
    if "producer" in session["type"]:
        products = cursor.execute("SELECT * FROM products WHERE producer = ? ", (email,)).fetchmany(3)
        db.close()
        return render_template("dashboard.html", producer_new=producer_new[1], user=session.get("user"), user_type=session.get("type"), products=products)
    else:
        #If user is in session it will display 3 of their orders from the database
        orders = cursor.execute("SELECT * FROM orders WHERE customer_email = ?", (email,)).fetchmany(3)
        user = cursor.execute("SELECT email, loyalty FROM customer_users WHERE email = ?", (email,)).fetchone()
        special_offers = cursor.execute("SELECT * FROM special_offers").fetchmany(3)
        print(user["loyalty"])
        loyalty = user["loyalty"]
        db.close()
        return render_template("dashboard.html", user=session.get("user"), user_type=session.get("type"), orders=orders, loyalty=int(loyalty), special_offers=special_offers)


@app.route("/new_farm", methods=["POST", "GET"])
def new_farm():
    if request.method == "POST":
        #Gets producers farm details
        farm_name = request.form["farm_name"]
        desc = request.form["description"]
        phone_number = request.form["phone_number"]
        website_link = request.form["website_link"]
        image = request.form["image"]
        email = session.get("email")
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        #Adds producer farm details to a database
        cursor.execute("INSERT INTO producer_farms (farm,description,telephone,website, email, image) VALUES(?,?,?,?,?,?)", (farm_name,desc,phone_number,website_link, email, image))
        cursor.execute("UPDATE producer_users SET new = 1 WHERE email = ?", (email,))
        db.commit()
        db.close()
        return redirect("/dashboard")
    else:
        return redirect("/")


@app.route("/account_settings")
def account_settings():
    if "user" not in session: #if user not in session return redirect
        return redirect("/")
    return render_template("accountSettings.html", user_type=session.get("type"), user=session.get("user"), loyalty=session.get("loyalty"))

@app.route("/update_customer_email", methods=["GET", "POST"])
def update_customer_email():
    if request.method == "POST":
        old_email = request.form["old_email"]
        new_email = request.form["new_email"]
        password = request.form["password"]
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT email, password FROM customer_users WHERE email = ?", (old_email,)) #Selects customer information from database
        user = cursor.fetchone() #Fetches user information
        if user and check_password_hash(user[1], password):
            cursor.execute("UPDATE customer_users SET email = ? WHERE email = ?", (new_email, old_email))
            cursor.execute("UPDATE orders SET customer_email = ? WHERE customer_email = ?", (new_email, old_email))
            db.commit()
            db.close()
            session["email"] = new_email
            return render_template("accountSettings.html", user=session.get("user"), user_type=session.get("type"))
        else:
            return render_template("accountSettings.html", display_message="Password or email is incorrect", user=session.get("user"), user_type=session.get("type"))
    else:
        return redirect("/")


@app.route("/update_producer_email", methods=["GET", "POST"])
def update_producer_email():
    if request.method == "POST":
        old_email = request.form["old_email"]
        new_email = request.form["new_email"]
        password = request.form["password"]
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT email, password FROM producer_users WHERE email = ?", (old_email,)) #Selects customer information from database
        user = cursor.fetchone() #Fetches user information
        if user and check_password_hash(user[1], password):
            cursor.execute("UPDATE producer_users SET email = ? WHERE email = ?", (new_email, old_email))
            cursor.execute("UPDATE products SET producer = ? WHERE producer = ?", (new_email, old_email))
            cursor.execute("UPDATE producer_farms SET email = ? WHERE email = ?", (new_email, old_email))
            cursor.execute("UPDATE special_offers SET producer = ? WHERE producer = ?", (new_email, old_email))
            db.commit()
            db.close()
            session["email"] = new_email
            return render_template("accountSettings.html", user=session.get("user"), user_type=session.get("type"))
        else:
            return render_template("accountSettings.html", display_message="Password or email is incorrect", user=session.get("user"), user_type=session.get("type"))
    else:
        return redirect("/")

        

@app.route("/buy_special_offer<int:product_id>")
#Inserts the product the user has bought into orders
def buy_special_offer(product_id):
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    product = cursor.execute("SELECT * FROM special_offers WHERE id = ?", (product_id,)).fetchone()
    customer_email = session.get("email")
    cursor.execute("INSERT INTO orders (customer_email,product, image,price, collect) VALUES(?,?,?, ?,?)", (customer_email, product["product"], product["image"], product["price"], "N/A"))
    db.commit()
    db.close()
    return redirect("/orders") #Returns to orders for the customer to view the order

@app.route("/logout")
def logout():
    if "user" not in session:
        return redirect("/")
    session.clear()
    return redirect("/") #clear session and redirects user to homepage


@app.route("/marketing", methods=["POST", "GET"])
def marketing():
    if request.method == "POST":
        email = request.form["email"].lower().replace(" ", "")
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT emails from marketing WHERE emails = ?", (email,))
        email_exists = cursor.fetchone() #Sees if email already exists in marketing
        
        if email_exists:
            return "", 204
        else:
            cursor.execute("INSERT INTO marketing (emails) VALUES(?)", (email,)) #Insers email into marketing
            db.commit()
            db.close()
            return "", 204
    else:
        return redirect("/")
        

#Allows for producer to add products to the products database
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        producer_email = session.get("email")
        product_name = request.form["product"]
        category = request.form["category"]
        print(category)
        image_link = request.form["image_link"] #Gets product information
        desc = request.form["description"]
        price = request.form["price"]
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        

        
        
        
        cursor.execute("INSERT INTO products (producer,product,image,desc,price, category) VALUES(?,?,?,?,?,?)", (producer_email, product_name, image_link, desc, price,category)) #Insers product information into the database
        db.commit()
        db.close()
        return redirect("/dashboard") #Return redirect to dashbaord after form has been complete
    else:
        return redirect("/") #If post request is not made a redirect to the homepage will be made

#Allows for producer to add special offers
@app.route("/special_offers", methods=["POST", "GET"])
def special_offers():
    if request.method == "POST":
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        producer_email = session.get("email")
        product_name = request.form["product"]
        desc = request.form["desc"]
        image = request.form["image"]
        price = request.form["price"]
        cursor.execute("INSERT INTO special_offers (producer,product,image,desc,price) VALUES(?,?,?,?,?)", (producer_email, product_name, image,desc,price))
        db.commit()
        db.close()
        return redirect("/dashboard")
    else:
        return redirect("/")
@app.route("/view_product/<int:product_id>") #Gets product id 
def view_product(product_id):
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    product = cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone() #Selects product information by using the product id
    db.close()
   
    loyalty = session.get("loyalty")
    price = product["price"]
    
    if "user" not in session:
        return render_template("product_page.html", product=product, loyalty=loyalty, user=session.get("user"), user_type=session.get("type")) #displays the product on the product page
    if "customer" in session.get("type"): #if customer has loyalty then they will be given a discounted price of 20%
        if int(loyalty) == 1:
            discounted_price = round(price * 0.8, 2)
            print(discounted_price)
            return render_template("product_page.html", product=product, discounted_price=discounted_price, loyalty=int(loyalty), user=session.get("user"), user_type=session.get("type"))
        return render_template("product_page.html", product=product, loyalty=int(loyalty), user=session.get("user"), user_type=session.get("type")) 
    return render_template("product_page.html", product=product, loyalty=loyalty, user=session.get("user"), user_type=session.get("type"))
    



@app.route("/buy_product/<int:product_id>", methods=["GET", "POST"])
def buy_product(product_id):
    if "user" not in session:
        return redirect("/login_signup")
    if "producer" in session.get("type"): #Producer cannot buy products
        return redirect("/")
    
    if request.method == "POST":
        customer_email = session.get("email")
        db = sqlite3.connect("database.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        product = cursor.execute("SELECT id, product, image, price FROM products WHERE id = ?", (product_id,)).fetchone() #Selects product details using product id
        loyalty = session.get("loyalty")
        price = product["price"]
        collect = request.form["collect"]
        if int(loyalty) == 1:
            discounted_price = round(price * 0.8, 2) #if customer has loyalty then they will be given a discounted price of 20%
            cursor.execute("INSERT INTO orders (customer_email,product, image,price, collect) VALUES(?,?,?, ?,?)", (customer_email, product["product"], product["image"], discounted_price, collect))
        else:
            cursor.execute("INSERT INTO orders (customer_email,product, image,price,collect) VALUES(?,?,?, ?,?)", (customer_email, product["product"], product["image"], product["price"],collect)) #Inserst the product into orders under the customers email
        db.commit()
        db.close()
        #Return to orders
        return redirect("/orders")
    else:
        return redirect("/")

@app.route("/manage_orders") #Allows for producer to manage orders
def manage_orders():
    if "user" not in session:
        return redirect("/")
    if "customer" in session:
        return redirect("/")
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    email = session.get("email")
    products = cursor.execute("SELECT * FROM products WHERE producer = ?", (email,)).fetchall()
    db.close()
    return render_template("manageProducts.html", products=products, user=session.get("user"))




@app.route("/delete_product/<int:product_id>") #Allows for producer to delete product
def delete_product(product_id):
    if "user" not in session:
        return redirect("/")
    if "customer" in session:
        return redirect("/")
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    db.close()
    return redirect("/manage_orders")


#Allows for producer to update product name
@app.route("/product_name/<int:product_id>", methods=["GET", "POST"])
def product_name(product_id):
    if request.method == "POST":
        product = request.form["product"]
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        
        cursor.execute("UPDATE products SET product = ? WHERE id = ?", (product,product_id))
        db.commit()
        db.close()
        return redirect("/manage_orders")
    else:
        return redirect("/")

#Allows for producer to update product description
@app.route("/product_description/<int:product_id>", methods=["GET", "POST"])
def product_description(product_id):
    if request.method == "POST":
        desc = request.form["description"]
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        
        cursor.execute("UPDATE products SET desc = ? WHERE id = ?", (desc,product_id))
        db.commit()
        db.close()
        return redirect("/manage_orders")
    else:
        return redirect("/")

#Allows for producer to update product image
@app.route("/product_image/<int:product_id>", methods=["GET", "POST"])
def product_image(product_id):
    if request.method == "POST":
        image = request.form["image"]
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        
        cursor.execute("UPDATE products SET image = ? WHERE id = ?", (image,product_id))
        db.commit()
        db.close()
        return redirect("/manage_orders")
    else:
        return redirect("/")

#Allows for producer to update product price
@app.route("/product_price/<int:product_id>", methods=["GET", "POST"])
def product_price(product_id):
    if request.method == "POST":
        price = request.form["price"]
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        
        cursor.execute("UPDATE products SET price = ? WHERE id = ?", (price,product_id))
        db.commit()
        db.close()
        return redirect("/manage_orders")
    else:
        return redirect("/")














#Allows for customer to see their orders they have made
@app.route("/orders")
def orders():
    if "producer" in session:
        return redirect("/")
    if "user" not in session:
        return redirect("/")
    email = session.get("email")
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    products = cursor.execute("SELECT * FROM orders WHERE customer_email = ?", (email,)).fetchall()
    return render_template("orders.html", products=products, user=session.get("user"), user_type=session.get("type"))


#Gives the customer the option to cancel any order by using the product id
@app.route("/cancel_orders/<int:product_id>")
def cancel_orders(product_id):
    if "producer" in session:
        return redirect("/")
    if "user" not in session:
        return redirect("/")
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    
    cursor.execute("DELETE FROM orders WHERE id = ?", (product_id,))
    db.commit()
    db.close()
    return redirect("/orders")
@app.route("/get_loyalty") #Allows customer to get loyatly scheme giving them benefits such as discounts and special offers
def get_loyalty():
    if "producer" in session.get("type"):
        return redirect("/")
    if "user" not in session:
        return redirect("/")
    if session.get("loyalty") == 1:
        return redirect("/")
    if "email" not in session:
        return redirect("/")
    email = session.get("email")
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("UPDATE customer_users SET loyalty = ? WHERE email = ?", (1, email))
    db.commit()
    db.close()
    session["loyalty"] = 1
    return redirect("/dashboard")


@app.route("/cancel_loyalty") #Allows for customer to cancel their loyalty scheme
def cancel_loyalty():
    if "producer" in session:
        return redirect("/")
    if "user" not in session:
        return redirect("/")
    
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    email = session.get("email")

    cursor.execute("UPDATE customer_users SET loyalty = ? WHERE email = ? ", (0,email))
    db.commit()
    db.close()
    session["loyalty"] = 0
    return redirect("/")

@app.route("/delete_account") #Allows for user to delete their account
def delete_account():
    if "customer" in session.get("type"):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        email = session.get("email")
        cursor.execute("DELETE FROM customer_users WHERE email = ?", (email,))
        cursor.execute("DELETE FROM orders WHERE customer_email = ?", (email,))
        
        db.commit()
        db.close()
        session.clear()
        return redirect("/")
    
    if "producer" in session.get("type"):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        email = session.get("email")
        cursor.execute("DELETE FROM producer_users WHERE email = ?", (email,))
        cursor.execute("DELETE FROM producer_farms WHERE email = ?", (email,))
        cursor.execute("DELETE FROM products WHERE producer = ?", (email,))
        db.commit()
        db.close()
        session.clear()
        return redirect("/")
    





#Allows producer to updat farm name
@app.route("/update_farm_name", methods=["GET", "POST"])
def update_farm_name():
    if request.method == "POST":
        name = request.form["farm_name"]
        
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        email = session.get("email")
        cursor.execute("UPDATE producer_farms SET farm = ? WHERE email = ? ", (name,email))
        db.commit()
        db.close()
        return redirect("/dashboard")
    
#Allows producer to updat farm description
@app.route("/update_farm_desc", methods=["GET", "POST"])
def update_farm_desc():
    if request.method == "POST":
        description = request.form["description"]
        
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        email = session.get("email")
        cursor.execute("UPDATE producer_farms SET description = ? WHERE email = ? ", (description,email))
        db.commit()
        db.close()
        return redirect("/dashboard")
    



#Allows producer to updat farm telephone number
@app.route("/update_farm_tele", methods=["GET", "POST"])
def update_farm_tele():
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        email = session.get("email")
        cursor.execute("UPDATE producer_farms SET telephone = ? WHERE email = ? ", (phone_number,email))
        db.commit()
        db.close()
        return redirect("/dashboard")
    



#Allows producer to updat farm image
@app.route("/update_farm_img", methods=["GET", "POST"])
def update_farm_img():
    if request.method == "POST":
        image = request.form["image"]
        
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        email = session.get("email")
        cursor.execute("UPDATE producer_farms SET image = ? WHERE email = ? ", (image,email))
        db.commit()
        db.close()
        return redirect("/dashboard")

#Allows producer to updat farm website link
@app.route("/update_farm_link", methods=["GET", "POST"])
def update_farm_link():
    if request.method == "POST":
        website_link = request.form["website_link"]
        
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        email = session.get("email")
        cursor.execute("UPDATE producer_farms SET website = ? WHERE email = ? ", (website_link,email))
        db.commit()
        db.close()
        return redirect("/dashboard")
#Allows app to run
if "__main__" == __name__:
    app.run(debug=True)

