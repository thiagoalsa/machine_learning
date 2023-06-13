import customtkinter as ctk
import tkinter.ttk as tkk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from CTkMessagebox import CTkMessagebox
from time import sleep
from model.database import HistoricModel
#import mysql.connector


class LoginView:
    def __init__(self, controller):
        self.controller = controller

        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title("Login")

        self.root.geometry('320x320')

        # Create a username Label
        self.username_label = ctk.CTkLabel(self.root, text="Username:")
        self.username_label.pack()

        # Create a username input
        self.username_entry = ctk.CTkEntry(self.root, placeholder_text='example@gmail.com')
        self.username_entry.pack(padx=10, pady=10)

        # Create a password label
        self.password_label = ctk.CTkLabel(self.root, text="Password:")
        self.password_label.pack()

        # Create a password input
        self.password_entry = ctk.CTkEntry(self.root, show="*", placeholder_text='your password')
        self.password_entry.pack(padx=10, pady=10)

        # Create a checkbox
        self.checkbox = ctk.CTkCheckBox(self.root, text='Remember Password')
        self.checkbox.pack(padx=10, pady=10)

        # Create a Button
        self.login_button = ctk.CTkButton(self.root, text="Login", command=self.login)
        self.login_button.pack(padx=10, pady=10)

    def show_successful(self):
        self.app = App()
        self.app.run()


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            self.empty_label = ctk.CTkLabel(self.root, text="ERROR! Please fill in all fields.",
                                            text_color='yellow',
                                            )
            self.empty_label.pack()
        else:
            self.controller.login(username, password)

    def show_error(self):
        # Show some error message
        CTkMessagebox(title="Error", message="Something went wrong!!! Check your username and your password",
                      icon="cancel")

    def run(self):
        self.root.mainloop()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Machine Learning")
        self.geometry(f"{320}x{420}")
        self.pack_propagate(False)


        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme("green")

        self.logo_label = ctk.CTkLabel(self, text="Machine Learning",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack()

        self.frame_ml = ctk.CTkFrame(self)
        self.frame_ml.pack()

        self.mt5_data = HistoricModel.open_mt5(self)

        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.pack()
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self,
                                                             values=["Light", "Dark"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack()

    def run(self):
        self.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)


