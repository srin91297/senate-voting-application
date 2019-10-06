class User():
	def _init__(self, id):
		self.id = id	#db user id
		
	def is_authenticated(self):
		return True
		
	def is_active(self):
		return True
		
	def is_anonymous(self):
		return False
		
	def get_id(self):
		return self.id