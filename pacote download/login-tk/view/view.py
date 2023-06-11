import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from CTkMessagebox import CTkMessagebox
from time import sleep
from model.database import HistoricModel


class LoginView:
    def __init__(self, controller):
        self.controller = controller

        ctk.set_appearance_mode('dark')

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
        App()

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
        self.geometry(f"{1100}x{580}")
        self.pack_propagate(False)
        self.resizable(0, 0)

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("green")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Machine Learning",
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.checkbox_1 = ctk.CTkCheckBox(master=self.sidebar_frame, text='Machine Learning')
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="nsew")


        # create main entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text="search")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = ctk.CTkButton(master=self, border_width=2, text='Search',
                                                     text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create scrollable frame #1
        self.scrollable_frame1 = ctk.CTkScrollableFrame(self, label_text="Historic MT5 - Machine Learning")
        self.scrollable_frame1.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.historic_label1 = ctk.CTkLabel(self.scrollable_frame1, text='OI')
        self.historic_label1.grid(row=0, column=0, padx=20, pady=(20, 10))


        # create scrollable frame #2
        self.scrollable_frame2 = ctk.CTkScrollableFrame(self, label_text="Historic MT5")
        self.scrollable_frame2.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        data = HistoricModel.historic
        self.historic_label2 = ctk.CTkLabel(self.scrollable_frame2, text=data)
        self.historic_label2.grid(row=0, column=0, padx=20, pady=(20, 10))




    def run(self):
        self.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

