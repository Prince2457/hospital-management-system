class Users:
    def __init__(self, username, password, role, full_name, email=None, phone=None ):

        self.username = username
        self.password = password
        self.role = role
        self.full_name = full_name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f" Username:{self.username} | Role:{self.role} | Full Name:{self.full_name}"  
        