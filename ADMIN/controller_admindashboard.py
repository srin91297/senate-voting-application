# imports
from app import app, common, admin
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from models.candidate import Candidate
from models.party import Party
from math import ceil
import bcrypt
import re

MAX_ENTRIES = 10 # Set the maximum entries on discussion board page to this value

def get_max_page(type):
    if type == "Candidates":
        total = len(Candidate().getAll(common))
    elif type == "Parties":
        total = len(Party().getAll(common))
    if total == 0:
        total = 1
    return ceil(total/MAX_ENTRIES)

def prep_data(page_num, type):
    if type == "Candidates":
        data = Candidate().getAll(common)
    elif type == "Parties":
        data = Party().getAll(common)
    total = len(data)
    res = []
    i = 0
    for x in data:
        res.append([x,i])
        i = i + 1
    upper = page_num * MAX_ENTRIES
    upper = upper if upper <= total else total
    lower = page_num * MAX_ENTRIES - 10
    res = res[lower:upper]
    return [res,total,len(res)]

def get_max_page_party_candidate_list(partyid):
    party = Party().getbyid(common, partyid)
    #add candidate objects to array
    tmp = []
    for x in party[0]['candidates']:
        tmp.append(Candidate().getbyid(common, x))
    total = len(tmp)
    if total == 0:
        total = 1
    return ceil(total/MAX_ENTRIES)

def prep_data_party_candidate_list(page_num, partyid):
    data = Party().getbyid(common, partyid)
    #add candidate objects to array
    tmp = []
    for x in data[0]['candidates']:
        tmp.append(Candidate().getbyid(common, x))
    total = len(tmp)
    res = []
    i = 0
    for x in data:
        res.append([x,i])
        i = i + 1
    upper = page_num * MAX_ENTRIES
    upper = upper if upper <= total else total
    lower = page_num * MAX_ENTRIES - 10
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
            max_pages = get_max_page("Candidates")
            if page > max_pages:
                return redirect(url_for('candidates',page=str(max_pages)))
            if page < 1:
                return redirect(url_for('candidates',page=str(1)))
        if request.method == "POST":
            #create obj
            obj = {
                'name':request.values.get('name'),
                "in_party":"false"
            }
            #client-side validation
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if regex.search(obj.get('name')) == None:
                candidate = Candidate().create(common, obj)
            else:
                flash(u'Illegal characters detected!')
            return redirect(url_for('candidates',page=str(page)))
        res = prep_data(page, "Candidates")
        total_entries = res[1]
        current_entries = res[2]
        return render_template('candidates.html', data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return render_template('login.html')

@app.route('/admindashboard/candidates/<int:page>/edit/<string:candid>', methods=["GET", "POST"])
def candidates_edit(page, candid):
    if request.method == "POST":
        #update candidate
        data = [request.values.get('name'), request.values.get('in_party'), candid]
        Candidate().update(common, data)
        return redirect(url_for('candidates', page=page))

@app.route('/admindashboard/candidates/<int:page>/delete/<string:candid>', methods=["GET", "POST"])
def candidates_delete(page, candid):
    if request.method == "POST":
        #Delete candidate
        Candidate().delete(common, candid)
        return redirect(url_for('candidates', page=page))

@app.route('/admindashboard/parties/<int:page>', methods=['GET', 'POST'])
def parties(page):
    if 'username' in session:
        if request.method == "GET":
            max_pages = get_max_page("Parties")
            if page > max_pages:
                return redirect(url_for('parties',page=str(max_pages)))
            if page < 1:
                return redirect(url_for('parties',page=str(1)))
        if request.method == "POST":
            #create obj
            obj = {
                'name':request.values.get('name'),
                'candidates': [],
            }
            parties = Party().create(common, obj)
            return redirect(url_for('parties',page=str(page)))
        res = prep_data(page, "Parties")
        total_entries = res[1]
        current_entries = res[2]
        return render_template('parties.html', data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return render_template('login.html')

@app.route('/admindashboard/parties/<int:page>/edit/<string:partyid>', methods=["GET", "POST"])
def parties_edit(page, partyid):
    if request.method == "POST":
        #update party
        data = [request.values.get('name'), partyid]
        Party().update_name(common, data)
        return redirect(url_for('parties', page=page))

@app.route('/admindashboard/parties/<int:page>/delete/<string:partyid>', methods=["GET", "POST"])
def parties_delete(page, partyid):
    if request.method == "POST":
        #Delete party
        Party().delete(common, partyid)
        return redirect(url_for('parties', page=page))

@app.route('/admindashboard/parties/<string:partyid>/candidates/<int:page>', methods=['GET', 'POST'])
def parties_candidateslist(partyid, page):
    if 'username' in session:
        if request.method == "GET":
            max_pages = get_max_page_party_candidate_list(partyid)
            if page > max_pages:
                return redirect(url_for('parties_candidateslist', partyid=partyid, page=str(max_pages)))
            if page < 1:
                return redirect(url_for('parties_candidateslist', partyid=partyid, page=str(1)))
        if request.method == "POST":
            #get candidate and append to candidates array of party
            Candidate().update_in_party(common, ['true', request.values.get('candid')])
            party = Party().getbyid(common, partyid)
            tmp = party[0]['candidates']
            tmp.append(request.values.get('candid'))
            Party().update_candidates(common, [tmp, partyid])
            return redirect(url_for('parties_candidateslist', partyid=partyid, page=str(page)))
        res = prep_data_party_candidate_list(page, partyid)
        total_entries = res[1]
        current_entries = res[2]
        party = Party().getbyid(common, partyid)
        #add candidate objects to array
        tmp = []
        for x in party[0]['candidates']:
            tmp.append(Candidate().getbyid(common, x))
        #remove candidate that have already been in a party
        Allcandidates = Candidate().getAll(common)
        candidates_left = []
        for x in Allcandidates:
            if(x[1] == "false"):
                candidates_left.append(x)
        return render_template('partycandidatelist.html', cand_left=candidates_left, candidates = tmp, party = party[0], data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return render_template('login.html')

# @app.route('/admindashboard/parties/<int:page>/edit/<string:partyid>', methods=["GET", "POST"])
# def parties_edit(page, partyid):
#     if request.method == "POST":
#         #update party
#         data = [request.values.get('name'), partyid]
#         Party().update_name(common, data)
#         return redirect(url_for('parties', page=page))

# @app.route('/admindashboard/parties/<int:page>/delete/<string:partyid>', methods=["GET", "POST"])
# def parties_delete(page, partyid):
#     if request.method == "POST":
#         #Delete party
#         Party().delete(common, partyid)
#         return redirect(url_for('parties', page=page))