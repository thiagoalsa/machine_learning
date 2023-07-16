import customtkinter as ctk
import tkinter.ttk as tkk
from tkinter import *
from tkinter import filedialog, messagebox, ttk

class App:
    def __init__(self):
        # configure window
        self.root = ctk.CTk()
        self.root.title("Lysmata | Machine Learning")

########################################################################################################################

        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=0)
        self.root.rowconfigure((0, 2), weight=1)

########################################################################################################################
        # create a styling
        self.style = ttk.Style()
        self.style.configure('leftFrame.TFrame', background='#1D5D9B')
        self.style.configure('positionFrame.TFrame', background='#75C2F6')
        self.style.configure('historicFrame.TFrame', background='#F4D160')
        self.style.configure('topFrame.TFrame', background='#FBEEAC')

########################################################################################################################

        # create sidebar frame with widgets
        self.sidebar_frame = ttk.Frame(self.root, width=250, height=250, style='leftFrame.TFrame')
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky='NSEW')

########################################################################################################################

        # create a frame for position
        self.position_frame = ttk.Frame(self.root, width=900, height=100, style='positionFrame.TFrame')
        self.position_frame.grid(row=0, column=1, columnspan=5, sticky='NWE', padx=5, pady=5)

########################################################################################################################

        # create a frame for historic
        self.historic_frame = ttk.Frame(self.root, width=900, height=150, style='historicFrame.TFrame')
        self.historic_frame.grid(row=2, column=1, columnspan=5, sticky='SEW', padx=5, pady=5)

        

########################################################################################################################
        self.acuracy_frame = ttk.Frame(self.root, height=150, width=150, style='topFrame.TFrame')
        self.acuracy_frame.grid(row=1, column=2, pady=10, padx=10, sticky='N')

########################################################################################################################
        self.acuracy_frame = ttk.Frame(self.root, height=150, width=150, style='topFrame.TFrame')
        self.acuracy_frame.grid(row=1, column=3, pady=10, padx=10, sticky='N')

########################################################################################################################
        self.acuracy_frame = ttk.Frame(self.root, height=150, width=150, style='topFrame.TFrame')
        self.acuracy_frame.grid(row=1, column=4, pady=10, padx=10, sticky='N')

        self.root.mainloop()

a = App()