from datetime import datetime
from bson.objectid import ObjectId

class State:

	# Input:
	# id
	# Output:
	# returns object
	def get(self, db):
		s = db.state
		rec = s.find()
		return rec

	# Input: 
	# data = [state]
	# Output:
	# returns the newly created object
	def create(self, db):
		s = db.state
		res =  s.insert({"state":"Set Up"})
		return s.find({"_id":res})

	# # Input: 
	# # data = [state]
	# # Output:
	# # returns the newly created object
	def update_state(self, db):
		s = db.state
		rec = s.find()
		state = ""
		for each in rec:
			if(each["state"]=="Set Up"):
				state = "Voting"
			if(each["state"]=="Voting"):
				state = "Results"
			s.update_one(
			{
				"_id":ObjectId(each["_id"])
			}, 
			{
				"$set": {"state":state}
			},
			upsert=False
			)      
