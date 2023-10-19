from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL 
from sqlalchemy.orm import sessionmaker

"""
DB = login
CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP 
);
"""
#connection.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))


url = URL.create(
    drivername="postgresql",
    username="turnips",
    host="/var/run/postgresql",
    database="login"
)
username = 'turnips'
password = 'hyejin'
engine = create_engine(url)
connection = engine.connect()
#connection.execute('SELECT * FROM accounts WHERE username = % s AND password = % s',
#                   (username, password, ))
query = text(f'SELECT * FROM accounts WHERE accounts.username = \'{username}\' AND accounts.password = \'{password}\'')
result = connection.execute(query).fetchall()
print(result)