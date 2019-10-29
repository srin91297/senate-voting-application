# imports
from app import app, common, admin
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from models.candidate import Candidate
from models.party import Party
from math import ceil
import bcrypt

MAX_ENTRIES = 10 # Set the maximum entries on discussion board page to this value

def get_max_page():
    total = len(Candidate().getAll(common))
    if total == 0:
        total = 1
    return ceil(total/MAX_ENTRIES)

def prep_data(page_num, ):
    data = Candidate().getAll(common)
    total = len(data)
    res = []
    i = 0
    for x in data:
        res.append([x,i])
        i = i + 1
    upper = page_num * MAX_ENTRIES
    upper = upper if upper <= total else total
    lower = page_num * MAX_ENTRIES - 10
    #print(upper, lower)
    res = res[lower:upper]
    return [res,total,len(res)]

@app.route('/admindashboard', methods=['GET'])
def admindashboard():
    if request.method == "GET":
        if 'username' in session:
            #return 'You are logged in as ' + session['username']
            return render_template('admindashboard.html')
        else:
            return render_template('login.html')

@app.route('/admindashboard/candidates/<int:page>', methods=['GET', 'POST'])
def candidates(page):
    if 'username' in session:
        if request.method == "GET":
            max_pages = get_max_page()
            if page > max_pages:
                return redirect(url_for('candidates',page=str(max_pages)))
            if page < 1:
                return redirect(url_for('candidates',page=str(1)))
        if request.method == "POST":
            # data = [name, location, party
            #create obj
            obj = {
                'name':request.values.get('name'),
                'location':request.values.get('location'),
                'party':request.values.get('party')
            }
            print(obj)
            candidate = Candidate().create(common, obj)
            print(candidate)
            return redirect(url_for('candidates',page=str(page)))
        res = prep_data(page)
        total_entries = res[1]
        current_entries = res[2]
        return render_template('candidates.html', data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return render_template('login.html')

@app.route('/admindashboard/candidates/<int:page>/edit/<string:candid>', methods=["GET", "POST"])
def candidates_edit(page, candid):
    if request.method == "POST":
        #update candidate
        data = [request.values.get('name'), request.values.get('location'), request.values.get('party'), candid]
        Candidate().update(common, data)
        return redirect(url_for('candidates', page=page))

@app.route('/admindashboard/candidates/<int:page>/delete/<string:candid>', methods=["GET", "POST"])
def candidates_delete(page, candid):
    if request.method == "POST":
        #Delete candidate
        Candidate().delete(common, candid)
        return redirect(url_for('candidates', page=page))