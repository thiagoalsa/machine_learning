import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime


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
    def open_mt5(self):
        # Initialize MT5
        mt5.initialize()

        # Set period
        from_date = datetime(2023,1,1)
        to_date = datetime.now()

        # Collect historic data
        deals = mt5.history_deals_get(from_date, to_date, group="*GBPUSD*")

        # create a pandas DataFrame
        df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())

        colunas_selecionadas = ['time', 'time_msc', 'type', 'entry', 'price', 'profit']
        df_limpo = df.filter(items=colunas_selecionadas)

        # Removendo as linhas dobradas com o profit = 0

        df = df_limpo.query('profit != 0')

        # Resetando o index

        df = df.reset_index(drop=True)

