from datetime import datetime
from bson.objectid import ObjectId

class Vote:
    # Input:
    # 
    # Output:
    # returns all the votes in an array
    def getAll(self, db):
        vote = db.votes
        rec = vote.find()
        data = []
        for each in rec:       
            tmp = []
            tmp.append(each["candid"])
            tmp.append(each["_id"])
            data.append(tmp)
        return data