import mysql.connector
import uuid
from models import Customer
from collections import namedtuple

mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='dbmsproject01',
        database="bankapp"
    )
cur=mydb.cursor(dictionary=True)

cur.execute('SELECT * FROM Customer where cust_id={}'.format(10822))
res=cur.fetchone()
Customer(cust_id=res['cust_id'], name=res['name'], phone=res['phone'], address=res['address'], email=res['email'], password=res['password'], occupation=res['occupation'], sex=res['sex'], dob=res['dob'])

