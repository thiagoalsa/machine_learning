from model.database import *
from view.view import LoginView, App


class LoginController:
    def __init__(self):
        self.model = LoginModel()
        self.view = LoginView(self)

    def login(self, username, password):
        if self.model.verify_credentials(username, password):
            self.view.show_successful()

        else:
            self.view.show_error()

    def run(self):
        self.view.run()

if __name__ == "__main__":
    controller = LoginController()
    controller.run()
