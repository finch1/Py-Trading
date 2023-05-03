# https://www.youtube.com/watch?v=OjMDXTlVOYU
# https://www.youtube.com/watch?v=pU53JUhSnkY

import sqlite3
import pandas as pd
import sqlalchemy
import yfinance as yf

'''
connection = sqlite3.connect('OurDataBase.db') # creates a new one if not existing
cursor = connection.cursor()

name = ""
surname = ""
salary = ""
cursor.execute("INSERT INTO employees VALUES (?,?,?)", (name, surname, salary))
cursor.execute("SELECT * FROM employees")
cursor.fetchall()
'''

'''
# for better performance, use engine
engine = sqlalchemy.create_engine('sqlite:///OurDataBase.db/')

pd.read_sql('SELECT employees', engine)

df1 = pd.DataFrame([{'name':'Max', 'surname':'Maxwell'}])
df1.to_sql('employees', engine) # creates table and inserts
df1.to_sql('employees', engine, if_exists='append', index=False) # creates table and inserts. add to existing data. ignore index
'''

engine = sqlalchemy.create_engine('sqlite:///OurDataBase.db/')

df = yf.download('F', start='2021-01-01')

# write to DB
df.to_sql('F', engine)

# read from DB
pd.read_sql('F', engine)

