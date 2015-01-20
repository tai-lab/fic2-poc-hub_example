from flask.ext.login import UserMixin

class User(UserMixin):

    def __init__(self, d_user): 
        self.access_token = d_user['access_token']
        self.refresh_token = d_user['refresh_token']
        self.id = d_user['id']
