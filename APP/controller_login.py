# imports
from app import app, mongo
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from app import *
from models.user import User
import bcrypt


@app.route('/login', methods=['POST', 'GET'])

def login():
    if request.method == "POST":
            
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if (request.form['pass'], login_user['password'] == login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('index'))

        return 'Invalid username/password combination'
    
    if request.method == "GET":
        print("GETTING")
        return render_template('login.html')
    
    return render_template('index.html')

#load user for the login manager auth
@login_manager.user_loader
def load_user(self, user_id):
	if user_id is None:
		return None
	return self.get_id()
    