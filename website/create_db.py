
# IN CMD
# mysql -u root -p
# create database database_name


import mysql.connector
import uuid

mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='dbmsproject01', # root_password
        database="bankapp",     # database_name
)

cur=mydb.cursor()

# cur.execute("Show tables")
# res=cur.fetchall()
# print(res)



cur.execute("create table bank (bank_code int AUTO_INCREMENT PRIMARY KEY,bank_name varchar(30))ENGINE=INNODB")
print("created table Bank")

cur.execute("create table branch (branch_id INT AUTO_INCREMENT PRIMARY KEY,branch_name varchar(30),bank_address varchar(100))ENGINE=INNODB")
print("created table Branch")

cur.execute("create table loan (loan_id INT AUTO_INCREMENT PRIMARY KEY,loan_type varchar(30),amount int,branch_id int ,index(branch_id),FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL)ENGINE=INNODB")
print("created table Loan")

cur.execute("create table account (account_no varchar(20) PRIMARY KEY,account_type varchar(30),balance int,branch_id int,index(branch_id),FOREIGN KEY (branch_id) REFERENCES branch(branch_id)  ON DELETE SET NULL)ENGINE=INNODB")
print("created table Account")

cur.execute("create table customer (cust_id int PRIMARY KEY,name varchar(30),phone varchar(20),address varchar(100),email varchar(30),password varchar(100),occupation varchar(30),sex varchar(10),dob date)ENGINE=INNODB")
print("created table Customer")

cur.execute("create table has (bank_code int,branch_id int,index(bank_code),index(branch_id),FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE CASCADE,FOREIGN KEY (bank_code) REFERENCES bank(bank_code) ON DELETE CASCADE,PRIMARY KEY(bank_code,branch_id))ENGINE=INNODB")
print("created table Has")

cur.execute("create table availedby (loan_id int,account_no varchar(20),index(loan_id),index(account_no),FOREIGN KEY (account_no) REFERENCES account(account_no) ON DELETE CASCADE,PRIMARY KEY(account_no,loan_id)) ENGINE=INNODB")
print("created table AvailedBy")

cur.execute("create table holdby (account_no varchar(20),index(account_no),cust_id int,index(cust_id),FOREIGN KEY (account_no) REFERENCES account(account_no) ON DELETE CASCADE ,FOREIGN KEY (cust_id) REFERENCES customer(cust_id) ON DELETE CASCADE,PRIMARY KEY(account_no,cust_id))ENGINE=INNODB")
print("created table HoldBy")

# -------inserting into bank--------------#
cur.execute("insert into bank(bank_name) values('Chamber Bank')")
mydb.commit()

# -------inserting branches--------------#

sql = "INSERT INTO branch (branch_name ,bank_address) VALUES (%s, %s)"
val = [
  ('Kalyan Nagar', 'Kalyan Nagar, near East point college Bengaluru- 560043'),
  ('Rammurthy nagar', 'Rammurthy nagar, TC palya main road Bengaluru- 560016'),
  ('Hoskote ', '21,Hoskote main road, Opp. To Bengaluru one Bengaluru - 560067'),
  ('HRBR', 'HRBR main road, Near Near tamarind restaurant  Bengaluru - 27'),
  ('Indranagar','28 Indranagar main road, Bengaluru- 560038')
]
cur.executemany(sql, val)
mydb.commit()

# -------inserting into has--------------#

cur.execute("Insert into has select bank_code,branch_id from bank,branch;")
mydb.commit()

print("Entered all data")