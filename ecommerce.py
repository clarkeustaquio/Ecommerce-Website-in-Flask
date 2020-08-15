from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'prettySecret'
connection = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/showroom')
def showroom():
    return render_template('showroom.html')

@app.route('/pianos', methods=['GET','POST'])
def pianos():
    data = None
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        cursor = connection.cursor()

        query = "select * from products ORDER BY product_id ASC"
        cursor.execute(query)
        data = cursor.fetchall()

    finally:
        if connection is not None:
            connection.close()

    return render_template('pianos.html', products=data)

@app.route('/musicartist')
def musicartist():
    return render_template('musicartist.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        cursor = connection.cursor()

        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            session["username"] = username
            query = "select * from customers WHERE username = '{}' AND password = '{}'".format(username, password)
            cursor.execute(query)

            row = cursor.rowcount
            cursor.close()
            if row == 1:
                return redirect('/')
            else:
                return render_template('login.html')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if connection is not None:
            connection.close()

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )

        cursor = connection.cursor()

        if request.method == "POST":
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            birthday = request.form['birthday']
            gender = request.form['gender']
            contact = request.form['contact']

            query = "insert into customers(first_name, last_name, gender, birthday, email_address, username, password, contact) values('{}','{}','{}','{}','{}','{}','{}','{}')".format(firstName, lastName, gender, birthday, email, username, password, contact)
            
            cursor.execute(query)
            connection.commit()
            cursor.close

            return redirect('/login')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()

    return render_template('signup.html')

@app.route('/cart')
def cart():
    courierData = None
    data = None
    courier_id = None
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        cursor = connection.cursor()

        if 'username' in session:
            username = session['username']

            getId = "select customer_id from customers where username ='{}'".format(username)
            cursor.execute(getId)
            userData = cursor.fetchone()
            userId = userData[0]

            cart = "select status, courier_id, product_id, shipping_fee, total_price, product_image, quantity, name, description from orders where customer_id ='{}'".format(userId)
            cursor.execute(cart)
            data = cursor.fetchall()
            
            if data is not None:
                for getCourier in data:
                    courier_id = getCourier[1]

            if courier_id is not None:
                courier = "select name from courier where courier_id = '{}'".format(courier_id)
                cursor.execute(courier)
                courierData = cursor.fetchone()


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()

    return render_template('cart.html', cart = data, courierID = courierData)

@app.route('/profile', methods=['GET','POST'])
def profile():
    password = None
    email = None
    gender = None
    birthday = None
    contact = None
    customer_id = None
    add1 = None
    add2 = None
    cit = None
    postal = None
    code = None
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        
        cursor = connection.cursor()

        if 'username' in session:
            username = session['username']
            query = "select customer_id, password, email_address, gender, birthday, contact from customers where username = '{}'".format(username)

            cursor.execute(query)
            data = cursor.fetchall()

            for datas in data:
                customer_id = datas[0]
                password = datas[1]
                email = datas[2]
                gender = datas[3]
                birthday = datas[4]
                contact = datas[5]
            
            query2 = "select * from countries"
            cursor.execute(query2)
            country = cursor.fetchall()

            query3 = "select address1, address2, city, postal_code, country_code from addresses where customer_id = '{}'".format(customer_id)
            cursor.execute(query3)
            addresses = cursor.fetchall()

            for address in addresses:
                add1 = address[0]
                add2 = address[1]
                cit = address[2]
                postal = address[3]
                code = address[4]
                
        if request.method == "POST":
            if request.form['action'] == "HISTORY":
                return redirect('/history')

            if 'username' in session:
                username = session['username']

                gender = request.form['gender']
                birthday = request.form['birthday']
                contact = request.form['contact']
                
                query = "update customers set gender = '{}', birthday = '{}', contact = '{}' where username = '{}'".format(gender, birthday, contact, username)
                cursor.execute(query)

                address1 = request.form['address1']
                address2 = request.form['address2']
                city = request.form['city']
                postal_code = request.form['postalCode']
                country_code = request.form['country']

                check = "select * from addresses where customer_id = '{}'".format(customer_id)
                cursor.execute(check)

                row = cursor.rowcount

                if row != 0:
                    query2 = "update addresses set address1 = '{}', address2 = '{}', city = '{}', postal_code='{}', country_code='{}' where customer_id = '{}'".format(address1, address2, city, postal_code, country_code,customer_id)
                    cursor.execute(query2)
                else:
                    query3 = "insert into addresses(customer_id, address1, address2, city, postal_code, country_code) values('{}','{}','{}','{}', '{}','{}')".format(customer_id, address1, address2, city, postal_code, country_code)
                    cursor.execute(query3)

                connection.commit()
                cursor.close()
                return redirect('/profile')
        
        
    
    finally:
        if connection is not None:
            connection.close()

    return render_template('profile.html', username=username, password=password, email=email, gender=gender, birthday=birthday, contact=contact, countries=country, address=addresses, add1=add1, add2=add2, cit=cit, postal=postal, code=code)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/password', methods=['GET', 'POST'])
def passwordChange():
    password = None
    email = None
    newPassword = None
    oldPassword = None
    try:
        connection = psycopg2.connect(
            database = "postgres",  
            user = "postgres",
            password = "password"
        )

        cursor = connection.cursor()
        if 'username' in session:
            username = session['username']
            query = "select password, email_address from customers where username = '{}'".format(username)

            cursor.execute(query)
            data = cursor.fetchall()

            for datas in data:
                password = datas[0]
                email = datas[1]

        if request.method == "POST":
            if 'username' in session:
                username = session['username']
                oldPassword = request.form['oldPassword']
                newPassword = request.form['newPassword']

                if password == oldPassword:
                    query = "update customers set password = '{}' where username = '{}'".format(newPassword, username)
                    cursor.execute(query)
                    connection.commit()
                    cursor.close()
            
                    return redirect('/profile')
                else:
                    return redirect('/password')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if connection is not None:
            connection.close()


    return render_template('passwordChange.html', password=password, email=email)

@app.route('/email', methods=['GET','POST'])
def emailChange():
    password = None
    email = None
    oldPassword = None
    newEmail = None
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        
        cursor = connection.cursor()
        
        if 'username' in session:
            username = session['username']
            query = "select password, email_address from customers where username = '{}'".format(username)

            cursor.execute(query)
            data = cursor.fetchall()

            for datas in data:
                password = datas[0]
                email = datas[1]

        if 'username' in session:
            username = session['username']
            oldPassword = request.form['oldPassword']
            newEmail = request.form['newEmail']

            if password == oldPassword:
                query = "update customers set email_address = '{}' where username = '{}'".format(newEmail, username)
                cursor.execute(query)
                connection.commit()
                cursor.close()
                
                return redirect('/profile')
            else:
                return redirect('/email')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if connection is not None:
            connection.close()


    return render_template('emailChange.html', password=password, email=email)


@app.route('/products/<id>', methods=['GET', 'POST'])
def products(id): 
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        cursor = connection.cursor()

        query = "select specification, name, product_image, description, price, stock from products where product_id = '{}'".format(id)
        cursor.execute(query)
        data = cursor.fetchone()

        query2 ="select image_name from product_image where product_id = '{}'".format(id)
        cursor.execute(query2)
        data2 = cursor.fetchone()

        query3 ="select * from products ORDER BY product_id ASC"
        cursor.execute(query3)
        data3= cursor.fetchall()

        query4 ="select * from courier"
        cursor.execute(query4)
        data4= cursor.fetchall()

        userId = None
        if request.method == "POST":
            if request.form['action'] == 'ADD TO CART':
                if 'username' in session:
                    username = session['username']

                    getUser = "select customer_id from customers where username ='{}'".format(username)
                    cursor.execute(getUser)
                    userData = cursor.fetchone()
                    userId = userData[0]

                    courier = request.form['courier']
                    shippingFee = "select price from courier where courier_id ='{}'".format(courier)
                    cursor.execute(shippingFee)
                    courierData = cursor.fetchone()
                    courierFee = courierData[0]

                    productPrice = "select price, stock, product_image, name, description from products where product_id='{}'".format(id)
                    cursor.execute(productPrice)
                    productData = cursor.fetchone()
                    productTotal = productData[0]
                    productStock = productData[1]
                    productImage = productData[2]
                    productName = productData[3]
                    productDescription = productData[4]
                   
                    quantity = request.form['quantity']
                    totalValue = productTotal * int(quantity)

                    orders = "insert into orders(customer_id, status, courier_id, product_id, shipping_fee, total_price, product_image, quantity, name, description) values('{}','{}','{}','{}','{}','{}', '{}', '{}', '{}','{}')".format(userId, 'pending', courier, id, courierFee, totalValue, productImage, quantity, productName, productDescription)
                    cursor.execute(orders)

                    updateQuantity = productStock - int(quantity)

                    updateStock = "update products set stock ='{}' where product_id ='{}'".format(updateQuantity, id)
                    cursor.execute(updateStock)

                    connection.commit()
                    cursor.close()

                    return redirect('/products/{}'.format(id))

            elif request.form['action'] == 'BUY NOW':
                if 'username' in session:
                    username = session['username']

                    getUser = "select customer_id from customers where username ='{}'".format(username)
                    cursor.execute(getUser)
                    userData = cursor.fetchone()
                    userId = userData[0]

                    courier = request.form['courier']
                    shippingFee = "select price from courier where courier_id ='{}'".format(courier)
                    cursor.execute(shippingFee)
                    courierData = cursor.fetchone()
                    courierFee = courierData[0]

                    productPrice = "select price, stock, product_image, name, description from products where product_id='{}'".format(id)
                    cursor.execute(productPrice)
                    productData = cursor.fetchone()
                    productTotal = productData[0]
                    productStock = productData[1]
                    productImage = productData[2]
                    productName = productData[3]
                    productDescription = productData[4]
                   
                    quantity = request.form['quantity']
                    totalValue = productTotal * int(quantity)

                    orders = "insert into buy(customer_id, status, courier_id, product_id, shipping_fee, total_price, product_image, quantity, name, description) values('{}','{}','{}','{}','{}','{}', '{}', '{}', '{}','{}')".format(userId,'pending', courier, id, courierFee, totalValue, productImage, quantity, productName, productDescription)
                    cursor.execute(orders)

                    updateQuantity = productStock - int(quantity)

                    updateStock = "update products set stock ='{}' where product_id ='{}'".format(updateQuantity, id)
                    cursor.execute(updateStock)

                    connection.commit()
                    cursor.close()

                    return redirect('/buy')


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
        
    return render_template('products.html', product_id=id, specification=data, imageSample=data2, products=data3, courier=data4)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    courierData = None
    courierID = None
    data = None
    total = None
    userQueryData = None
    addressQueryData = None
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        cursor = connection.cursor()
        
        if request.method == "POST":
            if 'username' in session:
                username = session['username']

                getId = "select customer_id from customers where username ='{}'".format(username)
                cursor.execute(getId)
                userData = cursor.fetchone()
                userId = userData[0]

                cart = "select status, courier_id, product_id, shipping_fee, total_price, product_image, quantity, name, description from orders where customer_id ='{}'".format(userId)
                cursor.execute(cart)
                data = cursor.fetchall()
                
                for getCourier in data:
                    courier_id = getCourier[1]

                courier = "select name from courier where courier_id = '{}'".format(courier_id)
                cursor.execute(courier)
                courierData = cursor.fetchone()

                total = 0
                for totalPrice in data:
                    total = total + totalPrice[4] + totalPrice[3]

                userQuery = "select first_name, last_name, email_address from customers where username='{}'".format(username)
                cursor.execute(userQuery)
                userQueryData = cursor.fetchone()
                
                addressQuery = "select address1, address2 from addresses where customer_id='{}'".format(userId)
                cursor.execute(addressQuery)
                addressQueryData = cursor.fetchone()
            
                if request.form['action'] == "BUY NOW":
                    orderID = "select order_id, product_id, quantity, total_price, name from orders where customer_id='{}'".format(userId)
                    cursor.execute(orderID)
                    getID = cursor.fetchall()

                    for i in getID:
                        orderedProduct = "insert into history(order_id, product_id, quantity, total_price, customer_id, product_name) values('{}','{}','{}','{}', '{}', '{}')".format(i[0], i[1], i[2], i[3], userId, i[4])
                        cursor.execute(orderedProduct)

                        deleteCart = "delete from orders where order_id='{}'".format(i[0])
                        cursor.execute(deleteCart)

                        connection.commit()
                    return redirect('/')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()

    return render_template('checkout.html', cart = data, courierID = courierData, totalCheckout = total, userQuery=userQueryData, addressQuery=addressQueryData)

@app.route('/history')
def history():
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        cursor = connection.cursor()

        if 'username' in session:
            username = session['username']

            getUser = "select customer_id from customers where username ='{}'".format(username)
            cursor.execute(getUser)
            userData = cursor.fetchone()
            userId = userData[0]

            view = "select * from history where customer_id ='{}'".format(userId)
            cursor.execute(view)
            viewAll = cursor.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()

    return render_template('history.html', history=viewAll)

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    courierData = None
    courierID = None
    data = None
    total = None
    userQueryData = None
    addressQueryData = None
    try:
        connection = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "password"
        )
        cursor = connection.cursor()
        if 'username' in session:
            username = session['username']
            getId = "select customer_id from customers where username ='{}'".format(username)         
            cursor.execute(getId)
            userData = cursor.fetchone()
            userId = userData[0]
       
            userQuery = "select first_name, last_name, email_address from customers where username='{}'".format(username)
            cursor.execute(userQuery)
            userQueryData = cursor.fetchone()

            addressQuery = "select address1, address2 from addresses where customer_id='{}'".format(userId)
            cursor.execute(addressQuery)
            addressQueryData = cursor.fetchone()
            

            cart = "select status, courier_id, product_id, shipping_fee, total_price, product_image, quantity, name, description from buy where customer_id ='{}'".format(userId)
            cursor.execute(cart)
            data = cursor.fetchall()

            for getCourier in data:
                courier_id = getCourier[1]

            courier = "select name from courier where courier_id = '{}'".format(courier_id)
            cursor.execute(courier)
            courierData = cursor.fetchone()

            total = 0
            for totalPrice in data:
                total = total + totalPrice[4] + totalPrice[3]

        if request.method == "POST":
            if request.form['action'] == "BUY NOW":
                orderID = "select order_id, product_id, quantity, total_price, name from buy where customer_id='{}'".format(userId)
                cursor.execute(orderID)
                getID = cursor.fetchall()

                for i in getID:
                    orderedProduct = "insert into history(order_id, product_id, quantity, total_price, customer_id, product_name) values('{}','{}','{}','{}', '{}', '{}')".format(i[0], i[1], i[2], i[3], userId, i[4])
                    cursor.execute(orderedProduct)

                    deleteCart = "delete from buy where order_id='{}'".format(i[0])
                    cursor.execute(deleteCart)
                    
                    connection.commit()
                return redirect('/')
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
    return render_template('buy.html', userQuery=userQueryData, addressQuery=addressQueryData, cart = data, courierID = courierData, totalCheckout = total)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")