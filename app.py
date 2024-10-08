from flask import *
import pymysql
from functions import *
from mpesa import *

app = Flask (__name__)

# session key
app.secret_key = "today@90"

@app.route ('/')
def homepage ():
#    connect to DB
    connection = pymysql.connect(host='localhost', user='root', password='', database='jumiya')
    sql = "select * from products where product_category = 'phones' "
    sql1 = "select * from products where product_category = 'electronics' "
    sql2  = "select * from products where product_category = 'beauty' "
    sql3  = "select * from products where product_category = 'shoes' "
    sql4  = "select * from products where product_category = 'tablets' "
    

    # you need to have a cursor 
    # cursor is used to run/execute above sql
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    cursor4 = connection.cursor()

    # execute
    cursor.execute(sql)
    cursor1.execute(sql1)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    cursor4.execute(sql4)

    # fetch all the phone rows
    phones = cursor.fetchall()

    # fetch all the electronics rows
    electronics = cursor1.fetchall()

    # fetch all the beauty rows
    beauty = cursor2.fetchall()

    # fetch all the shoes rows
    shoes = cursor3.fetchall()

    # fetch all tablets rows
    tablets = cursor4.fetchall()
    
    
    return render_template("index.html", phones = phones, electronics = electronics, beauty = beauty, shoes = shoes, tablets = tablets)

    # route for a single item
@app.route("/single/<product_id>")    
def singleitem(product_id):

    # connection to DB
    connection = pymysql.connect(host='localhost', user='root', password='', database='jumiya')
    

    # create sql query
    sql = "select * from products where product_id = %s"

    # create a cursor
    cursor = connection.cursor()

    # execute
    cursor.execute(sql, product_id)

    # get the single product
    product = cursor.fetchone()

    return render_template ("single.html", product = product)

    # upload products
@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # user can add the products
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_cost = request.form['product_cost']
        product_category = request.form['product_category']
        product_image_name = request.files['product_image_name']
        product_image_name.save('static/images/' + product_image_name.filename)

        # connect to DB
        connection = pymysql.connect(host='localhost', user='root', password='', database='jumiya')

        # create a cursor
        cursor = connection.cursor()

        sql = "insert into products (product_name, product_desc, product_cost, product_category, product_image_name) values (%s,%s, %s, %s, %s)"

        data = (product_name, product_desc, product_cost, product_category, product_image_name.filename)

        # execute
        cursor.execute(sql, data)

        # save changes
        connection.commit()






        return render_template("upload.html", message= "product added successfully")
    else:
        return render_template("upload.html", error= "Please add a product")


 # fashion route
 # helps you to see all fashions

@app.route ('/fashion')
def Fashion():
    return "This is a fashion page"

   # a route to upload fashion
   
@app.route('/uploadfashion')
def UploadFashion():
    return render_template ("uploadfashion.html")

@app.route ('/about')
def about ():
    return "this is about page"

@app.route('/register',methods = ['POST' , 'GET'])
def register ():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        password = request.form.get('password')
        # validate user pasword
        # Response = checkpassword(password)
        # if Response == True :
        # # password met all the cnditions

        # else:
        # # password didnot meet all conditions
        # return render_template ('register.html', message = "Reistered successfully")

        

        

        # connect to db
        connection = pymysql.connect(host='localhost', user='root', password='', database='Jamia LTD')
        cursor = connection.cursor()
        sql = "insert into users (user_name, email,gender, phone,password) values (%s, %s, %s,%s,%s)"
        data = (user_name, email,gender, phone,password)
        cursor.execute(sql, data)
        connection.commit()
        return render_template ('register.html', message = "Reistered successfully")
    else:
        return render_template('register.html',error = 'Please register')




@app.route ('/login', methods=['POST', 'GET'])
def login ():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='jumiya')
        cursor = connection.cursor()

        # check if user with email exists in database
        sql = "select * from users where email = %s and password = %s"
        data = (email, password)

        # execute
        cursor.execute(sql, data)

        # check if any result found
        if cursor.rowcount == 0:

        # it means the usernhame and password does not exist
            return render_template ("login.html", error = " Invalid login credentials")
        else:
            session['key'] = email

        # If GET request, show the registration form
            return redirect("/")
            
    else:

        return render_template ('login.html')


    # mpesa
    # implement STK PUSH
@app.route('/mpesa', methods = ['POST'])
def mpesa():
    phone = request.form["phone"]
    amount = request.form["amount"]

    # use mpesa_payment function mpesa.py
    # it accepts the phone and amount as arguments 
    mpesa_payment(amount, phone)

    return '<h1>Please Complete Payment in Your Phone</h1>' \
    '<a href="/" class="btn btn-dark btn-sm" > Go Back To Products </a> '


@app.route ('/logout')
def logout (): 
    session.clear()
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True,port=3000)