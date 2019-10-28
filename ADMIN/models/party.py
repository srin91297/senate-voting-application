from datetime import datetime
from bson.objectid import ObjectId

class Party:

    # Input: 
    # data = [name]
    # Output:
    # returns the newly created object
    def create(self, db, obj):
        party = db.party
        res =  party.insert(obj)
        return party.find({"_id":res})

    # Input:
    # 
    # Output:
    # returns all the party in an array
    def getAll(self, db):
        party = db.party
        rec = party.find()
        data = []
        for each in rec:       
            tmp = []
            tmp.append(each["name"])
            tmp.append(each["_id"])
            data.append(tmp)
        return data
    
    # Input:
    # id of the party to be deleted
    # Output:
    # deletes party at the given id
    def delete(self, db, id):
        party = db.party
        party.delete_one({"_id":ObjectId(id)})