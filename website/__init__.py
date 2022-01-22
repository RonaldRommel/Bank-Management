from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import yaml
from flask_mysqldb import MySQL
import MySQLdb.cursors
from .models import User 

# db = SQLAlchemy()
import mysql.connector

mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='dbmsproject01',
    )
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' 
    
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    
    cur=mydb.cursor()
    
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        cur.execute("select cust_id,email,password from customer where cust_id={}".format(id)) 
        res=cur.fetchone()
        if res==None:
            return None
        else:
            return User(id=res[0],email=res[1],password=res[2])
    return app

