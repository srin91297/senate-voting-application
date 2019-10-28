from app import app, db
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from models.candidate import Candidate
from models.party import Party
from math import ceil
import bcrypt

# data = [name, location, party
#create obj
obj = {
    'name':'Srin',
    'location':'srin location',
    'party':'srin party'
}
candidate = Candidate().create(db, obj)

print(candidate)