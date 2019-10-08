# imports
from app import app
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

@app.route('/', methods=['GET'])

def index():
    if request.method == "GET":
        if 'username' in session:
            return 'You are logged in as ' + session['username']
        else:
            return render_template('login.html')