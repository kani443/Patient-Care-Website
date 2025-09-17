# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:43:38 2024

@author: Kanim
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import re
#from flask_table import Table, Col

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'pagelogin'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login')
def login():
    session['loggedin']=False
    if 'name' in session:
        session.pop('name',None)
    if 'email' in session:
        session.pop('email',None)
    if 'id' in session:
        session.pop('id',None)
    if 'contact' in session:
        session.pop('id',None)
    return render_template('login.html')

@app.route('/customer_login',methods=['GET'])
def customer_login():
    return render_template('customer_login.html')
@app.route('/nurse_login',methods=['GET'])
def nurse_login():
    return render_template('nurse_login.html')

@app.route('/customer_account',methods=['GET'])
def customer_create():
    return render_template('customer_account.html')

@app.route('/nurse_account',methods=['GET'])
def nurse_account():
    return render_template('nurse_account.html')

@app.route('/logout',methods=['GET'])
def logout():
    session['loggedin']=False
    if 'name' in session:
        session.pop('name',None)
    if 'email' in session:
        session.pop('email',None)
    if 'id' in session:
        session.pop('id',None)
    if 'contact' in session:
        session.pop('id',None)
    return render_template('logout.html')


@app.route('/customer_account', methods=['POST'], endpoint='customer_account')
def customer_register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'contact' in request.form:
        name = request.form['name']
        email = request.form['email']
        password =request.form['password']
        contact = request.form['contact']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer_accounts WHERE email = %s', (email,))
        account = cursor.fetchone() 
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Name must contain only characters and numbers!'
        elif not re.match(r'[0-9]+',contact):
            msg = 'Contact must contain only numbers'
        elif not name or not password or not email or not contact:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO customer_accounts VALUES (NULL, % s, % s, % s, %s)', (email, name, contact, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('customer_success.html',msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('customer_account.html', msg=msg)

@app.route('/customer_login',methods=['POST'])
def customer_login_now():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer_accounts WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['name'] = account['name']
            session['contact'] = account['contact']
            msg = 'Logged in successfully !'
            email = account['email']
            name=account['name']
            contact = account['contact']
            return render_template('customer_dashboard.html', msg = msg, email=email, name=name, contact=contact)
        else:
            msg = 'Incorrect email / password !'
    return render_template('customer_login.html', msg = msg)

@app.route('/nurse_account', methods = ['POST'])
def nurse_register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'contact' in request.form:
        name = request.form['name']
        email = request.form['email']
        password =request.form['password']
        contact = request.form['contact']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM nurse_accounts WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Username must contain only characters!'
        elif not name or not password or not email or not contact:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO nurse_accounts VALUES (NULL, % s, % s, % s, %s)', (email, name, contact, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('nurse_success.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('nurse_account.html', msg=msg)

@app.route('/nurse_login',methods=['POST'])
def nurse_login_now():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM nurse_accounts WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['name']=account['name']
            session['contact']=account['contact']
            msg = 'Logged in successfully !'
            email = account['email']
            name=account['name']
            contact = account['contact']
            return render_template('nurse_dashboard.html', msg = msg, email=email, name=name, contact=contact)
        else:
            msg = 'Incorrect email / password !'
    return render_template('nurse_login.html', msg = msg)

@app.route('/nurse_details',methods=['GET'])
def nurse_details_page():
    return render_template('nurse_details.html')    

@app.route('/nurse_details',methods=['POST'])
def get_nurse_details():
    if 'qualification' in request.form and 'experience' in request.form and 'desired_location' in request.form and 'contact' in request.form:
        qualification = request.form['qualification']
        experience = request.form['experience']
        location = request.form['desired_location']
        contact = request.form['contact']
        salary = request.form ['desired_salary']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        email  = session.get('email')
        name = session.get('name')
        cursor.execute('SELECT * FROM nurse_req WHERE email = % s', (email, ))
        details = cursor.fetchone()
        if details:
            msg = 'Request already posted'
        else:
            cursor.execute('INSERT INTO nurse_req VALUES (NULL, %s,%s, %s, %s, %s, %s,%s)', (email,name, qualification, experience, location, contact, salary))
            print("Done")
            mysql.connection.commit()
            msg = 'Request successfully implemented'
            return render_template('nurse_posted.html')
    else:
        msg = 'enter all details'
    return render_template('nurse_details.html',msg=msg)    

@app.route('/nurse_dashboard',methods=['GET'])
def get_nurse_dashboard():
    return render_template('nurse_dashboard.html',name=session.get('name'),email = session.get('email'),contact=session.get('contact'))

@app.route('/view_your_request_nurse', methods=['GET'])
def view_your_req_nurse():
    email = session.get('email')

    print(f"Session email: {email}")
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    email = email.strip()
    print(f"Querying for email: {email}")
    cursor.execute('SELECT * FROM nurse_req WHERE LOWER(email) = LOWER(%s)', (email,))
    item = cursor.fetchone()
    print(f"Fetched item from database: {item}")
    
    cursor.close()

    return render_template('your_nurse_request.html', email=email, item=item)

@app.route('/view_all_nurse_req', methods=['GET'])
def view_all_nurse_req():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM nurse_req")  
        items = cursor.fetchall()
        cursor.close()
        return render_template('nurse_requests.html', items=items)

    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route('/customer_details',methods=['GET'])
def customer_details_page():
    return render_template('customer_details.html')

@app.route('/customer_details', methods=['POST'])
def get_customer_details():
    msg = ''  # Initialize msg variable
    # Check for the presence of all required fields in the form
    if all(field in request.form for field in ['description', 'location', 'contact', 'age']):
        location = request.form['location']
        contact = request.form['contact'] 
        description = request.form['description']
        age = request.form['age']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        email = session.get('email')
        name = session.get('name')

        print(f"Email: {email}, Name: {name}, Description: {description}, Location: {location}, Contact: {contact}, Age: {age}")

        cursor.execute('SELECT * FROM customer_post WHERE email = %s', (email,))
        details = cursor.fetchone()

        if details:
            msg = 'Request already posted'
            print(msg)
        else:
            try:
                cursor.execute('INSERT INTO customer_post (email, name, description, location, contact, age) VALUES (%s, %s, %s, %s, %s, %s)', 
                               (email, name, description, location, contact, age))
                mysql.connection.commit()
                msg = 'Your request has been posted successfully.'
                print(msg)
                return render_template('customer_posted.html', msg=msg)
            except Exception as e:
                mysql.connection.rollback()  # Rollback in case of error
                msg = f'Error inserting data: {str(e)}'
                print(msg)
        
        cursor.close()  # Close the cursor after operations
    else:
        msg = 'Please enter all details.'
        print(msg)

    return render_template('customer_details.html', msg=msg)

@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('customer_dashboard.html',name=session['name'],email=session['email'],contact=session['contact'])

@app.route('/view_your_request_customer')
def view_your_req_customer():
    email = session.get('email')

    print(f"Session email: {email}")
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    email = email.strip()
    print(f"Querying for email: {email}")
    cursor.execute('SELECT * FROM customer_post WHERE LOWER(email) = LOWER(%s)', (email,))
    item = cursor.fetchone()
    print(f"Fetched item from database: {item}")
    
    cursor.close()

    return render_template('your_customer_request.html', email=email, item=item)

@app.route('/view_all_customer_req', methods=['GET'])
def view_all_customer_req():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer_post")  
        items = cursor.fetchall()
        cursor.close()
        return render_template('customer_requests.html', items=items)

    except Exception as e:
        return render_template('error.html', error=str(e)), 500
    
@app.route('/delete_your_nurse')
def delete_nurse():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    email = session.get('email')
    email = email.strip()
    cursor.execute('DELETE FROM nurse_req where LOWER(email) = LOWER(%s)',(email,))
    mysql.connection.commit()
    cursor.close()
    return render_template("nurse_dashboard.html",name=session.get('name'),email=session.get('email'),contact=session.get('contact'))

@app.route('/delete_customer_req')
def delete_customer():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    email=session.get('email')
    name=session.get('name')
    contact=session.get('contact')
    email=email.strip()
    cursor.execute('DELETE FROM customer_post where LOWER(email) = LOWER(%s)',(email,))
    mysql.connection.commit()
    cursor.close()
    print(f"Email: {email}, Name: {name}, name: {name}, Contact: {contact}")
    return render_template("customer_dashboard.html")

    
   

if __name__ == '__main__':

    app.run(debug=False)

