import customtkinter as ctk
import tkinter.ttk as tkk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from CTkMessagebox import CTkMessagebox
from time import sleep
import model.database
from model.database import *
from model.brain import Brain
import pandas as pd


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
        self.root.destroy()
        self.app = App()
        self.app.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            self.empty_label = ctk.CTkLabel(self.root, text="ERROR! Please fill in all fields.",
                                            text_color='red',
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


class App:
    def __init__(self):
        # configure window
        self.root = ctk.CTk()
        self.root.title("Machine Learning")
        self.root.geometry(f"{1200}x{740}")
        #self.root.pack_propagate(False)
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme("green")

        # configure grid layout (4x4)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Machine Learning",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                             values=["Light", "Dark"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # create main entry and button
        self.file_button = ctk.CTkButton(self.sidebar_frame, border_width=2, text='Open File',
                                         command=self.open_file_view)
        self.file_button.grid(row=5, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create scrollable frame for position
        self.scrollable_frame1 = ctk.CTkScrollableFrame(self.root,
                                                        label_text='Open Positions MT5',
                                                        label_font=('Arial', 25)
                                                        )
        self.scrollable_frame1.grid(row=1, column=1, padx=(5, 20), pady=(5, 20), sticky="nsew")

        # create a Treeview for position
        self.trv_position = tkk.Treeview(self.scrollable_frame1)
        self.trv_position.pack(pady=10)

        # create a get positions button
        self.get = model.database.HistoricModel()
        self.position_button = ctk.CTkButton(self.root, border_width=2, text='Get Positions', command=self.show_position)
        self.position_button.grid(row=2, column=1)

        # create a frame for historic
        self.frame2 = ctk.CTkFrame(self.root)
        self.frame2.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky='nsew')
        self.frame2_label = Label(self.frame2, text='Historic MT5', font=('Arial', 25))
        self.frame2_label.pack()

        # create a Treeview for historic
        self.trv_historic = tkk.Treeview(self.frame2)
        self.trv_historic.pack(pady=20)

        # create a scroll bar
        self.scrollbar_x = Scrollbar(self.frame2, orient=HORIZONTAL)
        self.scrollbar_y = Scrollbar(self.frame2, orient=VERTICAL)
        self.scrollbar_x.place(relx=0.002, rely=0.925, width=1040, height=25)
        self.scrollbar_y.place(relx=0.934, rely=0.128, width=22, height=423)
        self.trv_historic.configure(xscrollcommand=self.scrollbar_x.set)
        self.trv_historic.configure(yscrollcommand=self.scrollbar_y.set)
        self.trv_historic.configure(selectmode='extended')
        self.scrollbar_x.configure(command=self.trv_historic.xview)
        self.scrollbar_y.configure(command=self.trv_historic.yview)

        # create a get historic button
        self.get = model.database.HistoricModel()
        self.position_button = ctk.CTkButton(self.root, border_width=2, text='Get Historic',
                                             command=self.show_historic)
        self.position_button.grid(row=4, column=1, pady=20)

    def show_position(self):
        self.pos_data = model.database.HistoricModel()
        self.pos_data = self.pos_data.get_position()
        print(self.pos_data)
        # clean treeview
        self.trv_position.delete(*self.trv_position.get_children())

        # create a headers
        self.trv_position['column'] = list(self.pos_data.columns)
        self.trv_position['show'] = 'headings'

        # show headers
        for col in self.trv_position['column']:
            self.trv_position.heading(col, text=col)

        # show all data
        self.pos_rows = self.pos_data.to_numpy().tolist()
        for row in self.pos_rows:
            self.trv_position.insert('', 'end', values=row)

    def show_historic(self):
        self.pos_data = model.database.HistoricModel()
        self.pos_data = self.pos_data.get_historic()
        print(self.pos_data)
        # clean treeview
        self.trv_historic.delete(*self.trv_historic.get_children())

        # create a headers
        self.trv_historic['column'] = list(self.pos_data.columns)
        self.trv_historic['show'] = 'headings'

        # show headers
        for col in self.trv_historic['column']:
            self.trv_historic.heading(col, text=col)

        # show all data
        self.pos_rows = self.pos_data.to_numpy().tolist()
        for row in self.pos_rows:
            self.trv_historic.insert('', 'end', values=row)

    def open_file_view(self):
        self.load_file = Brain.open_file(self)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
