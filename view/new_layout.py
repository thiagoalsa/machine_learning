import customtkinter as ctk
import tkinter.ttk as tkk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from model import collectdata

class App:
    def __init__(self):
        # configure window
        self.root = ctk.CTk()
        self.root.title("Lysmata | Machine Learning")
        ctk.set_appearance_mode('dark')

#############################################

        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=0)
        self.root.rowconfigure((0, 2), weight=1)

###############################################
        # create a styling
        self.style = ttk.Style()
        self.style.configure('leftFrame.TFrame', background='#3F3F44')
        self.style.configure('positionFrame.TFrame', background='white')
        self.style.configure('historicFrame.TFrame', background='white')
        self.style.configure('topFrame.TFrame', background='white')

##############################################
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, height=700, corner_radius=30)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='NSEW')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # create open file button
        self.file_button = ctk.CTkButton(self.sidebar_frame,
                                         border_width=2,
                                         text='Open File',
                                         fg_color='#FF6666',
                                         hover_color='#FF8989',
                                         command=self.open_file)
        self.file_button.grid(row=5, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

###########################################
        # create a frame for position
        self.position_frame = ctk.CTkFrame(self.root, width=900, height=150, corner_radius=30)
        self.position_frame.grid(row=0, column=1, columnspan=5, sticky='NWE', padx=5, pady=5)

###########################################
        # create a frame for historic
        self.historic_frame = ctk.CTkFrame(self.root, width=900, height=250, corner_radius=30)
        self.historic_frame.grid(row=3, column=1, columnspan=3, sticky='SEW', padx=5, pady=5)

        self.tree_frame = ctk.CTkFrame(self.historic_frame, width=900, height=250, corner_radius=5, fg_color='#FF6666')
        self.tree_frame.pack(pady=10, padx=10)

        # create a scroll bar for historic treeview
        self.scrollbar_y = Scrollbar(self.tree_frame, orient=VERTICAL)
        self.scrollbar_y.pack(side=RIGHT, fill=Y, pady=3, padx=3)
        self.scrollbar_x = Scrollbar(self.tree_frame, orient=HORIZONTAL)
        self.scrollbar_x.pack(side=BOTTOM, fill=X, pady=3, padx=1)

        # Treeview
        self.my_tree = ttk.Treeview(self.tree_frame)
        self.my_tree.pack()
        self.my_tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.my_tree.configure(yscrollcommand=self.scrollbar_y.set)
        self.my_tree.configure(selectmode='extended')
        self.scrollbar_x.configure(command=self.my_tree.xview)
        self.scrollbar_y.configure(command=self.my_tree.yview)

        # hack the column height
        self.my_tree.heading('#0', text='\n')

        # set treeview style
        style = ttk.Style()
        style.theme_use('default')

        # change style colors
        style.configure('Treeview',
                        background='#FFEADD',
                        foreground='blue',
                        rowheight=25,
                        fieldbackground='#2B2B2B',
                        font=('Calibri', 11)
                        )

        # change color of headers
        style.configure('Treeview.Heading',
                        background='#FF6666',
                        foreground='white',
                        font=('Calibri', 13, 'bold')
                        )
        self.style.layout("historic.Treeview",
                          [('historic.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        # change color of selected row
        style.map('Treeview', background=[('selected', 'gray')])

###########################################
        # create a frame for column graph
        self.acuracy_frame1 = ctk.CTkFrame(self.root, width=900, height=300, corner_radius=30)
        self.acuracy_frame1.grid(row=1, column=1, rowspan=2, columnspan=2, pady=5, padx=10, sticky='WE')
        self.acuracy_frame1.columnconfigure(0, weight=1)

        self.columngraph_frame = ctk.CTkFrame(self.acuracy_frame1, width=600, height=290, corner_radius=30)
        self.columngraph_frame.grid(column=0, columnspan=1, row=0, rowspan=1, pady=10, padx=10, sticky='NSWE')
        self.pizzagraph_frame = ctk.CTkFrame(self.acuracy_frame1, width=300, height=290, corner_radius=30)
        self.pizzagraph_frame.grid(column=2, row=0, rowspan=1, pady=10, padx=10, sticky='E')
###########################################
        # create a frame for
        self.acuracy_frame2 = ctk.CTkFrame(self.root, width=250, height=150, corner_radius=30)
        self.acuracy_frame2.grid(row=1, column=3, pady=10, padx=10, sticky='N')
###########################################
        # create a frame for
        self.acuracy_frame3 = ctk.CTkFrame(self.root, width=250, height=150, corner_radius=30)
        self.acuracy_frame3.grid(row=2, column=3, pady=10, padx=10, sticky='N')

###########################################
        # create a frame for
        self.acuracy_frame4 = ctk.CTkFrame(self.root, width=250, height=150, corner_radius=30)
        self.acuracy_frame4.grid(row=1, column=4, pady=10, padx=10, sticky='N')
###########################################
        # create a frame for
        self.acuracy_frame5 = ctk.CTkFrame(self.root, width=250, height=150, corner_radius=30)
        self.acuracy_frame5.grid(row=2, column=4, pady=10, padx=10, sticky='N')

##########################################
        # create a loss frame
        self.loss_frame = ctk.CTkFrame(self.root, width=200, height=100, corner_radius=30)
        self.loss_frame.grid(row=3, column=4, pady=10, padx=10, sticky='NSWE')
        self.loss_label = ctk.CTkLabel(self.loss_frame, text='Loss $-10', font=('Calibri', 50))
        self.loss_label.pack(pady=10, padx=10)


        self.root.mainloop()

    def open_file(self):
        # open a file
        my_file = filedialog.askopenfilename(title='Open File',
                                                  filetypes=(('Excel Files', '.xlsx'), ('ALL Files', '*.*'))
                                                  )
        # grab the file
        try:
            # create a dataframe
            df = pd.read_excel(my_file)
            # clean data for use in treeview
            df_tree = collectdata.DataView().clean_customer(df)
            # clean data for use in graph historic
            df_hist_graph = collectdata.DataView().clean_graph_deals(df)

            #display datas
            self.display_dataframe_in_treeview(df_tree)
            self.draw_plot(df_hist_graph)

        except Exception as e:
            messagebox.showerror('Error', e)

    def display_dataframe_in_treeview(self, df):
            # Clear the treeview
            self.my_tree.delete(*self.my_tree.get_children())

            # get the headers
            self.my_tree['column'] = list(df)
            self.my_tree['show'] = 'headings'

            # show the headers
            for col in self.my_tree['column']:
                self.my_tree.heading(col, text=col)

            # show data
            df = df.to_numpy().tolist()
            for row in df:
                self.my_tree.insert('', 'end', values=row)

    def draw_plot(self, df):
        fig, ax = plt.subplots()
        ax.plot(df)
        ax.axhline(y=df[0], color='red', linestyle='--', label=f'Initial Balance {df[0]:.2f}')
        ax.set_xlabel('Data Points')
        ax.set_ylabel('Values')
        ax.set_title('Historic Graph')
        ax.legend()
        ax.grid(True)

        # Embed the plot in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.columngraph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=10)


a = App()