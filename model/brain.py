import MetaTrader5 as mt5
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime
import numpy as np
from tkinter import ttk, filedialog, messagebox
from view import view


class Brain():
    # Create a close positions function
    def close_positions(self, symbol, volume, ticket, type_order, magic, deviation):
        if (type_order == 0):
            print('\033[41mORDEM FOI FECHADA\033[m')
            request_close = {
                'action': mt5.TRADE_ACTION_DEAL,
                'position': ticket,
                'symbol': symbol,
                'volume': volume,
                'deviation': deviation,
                'magic': magic,
                'type': mt5.ORDER_TYPE_SELL,
                'price': mt5.symbol_info_tick(symbol).bid,
                'type_time': mt5.ORDER_TIME_DAY,
                'type_filling': mt5.ORDER_FILLING_RETURN
            }

            result = mt5.order_send(request_close)
            print(result)
            print('-' * 50)

        else:
            print('\033[41mORDEM FOI FECHADA\033[m')
            request_close = {
                'action': mt5.TRADE_ACTION_DEAL,
                'position': ticket,
                'symbol': symbol,
                'volume': volume,
                'deviation': deviation,
                'magic': magic,
                'type': mt5.ORDER_TYPE_BUY,
                'price': mt5.symbol_info_tick(symbol).ask,
                'type_time': mt5.ORDER_TIME_DAY,
                'type_filling': mt5.ORDER_FILLING_RETURN
            }

            result = mt5.order_send(request_close)
            print(result)
            print('-' * 50)

    def collect_historic(self, date_start_y=2000,
                         date_start_m=1,
                         date_start_d=1,
                         date_finish_y=None,
                         date_finish_m=None,
                         date_finish_d=None):

        # start MT5
        self.mt5 = mt5.initialize()

        # create start and end date
        self.from_date = datetime(2022, 1, 1)
        self.to_date = datetime.now()

        # collect history data
        self.symbol = 'GBPUSD'
        self.historic = mt5.history_deals_get(self.from_date, self.to_date, group='*GBPUSD*')

        # create a DataFrame pandas

        self.df_historic = pd.DataFrame(list(self.historic), columns=self.historic[0]._asdict().keys())

        # Adjust the time format for viewing only
        self.df_historic_to_view = pd.DataFrame(list(self.historic), columns=self.historic[0]._asdict().keys())
        self.df_historic_to_view['time'] = pd.to_datetime(self.df_historic['time'], unit='s')
        self.df_historic_to_view['time_msc'] = pd.to_datetime(self.df_historic['time_msc'], unit='ns')

        # filter selected columns
        self.selected_columns = ['time', 'time_msc', 'type', 'entry', 'price', 'profit']
        self.df_historic = self.df_historic.filter(items=self.selected_columns)
        print(self.df_historic)

        # remove duplicate columns with a value of 0
        self.df_historic = self.df_historic.query('profit != 0')

        # Resetando o index
        self.df_historic = self.df_historic.reset_index(drop=True)
        print(self.df_historic)

    def open_file(self):
        # open a file
        self.my_file = filedialog.askopenfilename(title='Open File',
                                                  filetypes=(('Excel Files', '.xlsx'), ('ALL Files', '*.*')
                                                            ))
        # grab the file
        try:
            #create a dataframe
            self.file_name = self.my_file
            self.historic_df = pd.read_excel(io=self.file_name)
            self.index_start = self.historic_df.loc[self.historic_df.values == 'Posições'].index.values
            self.index_start = self.index_start[0]
            self.index_finish = self.historic_df.loc[self.historic_df.values == 'Ordens'].index.values
            self.index_finish = self.index_finish[0] - 1
            self.historic_df = self.historic_df.loc[self.index_start: self.index_finish]
            self.historic_df = self.historic_df.reset_index(drop=True)
            self.historic_df.columns = self.historic_df.iloc[1]
            self.historic_df = self.historic_df[2:]
            print(self.historic_df)

        except Exception as e:
            messagebox.showerror('Error', f'There was a problem! {e}')

        #Clear the treeview
        self.my_tree = view.App()
        self.my_tree = self.my_tree.trv
        self.my_tree.delete(*self.my_tree.get_children())

        # get the headers
        self.my_tree['column'] = list(self.historic_df.columns)
        self.my_tree['show'] = 'headings'

        # show the headers
        for col in self.my_tree['column']:
            self.my_tree.heading(col, text=col)
