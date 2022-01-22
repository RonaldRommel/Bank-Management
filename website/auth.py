from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import mydb
from .models import Customer,Account
import uuid
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
import random

auth = Blueprint('auth', __name__)

cur=mydb.cursor()
cur.execute("use bankapp")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cur.execute("select cust_id,password from customer where email='{}'".format(email))
        details=cur.fetchone()
        if details !=None:
            (cust_id,passwd)=details
            if check_password_hash(passwd, password):
                flash('Logged in successfully!', category='success')                
                user=User(id=cust_id,email=email,password=passwd)
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
            
    # return render_template("login.html")
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phoneNumber = request.form.get('phoneNumber')
        dob = request.form.get('dob')
        sex = request.form.get('sex')
        occupation = request.form.get('occupation')
        acctype = request.form.get('acctype')
        address = request.form.get('address')
        bid = request.form.get('bid')
        cur.execute("select password from customer where email='{}'".format(email))
        password=cur.fetchone() 
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif(len(phoneNumber)<10):
            flash('Phone number must be at least 10', category='error')
        elif len(occupation)<3:
            flash('Occupation must be greater than 3 characters', category='error')
        elif len(address)<3:
            flash('Address must be greater than 3 characters.', category='error')
        else:
            if password != None:
                if(check_password_hash(password[0],password1)):
                    cur.execute("select cust_id from customer where email='{}'".format(email))
                    cust_id=cur.fetchone()[0]
                    account_no=str(uuid.uuid1()).replace('-','')[:15]
                    cur.execute("INSERT into Account (account_no ,account_type ,balance,branch_id) values ('{}','{}',{},{})".format(account_no,acctype,5000,bid))
                    mydb.commit()
                    cur.execute("INSERT INTO holdby (account_no ,cust_id) values ('{}','{}') ".format(account_no,cust_id))
                    mydb.commit()
                    user=User(cust_id,email=email,password=password[0])
                    login_user(user, remember=True)
                    flash('New Account created with old personal details!', category='success')
                else:
                    flash('Account already exists, to create another account enter correct password', category='error')
            else:    
                cust_id=random.randint(10000,99999)
                # f=open('output.txt','w')
                # f.write("Insert into customer (cust_id ,name ,phone ,address ,email ,password ,occupation ,sex,dob) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(cust_id,name,len(phoneNumber),len(address),len(email),len(password1),len(occupation),sex,dob))
                # f.close()
                passwd=generate_password_hash(password1,method='sha256')
                cur.execute("Insert into customer (cust_id ,name ,phone ,address ,email ,password ,occupation ,sex,dob) values ({},'{}',{},'{}','{}','{}','{}','{}','{}')".format(cust_id,name,phoneNumber,address,email,passwd,occupation,sex,dob))
                mydb.commit()
                account_no=str(uuid.uuid1()).replace('-','')[:15]
                cur.execute("INSERT into Account (account_no ,account_type ,balance,branch_id) values ('{}','{}',{},{})".format(account_no,acctype,5000,bid))
                mydb.commit()
                cur.execute("INSERT INTO holdby (account_no ,cust_id) values ('{}','{}') ".format(account_no,cust_id))
                mydb.commit()
                user=User(cust_id,email=email,password=passwd)
                login_user(user, remember=True)
                flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    cur.execute("select branch_name ,br.branch_id from bank b,branch br,has h where b.bank_code = h.bank_code and br.branch_id = h.branch_id")
    branches=cur.fetchall()
    
    return render_template("sign_up.html",branches=branches,user=current_user)
    # return render_template("sign_up.html", user=current_user)
