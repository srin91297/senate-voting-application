# imports
from app import app, common, admin
from flask import Flask, render_template, url_for, request, session, redirect
from flask_login import logout_user
from flask_pymongo import PyMongo
from app import *
from models.user import User
import bcrypt
import cgi

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))