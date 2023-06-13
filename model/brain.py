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
        # Iniciando o MT5
        self.mt5 = mt5.initialize()

        #Criando data inicio e final
        self.from_date = datetime(2022, 1, 1)
        self.to_date = datetime.now()

        # Importando dados do historico
        self.symbol = 'GBPUSD'
        self.historic = mt5.history_deals_get(self.from_date, self.to_date, group='*GBPUSD*')
        print(self.historic)


a = Brain()
a.collect_historic()

