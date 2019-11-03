from datetime import datetime
from bson.objectid import ObjectId

class Party:

    # Input:
    # id
    # Output:
    # returns object
    def getbyid(self, db, id):
        party = db.party
        returnedparty = party.find({"_id":ObjectId(id)})
        return returnedparty

    # Input: 
    # data = [name, candidates[]]
    # Output:
    # returns the newly created object
    def create(self, db, obj):
        party = db.party
        res =  party.insert(obj)
        return party.find({"_id":res})

    # Input: 
    # data = [name, id]
    # Output:
    # updates a party at given id with data array
    def update(self, db, obj):
        party = db.party
        party.update_one(
            {
                "_id":ObjectId(obj[1])
            }, 
            {
                "$set": {"name":obj[0]}
            },
            upsert=False
            )

    # Input: 
    # data = [name]
    # Output:
    # updates a party at given id with data array
    def update_name(self, db, obj):
        party = db.party
        party.update_one(
            {
                "_id":ObjectId(obj[1])
            }, 
            {
                "$set": {"name":obj[0]}
            },
            upsert=False
            )

    # Input: 
    # data = [candidates[], id]
    # Output:
    # updates a party at given id with data array
    def update_candidates(self, db, obj):
        party = db.party
        party.update_one(
            {
                "_id":ObjectId(obj[1])
            }, 
            {
                "$set": {"candidates":obj[0]}
            },
            upsert=False
            )

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
            tmp.append(each["candidates"])
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