from werkzeug.security import check_password_hash

class User:
    def __init__(self,username,email,password) -> None:
        self.username=username
        self.email=email
        self.password=password
    def is_authenticated():
        return True
    def is_active():
        return True
    def is_anonymous():
        return True
    def get_id(self):
        return self.username
    def check_password(self,input_password):
        return check_password_hash(self.password,input_password)