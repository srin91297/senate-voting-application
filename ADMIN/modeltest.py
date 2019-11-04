from app import app, common
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from models.candidate import Candidate
from models.party import Party
from math import ceil
import bcrypt

#create obj
# for x in range(1, 19):    
#     obj = {
#         'name':'cand'+str(x),
#         'in_party':'false',
#     }
#     candidate = Candidate().create(common, obj) 


#create obj
for x in range(1, 7):    
    obj = {
        'name':'party'+str(x),
        'candidates':[],
    }
    party = Party().create(common, obj) 