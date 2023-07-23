import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
from tkinter import messagebox
from datetime import datetime
import view.view


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


class HistoricModel:
    def get_position_customer(self):
        # Initialize MT5
        mt5.initialize()

        # Collect positions data
        self.positions = mt5.positions_get()

        # create a pandas DataFrame
        if len(self.positions) > 0:
            self.positions_df = pd.DataFrame(list(self.positions), columns=self.positions[0]._asdict().keys())
            self.columns_selected = ['time', 'price_open', 'type', 'sl', 'tp']
            self.positions_df = self.positions_df.filter(items=self.columns_selected)

            # change column 'time' in int
            self.positions_df['time'] = pd.to_datetime(self.positions_df['time'], unit='s')
            self.positions_df['time'] = self.positions_df['time'].dt.time
            self.positions_df['time'] = self.positions_df['time'].item().strftime('%H%M%S')
            return self.positions_df
        else:
            messagebox.showerror('Error!', 'There is no open position')

    def get_historic_customer(self):
        # Initialize MT5
        mt5.initialize()

        # create a date the orders are requested from
        self.from_date = datetime(2022, 1, 1)
        self.to_date = datetime.now()

        # Collect historic data
        self.historic = mt5.history_orders_get(self.from_date, self.to_date)

        # create a historic DataFrame
        self.historic_df = pd.DataFrame(list(self.historic), columns=self.historic[0]._asdict().keys())
        self.historic_df['time_setup'] = pd.to_datetime(self.historic_df['time_setup'], unit='s')
        self.historic_df['time_setup_msc'] = pd.to_datetime(self.historic_df['time_setup_msc'], unit='ns')
        self.historic_df['time_done'] = pd.to_datetime(self.historic_df['time_done'], unit='s')
        self.historic_df['time_done_msc'] = pd.to_datetime(self.historic_df['time_done_msc'], unit='ns')
        return self.historic_df
