# imports
from app import app, common, admin
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from app import *
from models.user import User
import bcrypt
import cgi

@app.route('/login', methods=['POST', 'GET'])

def login():
    if request.method == "POST":
        users = admin.users

        #server side validaton
        transform_username = cgi.escape(request.form['username'])
        transform_password = cgi.escape(request.form['pass'])
        if transform_username  != request.form['username'] or transform_password  != request.form['pass']:
            #wrong characters entered
            return render_template('login.html', mess='Malicious characters entered')
        
        #check fields entered are not empty
        if transform_password == "" or transform_username == "":
            return render_template('login.html', mess='Must fill in all fields!')  

        login_user = users.find_one({'name' : request.form['username']})


        if login_user:
            if (request.form['pass'], login_user['password'] == login_user['password']):
                session['username'] = request.form['username']
                session['role'] = login_user['role']
                if(login_user['role'] == "admin"):
                    return redirect(url_for('candidates', page=1))
            else:
                #show message of incorrect details
                return render_template('login.html', mess='Incorrect login details entered')

        return render_template('login.html', mess='Incorrect login details entered')
    
    if request.method == "GET":
        return render_template('login.html')
    
    return render_template('index.html')

#load user for the login manager auth
@login_manager.user_loader
def load_user(user_id):
	if user_id is None:
		return None
	return User.query.get(int(user_id))
    