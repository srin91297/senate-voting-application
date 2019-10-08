# imports
from app import app, mongo
from flask import Flask, flash, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import cgi

@app.route('/register', methods=['POST', 'GET'])

def register():
    if request.method == 'POST':
        users = mongo.db.users

        #server side validaton
        transform_username = cgi.escape(request.form['username'])
        transform_password = cgi.escape(request.form['pass'])
        if transform_username  != request.form['username'] or transform_password  != request.form['pass']:
            #wrong characters entered
            flash('Malicious characters entered')
            return render_template('register.html')  

        existing_user = users.find_one({'name' : request.form['username']})
        
        #check fields entered are not empty
        if transform_password == "" or transform_username == "":
            flash('Must fill in all fields!')
            return render_template('register.html')            

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