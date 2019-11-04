# imports
from app import app, mongo, common
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from models.candidate import Candidate
from models.party import Party
from models.vote import Vote
from math import ceil
import bcrypt

#def sorter(e):
    #return e['name']

@app.route('/voterdashboard/vote', methods=['POST', 'GET'])
def vote():
    parties = Party().getAll(common)
    candidates = Candidate().getAll(common)
    #form structure
    tmp = []
    below_line = []
    #get max length of candidates array in parties
    max = 0
    for party in parties:
        if(len(party[1]) > max):
            max = len(party[1])
    #get candidates from parties
    for party in parties:
        tmp = []
        for cands in party[1]:
            #add candidate objects to tmp array
            tmp.append(Candidate().getbyid(common, cands))
        below_line.append(tmp)
    flag = True
    array = []
    k = 0
    while(flag):
        if(k == max):
            flag = False
            continue
        tmp = []
        for i in range(0, len(below_line)):
            if(k<len(below_line[i])):
                tmp.append(below_line[i][k])
            else:
                tmp.append('-')
        array.append(tmp)
        k = k + 1
    if request.method == 'GET':
        return render_template('vote.html', parties=parties, candidates=array)
    if request.method == 'POST':
        #find who got voted 1st     
        #check below the line first
        candvoted = ''
        flag = False
        for row in array:
            for col in row:
                if(col != '-'):
                    # print(col[0]['_id'])
                    # print(request.values.get(str(col[0]['_id'])))
                    if(request.values.get(str(col[0]['_id'])) == '1'):
                        # print(col[0]['_id'])
                        candvoted = col[0]['_id']
                        # print("WENT HERE")
                        # print(candvoted)
                        flag = True
                        break
            if flag == True:
                break        
        # print(candvoted)
        # print(array)
        if(flag == False):
            k = 0
            for i in parties:
                if(request.values.get(str(i[2])) == '1'):
                    if(array[0][k] != '-'):
                        candvoted = array[0][k][0]['_id']
                    flag = True
                    break
                k = k + 1
        # print(candvoted)
        #create obj
        obj = {
            'candid':candvoted
        }
        vote = Vote().create(common, obj)
        return render_template('voterdashboard.html')

    return '404'