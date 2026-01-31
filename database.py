import sqlite3
con=sqlite3.connect("pharmacy.db")

con.execute('''
CREATE TABLE IF NOT EXISTS register(
name   VARCHAR(50),
username VARCHAR(50),
email VARCHAR(40),
gen VARCHAR(50),
address  VARCHAR(50),
phone VARCHAR(50),
password VARCHAR(50),
cpassword VARCHAR(50),
rque VARCHAR(50))
''')

con.execute('''
CREATE TABLE IF NOT EXISTS food(
item   VARCHAR(50),
price INTEGER(10),
stock INTEGER(10))
''')

con.execute('''
CREATE TABLE IF NOT EXISTS data(
ref   INTEGER(10),
date INTEGER(10),
name  VARCHAR(50),
phone INTEGER(11),
age INTEGER(3),
slip TEXT(1000))
''')

