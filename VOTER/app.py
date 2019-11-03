from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Login'

#flask-login stuff
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'

#flask wtf csrf stuff
csrf = CSRFProtect()
csrf.init_app(app)

mongo = PyMongo(app, uri = 'mongodb+srv://ssegroup2:MghlwoCbDqaav9Yc@ssegroup2-vksod.mongodb.net/voters?retryWrites=true&w=majority')
common = PyMongo(app, uri = 'mongodb+srv://ssegroup2:MghlwoCbDqaav9Yc@ssegroup2-vksod.mongodb.net/common?retryWrites=true&w=majority').db

app.secret_key = 'mysecret'

if __name__=='__main__':
    # app.secret_key = 'mysecret'
    from controller_login import *
    from controller_index import *
    from controller_register import *
    from controller_logout import *
    from controller_vote import *
    from controller_voterdashboard import *
    app.run(debug=True, port=5001)
