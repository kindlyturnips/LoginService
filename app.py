#--------------------------------------------------------------------------------------------
#                                login.py                
#                   Simple login service using flask, sqlalchemy, a psql database
#                   
#                               10/18/2023
#                   Created by Christopher Turnipseed
#
#                    To add:
#                    Hash & salt password functionality
#                    https://stackoverflow.com/questions/1054022/best-way-to-store-password-in-database
#--------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify
from sqlalchemy import create_engine, URL, text
#from flask_sqlalchemy import SQLAlchemy
from datetime import date
import re
import bcrypt

app = Flask(__name__)

#Database Connection
def db_conn():
        url        = URL.create(drivername="postgresql",username="turnips",host="/var/run/postgresql",database="login")
        engine     = create_engine(url)
        return engine.connect()

#Password encryption
def hash_salt_pw(pw):
    bytes = pw.encode('utf-8') 
    #Ideally this function & the salt are stored in a 1 way algorithm seprate from the authentication/registration application.
    salt = b'$2b$12$vtb01YfghwgUYO8cgeeBs.'
    return bcrypt.hashpw(bytes, salt).decode()

#Login 
@app.route('/', methods =['GET', 'POST'])
@app.route('/login', methods =['GET', 'POST'])
#Retrieve user input and check database
def login():   
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #User
        username, password = request.form['username'] , hash_salt_pw(request.form['password'])

        #DB
        query         = text(f'SELECT * FROM accounts WHERE accounts.username = \'{username}\' AND accounts.password = \'{password}\'')
        connection    = db_conn()
        account       = connection.execute(query).fetchone()
        #Conditions
        if account is not None:
            session['loggedin'] = True
            session['id'] = account._asdict()['user_id']
            session['username'] = account._asdict()['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

#Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#Register
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        #User
        username = request.form['username']
        password = hash_salt_pw(request.form['password'])
        email = request.form['email']
        #Database
        query      = text(f'SELECT * FROM accounts WHERE accounts.username = \'{username}\'')
        connection = db_conn()
        account    = connection.execute(query).fetchone()
        #Conditions
        #Could add a condition to ensure secure password
        if account is not None:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        #Pass
        else:
            insertion  = text(f'INSERT INTO accounts(username,password,email,created_on,last_login) \
            VALUES(\'{username}\',\'{password}\',\'{email}\',\'{date.today()}\',\'{date.today()}\')')
            connection = db_conn()
            account    = connection.execute(insertion)
            connection.commit()
            print(password)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



#----------------------------------------------------------------------------------
#                                  MAIN LOOP
#----------------------------------------------------------------------------------


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'I love keymchi'
    app.run(debug= True)


