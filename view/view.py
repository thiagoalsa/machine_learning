import CTkMessagebox
import customtkinter as ctk
import tkinter.ttk as tkk
from tkinter import *
from tkinter import ttk
import model.database
from model.database import *
from model.brain import Brain
#from exemplo import AccuracyHistoric

class LoginView:
    def __init__(self, controller):
        self.controller = controller

        self.root = ctk.CTk()
        self.root.title("Lysmata | Login")
        self.root.geometry('300x300')
        self.root.pack_propagate(False)
        self.root.configure(bg='#2B2B2B')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("green")

        # create a logo Label
        self.logo_label = ctk.CTkLabel(self.root, text='Lysmatta', font=('Calibri', 50, 'bold'))
        self.logo_label.pack(pady=10)

        # Create a username Label
        self.username_label = ctk.CTkLabel(self.root, text="Username:", font=('Calibri', 15, 'bold'))
        self.username_label.pack()

        # Create a username input
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.pack(padx=10, pady=10)

        # Create a password label
        self.password_label = ctk.CTkLabel(self.root, text="Password:", font=('Calibri', 15, 'bold'))
        self.password_label.pack()

        # Create a password input
        self.password_entry = ctk.CTkEntry(self.root, show="*")
        self.password_entry.pack(padx=10, pady=10)

        # Create a Button
        self.login_button = ctk.CTkButton(self.root, text="Login", command=self.login)
        self.login_button.pack(padx=10, pady=10)

    def show_successful(self):
        messagebox.showinfo('Lysmata', 'Login successfully!')
        self.root.destroy()
        self.app = App()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showinfo('Login', 'Missing credentials. Please try again.')
        else:
            self.controller.login(username, password)

    def show_error(self):
        # Show some error message
        messagebox.showerror('Login', 'Incorrect credentials. Please try again.')

    def run(self):
        self.root.mainloop()


class App:
    def __init__(self):
        # configure window
        self.root = ctk.CTk()
        self.root.title("Machine Learning")
        self.root.geometry(f"{700}x{440}")
        self.root.pack_propagate(False)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

        # create a main Label logo Lysmatta
        self.logo_label = ctk.CTkLabel(self.root, text="Lysmata",
                                       font=('Calibri', 50, 'bold')
                                       )
        self.logo_label.pack()

########################################################################################################################
        self.acuracy_frame = ctk.CTkFrame(self.root, height=150, width=400, corner_radius=30)
        self.acuracy_frame.pack()


############################################################################################
    # create scrollable frame for position
        self.position_frame = ctk.CTkFrame(self.root, height=150, width=400, corner_radius=30)
        self.position_frame.pack()

    # create a get positions button
        self.position_button = ctk.CTkButton(self.position_frame, border_width=2,
                                             text='Get Positions',
                                             )
        self.position_button.pack(pady=10, padx=10)

############################################################################################

    # create a frame for historic
        self.historic_frame = ctk.CTkFrame(self.root, height=150, width=400, corner_radius=30)
        self.historic_frame.pack()
        self.position_button = ctk.CTkButton(self.historic_frame, border_width=2, text='Get Historic',
                                             )
        self.position_button.pack(pady=10, padx=10)

############################################################################################
        self.appearance_mode_label = ctk.CTkLabel(self.root, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.pack(pady=(10, 1))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.root,
                                                             values=["Light", "Dark"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(pady=(1, 30))

        self.root.mainloop()




    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
