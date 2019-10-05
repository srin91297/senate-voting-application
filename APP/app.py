from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Login'
app.config['MONGO_URI'] = 'mongodb+srv://ssegroup2:MghlwoCbDqaav9Yc@ssegroup2-vksod.mongodb.net/users?retryWrites=true&w=majority'

mongo = PyMongo(app)

app.secret_key = 'mysecret'

if __name__=='__main__':
    # app.secret_key = 'mysecret'
    from controller_login import *
    from controller_index import *
    from controller_register import *
    app.run(debug=True)
