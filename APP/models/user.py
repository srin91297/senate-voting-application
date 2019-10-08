from flask_login import UserMixin

#user class model
class User(UserMixin):
    def __init__(self, id):
        return id