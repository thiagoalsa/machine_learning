import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import datetime


pd.set_option('display.max_columns', 500)  # número de colunas mostradas
pd.set_option('display.width', 1500)  # max. largura máxima da tabela exibida

class DataView:
    def __init__(self):

        mt5.initialize()

        # obtemos o número de transações no histórico
        from_date = datetime(2022, 1, 1)
        to_date = datetime.now()

        orders = mt5.history_orders_get(from_date, to_date)
        deals = mt5.history_deals_get(from_date, to_date)

        df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
        df_profit = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())

        # transformando as colunas time_setup em um valor datetime
        df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
        df['time_setup_msc'] = pd.to_datetime(df['time_setup_msc'], unit='ms')
        df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
        df['time_done_msc'] = pd.to_datetime(df['time_done_msc'], unit='ms')

        # alterando os valores de profit positivo para 1 e valores negativos para 0
        df['type'] = np.where(df['type'] > 0, 'sell', 'buy')
        df = df.reset_index(drop=True)

        # removendo as linhas que nao possuem sl
        df = df.query('sl != 0')
        df = df.reset_index(drop=True)

        # removendo as linhas que o valor de profit seja igual a 0
        df_profit = df_profit.filter(items=['profit'])
        df_profit = df_profit[1:]
        df_profit = df_profit.query('profit != 0')
        df_profit = df_profit.reset_index(drop=True)

        # removendo as linhas com o profit baixo 'porque nao bateram no tp ou sl'
        df['profit'] = df_profit
        df = df.query('profit > 20 or profit < - 20')
        df = df.reset_index(drop=True)



        print(df)

#df.to_csv('MLMT5.csv', index=True)

a = DataView()