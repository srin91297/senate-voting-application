from datetime import datetime
from bson.objectid import ObjectId

class Candidate:
    # Input:
    # id
    # Output:
    # returns object
    def getbyid(self, db, id):
        candidate = db.candidate
        returnedcandidate = candidate.find({"_id":ObjectId(id)})
        return returnedcandidate

    # Input: 
    # data = [name, location, party]
    # Output:
    # returns the newly created object
    def create(self, db, obj):
        candidate = db.candidate
        res =  candidate.insert(obj)
        return candidate.find({"_id":res})

    # Input: 
    # data = [name, location, party, id]
    # Output:
    # updates a candidate at given id with data array
    def update(self, db, obj):
        candidate = db.candidate
        # res = post.find_one({"_id":data[8]})
        candidate.update_one(
            {
                "_id":ObjectId(obj[3])
            }, 
            {
                "$set": {"name":obj[0], "location":obj[1], "party":obj[2]}
            },
            upsert=False
            )

    # Input:
    # 
    # Output:
    # returns all the candidates in an array
    def getAll(self, db):
        candidate = db.candidate
        rec = candidate.find()
        data = []
        for each in rec:       
            tmp = []
            tmp.append(each["name"])
            tmp.append(each["location"])
            tmp.append(each["party"])
            tmp.append(each["_id"])
            data.append(tmp)
        return data
    
    # Input:
    # id of the candidate to be deleted
    # Output:
    # deletes candidate at the given id
    def delete(self, db, id):
        candidate = db.candidate
        candidate.delete_one({"_id":ObjectId(id)})