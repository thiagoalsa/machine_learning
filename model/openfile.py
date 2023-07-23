from tkinter import *
import customtkinter as ctk
import numpy as np
import pandas as pd
from tkinter import ttk, filedialog, messagebox


root = ctk.CTk()

root.title('Lysmata | Machine Learning')
root.geometry('900x400')


def open_file():
    # open a file
    my_file = filedialog.askopenfilename(title='Open File',
                                         filetypes=(('Excel Files', '.xlsx'),
                                                    ('ALL Files', '*.*'))
                                         )
    # grab the file
    try:
        # create a dataframe

        historic_df = pd.read_excel(my_file)
        print(historic_df)

    except Exception as e:
        messagebox.showerror('Error', e)

    # Clear the treeview
    my_tree.delete(*my_tree.get_children())

    # get the headers
    my_tree['column'] = list(historic_df.columns)
    my_tree['show'] = 'headings'

    # show the headers
    for col in my_tree['column']:
        my_tree.heading(col, text=col)

    # show data
    historic_df_rows = historic_df.to_numpy().tolist()
    for row in historic_df_rows:
        my_tree.insert('', 'end', values=row)


#Treeview
my_tree = ttk.Treeview(root)
my_tree.pack(pady=20)

# hack the column height
my_tree.heading('#0', text='\n')

# set treeview style
style = ttk.Style()
style.theme_use('default')

# change style colors
style.configure('Treeview',
                background='#FFEADD',
                foreground='blue',
                rowheight=25,
                fieldbackground='green'
                )

# change color of headers
style.configure('Treeview.Heading',
                background='orange',
                foreground='blue'
                )

# change color of selected row
style.map('Treeview', background=[('selected', 'gray')])

#Button
my_button = ctk.CTkButton(root, text='OpenFile', command=open_file)
my_button.pack(pady=20)

root.mainloop()