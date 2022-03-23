# from . import db
from flask_login import UserMixin
# from sqlalchemy.sql import func
import random

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin):
    def __init__(self,id,email,password):
        self.id=id
        self.email = email
        self.password = password
        
class Bank():
    def __init__(self,bank_name=None,bank_address=None,bank_code=None):
        self.bank_code = bank_code
        self.bank_name = bank_name
        self.bank_address = bank_address
           
class Branch():
    def __init__(self,branch_name=None,branch_address=None,branch_id=None):
        self.brackage_name = branch_name
        self.branch_id = branch_id
        self.branch_address = branch_address

      
class Loan():
    def __init__(self,loan_type=None,amount=None):
        self.loan_type = loan_type
        self.amount = amount

class Account():
    def __init__(self,account_type=None,balance=None,branch_id=None,account_no=None,cust_id=None,branch_name=None):
        self.account_no = account_no
        self.account_type = account_type
        self.balance= balance
        self.branch_id = branch_id
        self.cust_id = cust_id
        self.branch_name=branch_name

class Customer():
    def __init__(self,name=None,phone=None,address=None,email=None,password=None,occupation=None,sex=None,cust_id=None,dob=None):
        self.cust_id = cust_id
        self.name = name 
        self.phone = phone
        self.address = address
        self.email = email
        self.password = password
        self.occupation =occupation
        self.sex = sex
        self.dob=dob
    
class Has():
    def __init__(self,bank_code=None,branch_id=None):
        self.bank_code = bank_code
        self.branch_id = branch_id
        
class AvailedBy():
    def __init__(self,cust_id=None,loan_id=None):
        self.cust_id = cust_id
        self.loan_id = loan_id
    
class HoldBy():
    def __init__(self,account_no=None,cust_id=None):
        self.account_no= account_no
        self.cust_id = cust_id

        