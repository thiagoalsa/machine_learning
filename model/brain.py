import MetaTrader5 as mt5
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime

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

    def collect_historic(self):
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

        #####################################################
        self.orders = mt5.history_deals_get(self.from_date, self.to_date, group='*GBPUSD*')

        if self.orders is not None and len(self.orders) > 0:
            for order in self.orders:
                self.ticket = self.orders.ticket
                self.time = self.orders.time
                self.symbol = self.orders.symbol
                self.action = self.orders.action
                self.volume = self.orders.volume
                self.price = self.orders.price

                # Obtém os valores de stop loss e take profit
                self.order_info = mt5.order_get()
                if self.order_info is not None:
                    self.stop_loss = self.order_info.sl
                    self.take_profit = self.order_info.tp
                    print(self.stop_loss)
                else:
                    self.stop_loss = None
                    self.take_profit = None
                    print(self.stop_loss)

                # Faça o processamento necessário com os dados

        else:
            print("Nenhuma operação encontrada.")


a = Brain()
a.collect_historic()

