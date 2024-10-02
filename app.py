from flask import *
import pymysql


app = Flask (__name__)

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


@app.route ('/about')
def about ():
    return "this is about page"

@app.route ('/register')
def register ():
    return "this is register page"

@app.route ('/login')
def login ():
    return "return login page"

@app.route ('/logout')
def logout ():
    return "this is logout page"

if __name__ == '__main__':
    app.run(debug=True,port=3000)
