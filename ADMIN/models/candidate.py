from datetime import datetime
from bson.objectid import ObjectId

class Candidate:
    # Input:
    # id
    # Output:
    # returns object
    def getbyid(self, db, id):
        candidate = db.candidates
        returnedcandidate = candidate.find({"_id":ObjectId(id)})
        return returnedcandidate

    # Input: 
    # data = [name]
    # Output:
    # returns the newly created object
    def create(self, db, obj):
        candidate = db.candidates
        res =  candidate.insert(obj)
        return candidate.find({"_id":res})

    # Input: 
    # data = [name, id]
    # Output:
    # updates a candidate at given id with data array
    def update(self, db, obj):
        candidate = db.candidates
        candidate.update_one(
            {
                "_id":ObjectId(obj[1])
            }, 
            {
                "$set": {"name":obj[0]}
            },
            upsert=False
            )

    # Input:
    # 
    # Output:
    # returns all the candidates in an array
    def getAll(self, db):
        candidate = db.candidates
        rec = candidate.find()
        data = []
        for each in rec:       
            tmp = []
            tmp.append(each["name"])
            tmp.append(each["_id"])
            data.append(tmp)
        return data
    
    # Input:
    # id of the candidate to be deleted
    # Output:
    # deletes candidate at the given id
    def delete(self, db, id):
        candidate = db.candidates
        candidate.delete_one({"_id":ObjectId(id)})