from website import create_app
from flask import Flask
from flask_mysqldb import MySQL
import yaml 

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
