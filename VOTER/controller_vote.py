# imports
from app import app, mongo, common
from flask import Flask, flash, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import cgi

#def sorter(e):
    #return e['name']

@app.route('/vote', methods=['POST', 'GET'])

def vote():
    parties=common.db.party.find()
    if request.method == 'GET':
        return render_template('vote.html', parties=parties)
    if request.method == 'POST':
        votes = common.db.votes
        count=parties.count()
        value=[None]*count
        for i in parties:
            if(request.form[i['name']] != ''):
                x=({i['name']: request.form[i['name']]})
                value[int(request.form[i['name']])-1] = i['name']
        
        for j in range(0,5):
            if (value[j] == None):
                return render_template('voterdashboard.html')
        votes.insert({'vote': value})
        return render_template('voterdashboard.html')


    return '404'