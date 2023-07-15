from datetime import datetime
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier



class AccuracyHistoric:
    def __init__(self):
        mt5.initialize()

        self.from_date = datetime(2022, 1, 1)
        self.to_date = datetime.now()

        self.orders = mt5.history_orders_get(self.from_date, self.to_date)
        self.deals = mt5.history_deals_get(self.from_date, self.to_date)

        self.df = pd.DataFrame(list(self.orders), columns=self.orders[0]._asdict().keys())
        self.df_profit = pd.DataFrame(list(self.deals), columns=self.deals[0]._asdict().keys())

        # transformando a coluna time_setup em um valor datetime
        self.df['time_setup'] = pd.to_datetime(self.df['time_setup'], unit='s')
        self.df['time_setup'] = self.df['time_setup'].dt.time

        # removendo os dois pontos -> : dos valores datetime da coluna time_setup
        self.coluna_nova = []
        for item in self.df['time_setup']:
            item_formatado = item.strftime('%H%M%S')
            self.coluna_nova.append(item_formatado)

        self.df['time_setup'] = self.coluna_nova

        # selecionando apenas as colunas necessarias para o machine learning
        self.colunas_selecionadas = ['time_setup', 'type', 'price_open', 'sl', 'tp']
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
            last_entry_time = self.df['time_setup'][:-1]
            last_entry_type = self.df['type'][:-1]
            last_entry_price = self.df['price_open'][:-1]
            last_entry_sl = self.df['sl'][:-1]
            last_entry_tp = self.df['tp'][:-1]
            last_entry_profit = self.df['profit'][:-1]
        else:
            print('dados insuficiente.')

        if len(self.df) > 3:
            # criar as colunas da penultima entrada
            second_last_entry_time = self.df['time_setup'][:-2]
            second_last_entry_type = self.df['type'][:-2]
            second_last_entry_price = self.df['price_open'][:-2]
            second_last_entry_sl = self.df['sl'][:-2]
            second_last_entry_tp = self.df['tp'][:-2]
            second_last_entry_profit = self.df['profit'][:-2]
        else:
            pass

        if len(self.df) > 4:
            # criar as colunas da ante-penultima entrada
            third_last_entry_time = self.df['time_setup'][:-3]
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
            self.df['last_entry_time'] = last_entry_time
            self.df['last_entry_type'] = last_entry_type
            self.df['last_entry_price'] = last_entry_price
            self.df['last_entry_sl'] = last_entry_sl
            self.df['last_entry_tp'] = last_entry_tp
            self.df['last_entry_profit'] = last_entry_profit
            print(self.df.shape[1])
        else:
            pass

        if len(self.df) > 3:
            # removendo a primeira linha novamente porque ela nao tem duas entrada anterior por ser a primeira
            self.df = self.df[1:]
            self.df = self.df.reset_index(drop=True)

            # adicionando as colunas da penultima entrada ao dataframe
            self.df['second_last_entry_time'] = second_last_entry_time
            self.df['second_last_entry_type'] = second_last_entry_type
            self.df['second_last_entry_price'] = second_last_entry_price
            self.df['second_last_entry_sl'] = second_last_entry_sl
            self.df['second_last_entry_tp'] = second_last_entry_tp
            self.df['second_last_entry_profit'] = second_last_entry_profit
            print(self.df.shape[1])
        else:
            pass

        if len(self.df) > 4:
            # removendo a primeira linha novamente porque ela nao tem entrada anterior por ser a primeira
            self.df = self.df[1:]
            self.df = self.df.reset_index(drop=True)

            # adicionando as colunas da penultima entrada ao dataframe
            self.df['third_last_entry_time'] = third_last_entry_time
            self.df['third_last_entry_type'] = third_last_entry_type
            self.df['third_last_entry_price'] = third_last_entry_price
            self.df['third_last_entry_sl'] = third_last_entry_sl
            self.df['third_last_entry_tp'] = third_last_entry_tp
            self.df['third_last_entry_profit'] = third_last_entry_profit
            print(self.df.shape[1])
        else:
            pass

        # iniciando o ML
        self.y = self.df['profit']
        self.x = self.df.drop('profit', axis=1)

        x_treino, x_teste, y_treino, y_teste = train_test_split(self.x, self.y, test_size=0.3)

        self.modelo = ExtraTreesClassifier()
        self.modelo.fit(x_treino, y_treino)

        resultado = self.modelo.score(x_teste, y_teste)
        print(f'Accuracy: {resultado * 100:.2f}%')


    def predict_position(self):
        positions = mt5.positions_get()
        if len(positions) > 0:
            self.df_positions = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
            # transformando valores de time em um valor dataframe
            self.df_positions['time'] = pd.to_datetime(self.df_positions['time'], unit='s')
            self.df_positions['time'] = self.df_positions['time'].dt.time

            # retirando os : dos valores para virar um valor inteiro
            self.df_positions['time'] = self.df_positions['time'].item().strftime('%H%M%S')

            # mudando o nome da coluna time para time_setup
            self.df_positions = self.df_positions.rename(columns={'time': 'time_setup'})

            # selecionando apenas as colunas necessarias para o machine learning
            colunas_selecionadas2 = ['time_setup', 'type', 'price_open', 'sl', 'tp']
            self.df_positions = self.df_positions.filter(items=colunas_selecionadas2)

            self.historic_df = self.collect_historic_df()

            if self.historic_df.shape[1] == 12:
                # adicionado as novas colunas ao dataframe das posicoes
                self.df_positions['last_entry_time'] = self.historic_df['time_setup'].iloc[[-1]].item()
                self.df_positions['last_entry_type'] = self.historic_df['type'].iloc[[-1]].item()
                self.df_positions['last_entry_price'] = self.historic_df['price_open'].iloc[[-1]].item()
                self.df_positions['last_entry_sl'] = self.historic_df['sl'].iloc[[-1]].item()
                self.df_positions['last_entry_tp'] = self.historic_df['tp'].iloc[[-1]].item()
                self.df_positions['last_entry_profit'] = self.historic_df['profit'].iloc[[-1]].item()


            elif self.historic_df.shape[1] > 12:
                self.df_positions['last_entry_time'] = self.historic_df['time_setup'].iloc[[-2]].item()
                self.df_positions['last_entry_type'] = self.historic_df['type'].iloc[[-2]].item()
                self.df_positions['last_entry_price'] = self.historic_df['price_open'].iloc[[-2]].item()
                self.df_positions['last_entry_sl'] = self.historic_df['sl'].iloc[[-2]].item()
                self.df_positions['last_entry_tp'] = self.historic_df['tp'].iloc[[-2]].item()
                self.df_positions['last_entry_profit'] = self.historic_df['profit'].iloc[[-2]].item()

            elif self.historic_df.shape[1] > 18:
                self.df_positions['last_entry_time'] = self.historic_df['time_setup'].iloc[[-3]].item()
                self.df_positions['last_entry_type'] = self.historic_df['type'].iloc[[-3]].item()
                self.df_positions['last_entry_price'] = self.historic_df['price_open'].iloc[[-3]].item()
                self.df_positions['last_entry_sl'] = self.historic_df['sl'].iloc[[-3]].item()
                self.df_positions['last_entry_tp'] = self.historic_df['tp'].iloc[[-3]].item()
                self.df_positions['last_entry_profit'] = self.historic_df['profit'].iloc[[-3]].item()

            self.model = self.collect_modelo()
            self.prevision = self.model(self.df_positions)
            if self.prevision == 0:
                print('LOSS')
            else:
                print('GAIN')

    def collect_historic_df(self):
        return self.df

    def collect_modelo(self):
        return self.modelo

a = AccuracyHistoric()
a.predict_position()
