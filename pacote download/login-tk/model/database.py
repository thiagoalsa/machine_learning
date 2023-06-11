import pandas as pd

class LoginModel:
    def __init__(self):
        self.users = {
            "admin": "admin",
            "user1": "password1",
            "user2": "password2"
        }

    def verify_credentials(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        return False

class HistoricModel():
    historic = pd.DataFrame(({"admin": "admin",
            "user1": "password1",
            "user2": "password2"}), index=[0])
