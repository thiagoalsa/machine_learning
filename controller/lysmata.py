import tkinter as tk
'''
class NewprojectApp:
    def __init__(self):
        # build ui
        toplevel1 = tk.Tk()
        toplevel1.configure(background="#FF6666", height=545, width=860)
        toplevel1.geometry("640x480")
        toplevel1.overrideredirect("false")
        toplevel1.pack_propagate(False)
        frame2 = tk.Frame(toplevel1)
        frame2.configure(
            background="#2B2B2B",
            borderwidth=20,
            height=480,
            width=340)
        label5 = tk.Label(frame2)
        label5.configure(
            background="#2B2B2B",
            font="{Calibri} 48 {bold italic}",
            foreground="#ffffff",
            justify="left",
            text='Lysmatta')
        label5.place(anchor="nw", relx=0.14, rely=0.25, x=0, y=0)
        frame2.grid(column=0, columnspan=2, row=0, rowspan=6, sticky="nsew")
        self.login = tk.Label(toplevel1)
        self.login.configure(
            background="#FF6666",
            font="{Calibri} 20 {bold italic}",
            text='Login')
        self.login.place(anchor="nw", relx=0.56, rely=0.21, x=0, y=0)
        self.entry_login = tk.Entry(toplevel1)
        self.entry_login.configure(background="#2B2B2B", foreground="#ffffff")
        self.entry_login.place(
            anchor="nw",
            height=30,
            relx=0.56,
            rely=0.31,
            width=225,
            x=0,
            y=0)
        self.password = tk.Label(toplevel1)
        self.password.configure(
            background="#FF6666",
            font="{Calibri} 20 {bold italic}",
            text='Password')
        self.password.place(anchor="nw", relx=0.56, rely=0.41, x=0, y=0)
        self.entry_password = tk.Entry(toplevel1)
        self.entry_password.configure(
            background="#2B2B2B",
            foreground="#ffffff",
            show="•")
        self.entry_password.place(
            anchor="nw",
            height=30,
            relx=0.56,
            rely=0.51,
            width=225,
            x=0,
            y=0)
        button1 = tk.Button(toplevel1, command=self.login)
        button1.configure(
            activebackground="#FF8989",
            background="#2B2B2B",
            font="{Calibri} 24 {bold italic}",
            foreground="#ffffff",
            justify="left",
            relief="raised",
            text='Login')
        button1.place(anchor="nw", relx=0.68, rely=0.64, x=0, y=0)
        toplevel1.grid_propagate(0)

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = NewprojectApp()
    app.run()
'''
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

def collect_historic(date_start=None,
                     date_finish=None,
                     ):
    # start MT5
    mt5.initialize()

    # create start and end date
    from_date = datetime(2000, 1, 1)
    to_date = datetime.now()

    # collect history data
    historic = mt5.history_deals_get(from_date, to_date)

    # create a DataFrame pandas

    df_historic = pd.DataFrame(list(historic), columns=historic[0]._asdict().keys())
    print(df_historic)


collect_historic()