from datetime import datetime
from bson.objectid import ObjectId

class Vote:
    # Input: 
    # data = [candid]
    # Output:
    # returns the newly created object
    def create(self, db, obj):
        vote = db.votes
        res =  vote.insert(obj)
        return vote.find({"_id":res})