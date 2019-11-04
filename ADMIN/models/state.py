from datetime import datetime
from bson.objectid import ObjectId

class State:
    def __init__(self):
        state = "Set Up"
    
    #changes states of the ADMIN user through if-else ladder statement
	def changeState(self):
		if getState() == "Set Up":
			state = "Voting"
            print(state)
		elif getState() == "Voting":
			state = "View Results"
            print(state)
		elif getState() == "View Results":
			state = "Voting"
            print(state)
			
	#simple getter to return user state	
	def getState(self):
		return state