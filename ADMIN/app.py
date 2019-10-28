from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_login import LoginManager
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Login'
app.config['MONGO_URI'] = 'mongodb+srv://ssegroup2:MghlwoCbDqaav9Yc@ssegroup2-vksod.mongodb.net/admins?retryWrites=true&w=majority'

#flask-login stuff
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'

db = PyMongo(app).db

app.secret_key = 'mysecret'

if __name__=='__main__':
    # app.secret_key = 'mysecret'
    from controller_login import *
    from controller_index import *
    from controller_register import *
    from controller_logout import *
    from controller_admindashboard import *
    app.run(debug=True)
