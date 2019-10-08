# imports
from app import app, mongo
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
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
                
        #show message of incorrect details
        return render_template('login.html', mess='Incorrect login details entered')
    
    if request.method == "GET":
        return render_template('login.html')
    