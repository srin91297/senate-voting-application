# imports
from app import app
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

@app.route('/admindashboard', methods=['GET'])
def admindashboard():
    if request.method == "GET":
        if 'username' in session:
            #return 'You are logged in as ' + session['username']
            return render_template('admindashboard.html')
        else:
            return render_template('login.html')