# imports
from app import app
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

@app.route('/voterdashboard', methods=['GET'])
def voterdashboard():
    if request.method == "GET":
        if 'username' in session and session['role'] == 'voter')::
            #return 'You are logged in as ' + session['username']
            return render_template('voterdashboard.html')
        else:
            return redirect(url_for('logout'))