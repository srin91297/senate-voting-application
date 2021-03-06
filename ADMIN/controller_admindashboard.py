# imports
from app import app, common, admin
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
from models.candidate import Candidate
from bson.objectid import ObjectId
from models.party import Party
from models.state import State
from models.vote import Vote
from math import ceil
import operator
import bcrypt
import re

MAX_ENTRIES = 10 # Set the maximum entries on discussion board page to this value

def stateChange():
    if 'username' in session:
        State().changeState
    return render_template('candidate.html', state = State().getState())

def get_max_page(type):
    if type == "Candidates":
        total = len(Candidate().getAll(common))
    elif type == "Parties":
        total = len(Party().getAll(common))
    elif type == "Results":
        total = len(Vote().getAll(common))
    if total == 0:
        total = 1
    return ceil(total/MAX_ENTRIES)

def prep_data(page_num, type):
    if type == "Candidates":
        data = Candidate().getAll(common)
    elif type == "Parties":
        data = Party().getAll(common)
    elif type == "Results":
        data = Vote().getAll(common)
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
        if 'username' in session and session['role'] == 'admin':
            #return 'You are logged in as ' + session['username']
            return render_template('admindashboard.html')
        else:
            return redirect(url_for('logout'))

@app.route('/admindashboard/candidates/<int:page>', methods=['GET', 'POST'])
def candidates(page):
    print(session)
    if 'username' in session and session['role'] == 'admin':
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
                #acceptable input do not flash
                candidate = Candidate().create(common, obj)
            else:
                #unacceptable input flash
                flash('Illegal Characters detected')
            return redirect(url_for('candidates',page=str(page)))
        res = prep_data(page, "Candidates")
        total_entries = res[1]
        current_entries = res[2]
        state = State().get(common)
        return render_template('candidates.html', state=state, data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return redirect(url_for('logout'))

@app.route('/admindashboard/candidates/<int:page>/edit/<string:candid>', methods=["GET", "POST"])
def candidates_edit(page, candid):
    if request.method == "POST":
        #update candidate
        data = [request.values.get('name'), request.values.get('in_party'), candid]
        #client-side validation
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if regex.search(data[0]) == None:
            #acceptable input dont flash
            Candidate().update(common, data)
        else:
            #unacceptable input need to flash
            flash('Illegal Characters detected')
        return redirect(url_for('candidates', page=page))

@app.route('/admindashboard/candidates/<int:page>/delete/<string:candid>', methods=["GET", "POST"])
def candidates_delete(page, candid):
    if request.method == "POST":
        #get candidate by id
        cand = Candidate().getbyid(common, candid)
        #Remove candidate from party if true
        if(cand[0]['in_party']=='true'):
            #search
            parties = Party().getAll(common)
            #form structure
            i = 0
            flag = False
            #get candidates from parties
            for party in parties:
                i = 0
                for cands in party[1]:
                    #check if cand is in party
                    if(str(cand[0]['_id']) == str(cands)):
                        currparty = party[1]
                        del currparty[i]
                        flag = True
                        #update party
                        Party().update_candidates(common, [currparty, party[2]])
                        break
                    i = i + 1
                flag = True
        #Delete candidate
        Candidate().delete(common, candid)
        return redirect(url_for('candidates', page=page))

@app.route('/admindashboard/parties/<int:page>', methods=['GET', 'POST'])
def parties(page):
    if 'username' in session and session['role'] == 'admin':
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
            #client-side validation
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if regex.search(obj.get('name')) == None:
                #acceptable input do not flash
                parties = Party().create(common, obj)
            else:
                #unacceptable input flash
                flash('Illegal Characters detected')
            return redirect(url_for('parties',page=str(page)))
        res = prep_data(page, "Parties")
        total_entries = res[1]
        current_entries = res[2]
        state = State().get(common)
        return render_template('parties.html', state=state, data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return redirect(url_for('logout'))

@app.route('/admindashboard/parties/<int:page>/edit/<string:partyid>', methods=["GET", "POST"])
def parties_edit(page, partyid):
    if request.method == "POST":
        #update party
        data = [request.values.get('name'), partyid]
        #client-side validation
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if regex.search(data[0]) == None and len(data[0]) > 1:
            #acceptable input dont flash
            Party().update_name(common, data)
        else:
            #unacceptable input need to flash
            flash('Illegal Characters detected')
        return redirect(url_for('parties', page=page))

@app.route('/admindashboard/parties/<int:page>/delete/<string:partyid>', methods=["GET", "POST"])
def parties_delete(page, partyid):
    if request.method == "POST":
        #Delete party
        Party().delete(common, partyid)
        return redirect(url_for('parties', page=page))

@app.route('/admindashboard/parties/<string:partyid>/candidates/<int:page>', methods=['GET', 'POST'])
def parties_candidateslist(partyid, page):
    if 'username' in session and session['role'] == 'admin':
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
        state = State().get(common)
        return render_template('partycandidatelist.html', state=state, cand_left=candidates_left, candidates = tmp, party = party[0], data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return redirect(url_for('logout'))

@app.route('/admindashboard/states', methods=['GET', 'POST'])
def states():
    if 'username' in session and session['role'] == 'admin':
        if request.method == "POST":
            #change state here
            State().update_state(common)
            return redirect(url_for('states'))
        #get state
        state = State().get(common)
        return render_template('state.html', state = state)
    else:
        return redirect(url_for('logout'))

@app.route('/admindashboard/parties/<string:partyid>/candidates/<int:page>/delete/<string:candid>', methods=["GET", "POST"])
def parties_candidateslist_delete(partyid, page, candid):
    if request.method == "POST":
        #get candidate by id
        cand = Candidate().getbyid(common, candid)
        #Remove candidate from party if true
        if(cand[0]['in_party']=='true'):
            #search
            parties = Party().getAll(common)
            #form structure
            i = 0
            flag = False
            #get candidates from parties
            for party in parties:
                i = 0
                for cands in party[1]:
                    #check if cand is in party
                    if(str(cand[0]['_id']) == str(cands)):
                        currparty = party[1]
                        del currparty[i]
                        flag = True
                        #update party
                        Party().update_candidates(common, [currparty, party[2]])
                        break
                    i = i + 1
                flag = True
            #update candidates party status
            Candidate().update_in_party(common, ['false', candid]) 
        return redirect(url_for('parties_candidateslist', partyid=partyid, page=page))

@app.route('/admindashboard/results/<int:page>', methods=['GET', 'POST'])
def results(page):
    if 'username' in session and session['role'] == 'admin':
        if request.method == "GET":
            max_pages = get_max_page("Results")
            if page > max_pages:
                return redirect(url_for('results',page=str(max_pages)))
            if page < 1:
                return redirect(url_for('results',page=str(1)))
        res = prep_data(page, "Results")
        total_entries = res[1]
        current_entries = res[2]
        #calculate here
        #get all the votes
        votes = Vote().getAll(common)
        #flatten list
        votestest = []
        i = 0
        for v in votes:
            for item in v:
                if i % 2 == 0:
                    votestest.append(str(item))
                i = i + 1
        totalv = 0
        tmp = 0
        results = []
        print(votestest)
        votestestunique = [] 
        for num in votestest: 
            if num not in votestestunique: 
                votestestunique.append(num) 
        for vote in votestestunique:
            tmp = votestest.count(vote)
            totalv = totalv + tmp
            results.append([tmp, Candidate().getbyid(common, vote)])
        sort = sorted(results, key = operator.itemgetter(0), reverse=True)
        state = State().get(common)
        return render_template('results.html', state=state, results=sort, totalvotes=totalv, data = res[0], total = total_entries, current = current_entries, page_max = max_pages, current_page = page)
    else:
        return redirect(url_for('logout'))

    