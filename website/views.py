from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import url_for
from flask_login import login_required, current_user
import json
from . import mydb
from .models import Customer,Account

views = Blueprint('views', __name__)
cur=mydb.cursor(dictionary=True)

# ----------- HOME -------------#c
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    cur.execute('SELECT * FROM Customer where cust_id={}'.format(current_user.id))
    res=cur.fetchone()
    details=Customer(cust_id=res['cust_id'], name=res['name'], phone=res['phone'], address=res['address'], email=res['email'], password=res['password'], occupation=res['occupation'], sex=res['sex'], dob=res['dob'])
    # if request.method == 'POST':
    #     card_name=request.form.get('card')
    #     if(card_name=='Accounts'):
    #         return redirect(url_for('views.accounts'))        
        
    #     elif(card_name=='Debit'):
    #         return redirect(url_for('views.debit'))    
        
    #     elif(card_name=='Credit'):
    #         return redirect(url_for('views.credit'))    
        
    #     elif(card_name=='Transfer Funds'):
    #         return redirect(url_for('views.transfer_funds'))   
        
    #     elif(card_name=='Loan'):
    #         return redirect(url_for('views.loan'))    
         
    return render_template("home.html", user=current_user,details=details)

# ----------- DEBIT -------------#
@views.route('/debit', methods=['GET', 'POST'])
@login_required
def debit():
    if request.method=='POST' :
        accno=request.form.get('accno')
        deb_amt=int(request.form.get('deb_amt'))
        cur.execute("SELECT balance from account where account_no='{}'".format(accno))
        balance=cur.fetchone()['balance']
        balance=balance-deb_amt
        if(balance>0):
            flash("₹{} Debited, Current balance = ₹{}".format(deb_amt,balance),category='success')
            cur.execute("UPDATE account SET balance={} where account_no='{}'".format(balance,accno))
            mydb.commit()
        else:
            flash("Insufficient balance, Current balance = ₹{}".format(balance+deb_amt),category='error')        
        return redirect(url_for('views.home'))
        
    
    cur.execute('SELECT * from account a,holdby h where a.account_no=h.account_no AND h.cust_id={}'.format(current_user.id))
    accs=cur.fetchall()
    
    accDetails=[]
    for acc in accs:
        accDetails.append(Account(account_no=acc['account_no'], account_type=acc['account_type'], balance=acc['balance'], branch_id=acc['branch_id'], cust_id=acc['cust_id']))
    return render_template("debit.html", user=current_user,accDetails=accDetails)


# ----------- CREDIT-------------#
@views.route('/credit', methods=['GET', 'POST'])
@login_required
def credit():
    if request.method=='POST' :
        accno=request.form.get('accno')
        cred_amt=int(request.form.get('cred_amt'))
        cur.execute("SELECT balance from account where account_no='{}'".format(accno))
        balance=cur.fetchone()['balance']
        balance=balance+cred_amt
        flash("₹{} Credited, Current balance = ₹{}".format(cred_amt,balance),category='success')
        cur.execute("UPDATE account SET balance={} where account_no='{}'".format(balance,accno))
        mydb.commit()        
        return redirect(url_for('views.home'))
        
    
    cur.execute('SELECT * from account a,holdby h where a.account_no=h.account_no AND h.cust_id={}'.format(current_user.id))
    accs=cur.fetchall()
    
    accDetails=[]
    for acc in accs:
        accDetails.append(Account(account_no=acc['account_no'], account_type=acc['account_type'], balance=acc['balance'], branch_id=acc['branch_id'], cust_id=acc['cust_id']))
    return render_template("credit.html", user=current_user,accDetails=accDetails)
    
# ----------- Accounts -------------#
@views.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    cur.execute('SELECT * from account a,holdby h,branch b where b.branch_id=a.branch_id AND a.account_no=h.account_no AND h.cust_id={}'.format(current_user.id))
    accs=cur.fetchall()
    accDetails=[]
    for acc in accs:
        accDetails.append(Account(branch_name=acc['branch_name'],account_no=acc['account_no'], account_type=acc['account_type'], balance=acc['balance'], branch_id=acc['branch_id'], cust_id=acc['cust_id']))
    return render_template("accounts.html", user=current_user,accDetails=accDetails)
    
# ----------- Transfer Funds-------------#
@views.route('/transfer_funds', methods=['GET', 'POST'])
@login_required
def transfer_funds():
    if request.method == 'POST':
        accno=request.form.get('accno')
        ben_accno=request.form.get('ben_accno')
        tf_amt=int(request.form.get('tf_amt'))
        cur.execute("SELECT balance from account where account_no='{}'".format(accno))
        balance=cur.fetchone()['balance']
        if ben_accno==accno:
            flash("Cannot transfer money to the same account!",category='error')
        elif balance>=tf_amt:
            cur.execute("SELECT balance from account where account_no='{}'".format(ben_accno))
            ben_balance=cur.fetchone()
            if(ben_balance!=None):
                ben_balance=ben_balance['balance']+tf_amt
                cur.execute("UPDATE account SET balance={} where account_no='{}'".format(ben_balance,ben_accno))
                mydb.commit() 
                cur.execute("UPDATE account SET balance={} where account_no='{}'".format(balance-tf_amt,accno))
                mydb.commit() 
                flash("₹{} Transfered, Current balance = ₹{}".format(tf_amt,balance-tf_amt),category='success')
                return redirect(url_for('views.home'))
            else:
                flash("Could not find beneficiary account!",category='error')
        else:
            flash("Insufficient balance, Current balance = ₹{}".format(balance),category='error')
            return redirect(url_for('views.home'))
                    
    cur.execute('SELECT * from account a,holdby h where a.account_no=h.account_no AND h.cust_id={}'.format(current_user.id))
    accs=cur.fetchall()
    
    accDetails=[]
    for acc in accs:
        accDetails.append(Account(account_no=acc['account_no'], account_type=acc['account_type'], balance=acc['balance'], branch_id=acc['branch_id'], cust_id=acc['cust_id']))
    return render_template("transfer_funds.html", user=current_user,accDetails=accDetails)
    
# ----------- Loan -------------#
@views.route('/loan', methods=['GET', 'POST'])
@login_required
def loan():
    cur.execute('SELECT * from account a,holdby h,branch b,customer c where b.branch_id=a.branch_id AND a.account_no=h.account_no AND h.cust_id={}'.format(current_user.id))
    accs=cur.fetchall()
    accDetails=[]
    for acc in accs:
        accDetails.append([Account(branch_name=acc['branch_name'],account_no=acc['account_no'], account_type=acc['account_type'], balance=acc['balance'], branch_id=acc['branch_id'], cust_id=acc['cust_id']),
                           Customer(name=acc['name'],email=acc['email'],address=acc['address'],phone=acc['phone'],dob=acc['dob'],sex=acc['sex'],occupation=acc['occupation'])])
    f=open("output.txt",'w')
    f.write("{}".format((accDetails[0][1]).address))
    f.close()
    return render_template("loan.html", user=current_user,accDetails=accDetails)