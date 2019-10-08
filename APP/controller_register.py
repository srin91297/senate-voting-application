# imports
from app import app, mongo
from flask import Flask, flash, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

@app.route('/register', methods=['POST', 'GET'])

def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        
        #checking if user exists in db
        if existing_user is None:
            #add user
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            # session['username'] = request.form['username']
            # flash('user successfully created')
            return render_template('login.html', mess='user successfully created')

        #already exists
        flash('That user already exists!')
        return render_template('register.html')   

    if request.method == "GET":
        return render_template('register.html')

    return '404'