# imports
from app import app, common, admin
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        if 'username' in session and session['role'] == 'admin':
            #return 'You are logged in as ' + session['username']
            return render_template('index.html')
        else:
            return redirect(url_for('logout'))