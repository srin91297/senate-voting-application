# imports
from app import app, mongo
from flask import Flask, flash, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import cgi

@app.route('/vote', methods=['POST', 'GET'])

def vote():
    if request.method == 'GET':
        return render_template('vote.html')
    if request.method == 'POST':
        votes = mongo2.db.votes


    return '404'