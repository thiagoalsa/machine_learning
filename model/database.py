import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
from tkinter import messagebox
from datetime import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
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


class HistoricModel():
    def get_position_customer(self):
        # Initialize MT5
        mt5.initialize()

        # Collect positions data
        self.positions = mt5.positions_get()

        # create a pandas DataFrame
        if len(self.positions) > 0:
            self.positions_df = pd.DataFrame(list(self.positions), columns=self.positions[0]._asdict().keys())
            print(self.positions_df.to_string())
            self.columns_selected = ['price_open', 'type', 'sl', 'tp']
            self.positions_df = self.positions_df.filter(items=self.columns_selected)

            return self.positions_df
        else:
            messagebox.showerror('Error!', 'There is no open position')

    def get_historic_customer(self):
        # Initialize MT5
        mt5.initialize()

        self.from_date = datetime(2000, 1, 1)
        self.to_date = datetime.now()

        self.orders = mt5.history_orders_get(self.from_date, self.to_date)
        self.deals = mt5.history_deals_get(self.from_date, self.to_date)

        self.df = pd.DataFrame(list(self.orders), columns=self.orders[0]._asdict().keys())
        self.df_profit = pd.DataFrame(list(self.deals), columns=self.deals[0]._asdict().keys())

        # selecionando apenas as colunas necessarias para o machine learning
        self.colunas_selecionadas = ['type', 'price_open', 'sl', 'tp']
        self.df = self.df.filter(items=self.colunas_selecionadas)

        # removendo as linhas que nao possuem sl
        self.df = self.df.query('sl != 0')
        self.df = self.df.reset_index(drop=True)

        # removendo as linhas que nao possuem tp
        self.df = self.df.query('tp != 0')
        self.df = self.df.reset_index(drop=True)

        # removendo as linhas que o valor de profit seja igual a 0
        self.df_profit = self.df_profit.filter(items=['profit'])
        self.df_profit = self.df_profit[1:]
        self.df_profit = self.df_profit.query('profit != 0')
        self.df_profit = self.df_profit.reset_index(drop=True)
        self.df['profit'] = self.df_profit
        # alterando os valores de profit positivo para 1 e valores negativos para 0
        self.df['profit'] = np.where(self.df['profit'] > 0, 1, 0)
        self.df = self.df.reset_index(drop=True)

        if len(self.df) > 2:
            # criar as colunas da ultima entrada
            last_entry_type = self.df['type'][:-1]
            last_entry_price = self.df['price_open'][:-1]
            last_entry_sl = self.df['sl'][:-1]
            last_entry_tp = self.df['tp'][:-1]
            last_entry_profit = self.df['profit'][:-1]
        else:
            return 'insufficient data.'

        if len(self.df) > 3:
            # criar as colunas da penultima entrada
            second_last_entry_type = self.df['type'][:-2]
            second_last_entry_price = self.df['price_open'][:-2]
            second_last_entry_sl = self.df['sl'][:-2]
            second_last_entry_tp = self.df['tp'][:-2]
            second_last_entry_profit = self.df['profit'][:-2]
        else:
            pass

        if len(self.df) > 4:
            # criar as colunas da ante-penultima entrada
            third_last_entry_type = self.df['type'][:-3]
            third_last_entry_price = self.df['price_open'][:-3]
            third_last_entry_sl = self.df['sl'][:-3]
            third_last_entry_tp = self.df['tp'][:-3]
            third_last_entry_profit = self.df['profit'][:-3]
        else:
            pass

        if len(self.df) > 2:
            # removendo a primeira linha porque ela nao tem entrada anterior por ser a primeira
            self.df = self.df[1:]
            self.df = self.df.reset_index(drop=True)

            # adicionando as colunas da ultima entrada ao dataframe
            self.df['last_entry_type'] = last_entry_type
            self.df['last_entry_price'] = last_entry_price
            self.df['last_entry_sl'] = last_entry_sl
            self.df['last_entry_tp'] = last_entry_tp
            self.df['last_entry_profit'] = last_entry_profit
        else:
            pass

        if len(self.df) > 3:
            # removendo a primeira linha novamente porque ela nao tem duas entrada anterior por ser a primeira
            self.df = self.df[1:]
            self.df = self.df.reset_index(drop=True)

            # adicionando as colunas da penultima entrada ao dataframe
            self.df['second_last_entry_type'] = second_last_entry_type
            self.df['second_last_entry_price'] = second_last_entry_price
            self.df['second_last_entry_sl'] = second_last_entry_sl
            self.df['second_last_entry_tp'] = second_last_entry_tp
            self.df['second_last_entry_profit'] = second_last_entry_profit
        else:
            pass

        if len(self.df) > 4:
            # removendo a primeira linha novamente porque ela nao tem entrada anterior por ser a primeira
            self.df = self.df[1:]
            self.df = self.df.reset_index(drop=True)

            # adicionando as colunas da penultima entrada ao dataframe
            self.df['third_last_entry_type'] = third_last_entry_type
            self.df['third_last_entry_price'] = third_last_entry_price
            self.df['third_last_entry_sl'] = third_last_entry_sl
            self.df['third_last_entry_tp'] = third_last_entry_tp
            self.df['third_last_entry_profit'] = third_last_entry_profit
        else:
            pass

        # iniciando o ML
        self.y = self.df['profit']
        self.x = self.df.drop('profit', axis=1)

        total_df = len(self.x)
        train_index = int(total_df / 100 * 30)

        # create x train
        x_train = self.x[:-train_index]

        #create y train
        y_train = self.y[:-train_index]

        # create x test
        x_test = self.x[train_index:]

        #create y test
        y_test = self.y[train_index:]

        #x_treino, x_teste, y_treino, y_teste = train_test_split(self.x, self.y, test_size=0.3)

        self.modelo = ExtraTreesClassifier()
        self.modelo.fit(x_train, y_train)

        resultado = self.modelo.score(x_test, y_test)

        return f'Accuracy around: {resultado * 100:.2f}%'

a = HistoricModel()
a.get_historic_customer()
