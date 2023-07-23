from exemplo import AccuracyHistoric
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from new_layout import App
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)


class Lysmatta():
    def clean_customer(self, historic_df):
        # create 2 string one in english and other in portuguese for know if data is portuguese or english
        english = 'Trade History Report'  # name of first column
        portuguese = 'Relatório do Histórico de Negociação'  # name of first column

        # collect name of first column
        customer = historic_df.keys()
        customer = customer[0]

        # if the first column same portuguese DataFrame is in Portuguese
        if customer == portuguese:
            print('relatorio em portugues')
            # collect the number of row index == 'Ordens' beacause there finish customer dataframe.
            ordens_index = historic_df.loc[historic_df['Relatório do Histórico de Negociação'] == 'Ordens'].index[0]

            # create a historic data frame
            historic_orders = historic_df.loc[5:ordens_index - 1]
            historic_orders = historic_orders.reset_index(drop=True)
            historic_orders = historic_orders.rename(columns=historic_orders.iloc[0]).loc[1:]
            historic_orders = historic_orders.dropna(axis=1, how='all')
            return historic_orders


        if customer == english:
            print('relatorio em ingles')
            # collect the number of index the row 'Orders'
            orders_index = customer.loc[customer['Trade History Report'] == 'Orders'].index[0]


    def clean_ml(self, historic_orders):
        # create a historic data frame for machine learning
        historic_orders_for_ml = historic_orders

        # Get a dictionary to store the new column names
        new_names = []
        names_list = ['Entrada', 'Saida', 'Entrada', 'Saida']
        count = 0
        # Iterate over the columns and rename the duplicates
        for col in historic_orders_for_ml.columns:
            if col == 'Preço':
                new_names.append(f'Preço {names_list[count]}')
                count += 1
                continue
            if col == 'Horário':
                new_names.append(f'Horário {names_list[count]}')
                count += 1
                continue
            new_names.append(col)
        historic_orders_for_ml.columns = new_names

        # rename the columns for machine learning
        historic_orders_for_ml = historic_orders_for_ml.rename(columns={'Horário_1': 'time',
                                                                        'Preço_2': 'price_open',
                                                                        'Tipo': 'type',
                                                                        'S / L': 'sl',
                                                                        'T / P': 'tp',
                                                                        'Preço_4': 'price_close'})
        select_columns = ['time', 'price_open', 'type', 'sl', 'tp', 'price_close', 'Lucro']
        historic_orders_for_ml = historic_orders_for_ml.filter(items=select_columns)

        # remove the rows do not have sl
        historic_orders_for_ml = historic_orders_for_ml.query('sl != 0')
        historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

        # remove the rows do not have tp
        historic_orders_for_ml = historic_orders_for_ml.query('tp != 0')
        historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

        # remove row the Lucro == 0
        historic_orders_for_ml = historic_orders_for_ml.query('Lucro != 0')
        historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

        # remove rows where Lucro less than input
        more_than = int(input('How much? '))
        historic_orders_for_ml = historic_orders_for_ml[(historic_orders_for_ml['Lucro'] > more_than) |
                                                        (historic_orders_for_ml['Lucro'] < - more_than)]

        # change positive number for 1 and negative number for 0
        historic_orders_for_ml['Lucro'] = np.where(historic_orders_for_ml['Lucro'] > 0, 1, 0)
        historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

        # change sell or buy for int number
        historic_orders_for_ml['type'] = np.where(historic_orders_for_ml['type'] == 'sell', 1, 0)
        historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

        # remove the 2 dots -> :
        new_column = []
        for item in historic_orders_for_ml['time']:
            item_change = item[11:]
            item_change = item_change.replace(':', '')
            new_column.append(item_change)

        historic_orders_for_ml['time'] = new_column

        if len(historic_orders_for_ml) > 2:
            # criar as colunas da ultima entrada
            last_entry_time = historic_orders_for_ml['time'][:-1]
            last_entry_type = historic_orders_for_ml['type'][:-1]
            last_entry_price = historic_orders_for_ml['price_open'][:-1]
            last_entry_sl = historic_orders_for_ml['sl'][:-1]
            last_entry_tp = historic_orders_for_ml['tp'][:-1]
            last_entry_Lucro = historic_orders_for_ml['Lucro'][:-1]
        else:
            print('dados insuficiente.')

        if len(historic_orders_for_ml) > 3:
            # criar as colunas da penultima entrada
            second_last_entry_time = historic_orders_for_ml['time'][:-2]
            second_last_entry_type = historic_orders_for_ml['type'][:-2]
            second_last_entry_price = historic_orders_for_ml['price_open'][:-2]
            second_last_entry_sl = historic_orders_for_ml['sl'][:-2]
            second_last_entry_tp = historic_orders_for_ml['tp'][:-2]
            second_last_entry_Lucro = historic_orders_for_ml['Lucro'][:-2]
        else:
            pass

        if len(historic_orders_for_ml) > 4:
            # criar as colunas da ante-penultima entrada
            third_last_entry_time = historic_orders_for_ml['time'][:-3]
            third_last_entry_type = historic_orders_for_ml['type'][:-3]
            third_last_entry_price = historic_orders_for_ml['price_open'][:-3]
            third_last_entry_sl = historic_orders_for_ml['sl'][:-3]
            third_last_entry_tp = historic_orders_for_ml['tp'][:-3]
            third_last_entry_Lucro = historic_orders_for_ml['Lucro'][:-3]
        else:
            pass

        if len(historic_orders_for_ml) > 2:
            # removendo a primeira linha porque ela nao tem entrada anterior por ser a primeira
            historic_orders_for_ml = historic_orders_for_ml[1:]
            historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

            # adicionando as colunas da ultima entrada ao dataframe
            historic_orders_for_ml['last_entry_time'] = last_entry_time
            historic_orders_for_ml['last_entry_type'] = last_entry_type
            historic_orders_for_ml['last_entry_price'] = last_entry_price
            historic_orders_for_ml['last_entry_sl'] = last_entry_sl
            historic_orders_for_ml['last_entry_tp'] = last_entry_tp
            historic_orders_for_ml['last_entry_Lucro'] = last_entry_Lucro
            print(historic_orders_for_ml.shape[1])
        else:
            pass

        if len(historic_orders_for_ml) > 3:
            # removendo a primeira linha novamente porque ela nao tem duas entrada anterior por ser a primeira
            historic_orders_for_ml = historic_orders_for_ml[1:]
            historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

            # adicionando as colunas da penultima entrada ao dataframe
            historic_orders_for_ml['second_last_entry_time'] = second_last_entry_time
            historic_orders_for_ml['second_last_entry_type'] = second_last_entry_type
            historic_orders_for_ml['second_last_entry_price'] = second_last_entry_price
            historic_orders_for_ml['second_last_entry_sl'] = second_last_entry_sl
            historic_orders_for_ml['second_last_entry_tp'] = second_last_entry_tp
            historic_orders_for_ml['second_last_entry_Lucro'] = second_last_entry_Lucro
            print(historic_orders_for_ml.shape[1])
        else:
            pass

        if len(historic_orders_for_ml) > 4:
            # removendo a primeira linha novamente porque ela nao tem entrada anterior por ser a primeira
            historic_orders_for_ml = historic_orders_for_ml[1:]
            historic_orders_for_ml = historic_orders_for_ml.reset_index(drop=True)

            # adicionando as colunas da penultima entrada ao dataframe
            historic_orders_for_ml['third_last_entry_time'] = third_last_entry_time
            historic_orders_for_ml['third_last_entry_type'] = third_last_entry_type
            historic_orders_for_ml['third_last_entry_price'] = third_last_entry_price
            historic_orders_for_ml['third_last_entry_sl'] = third_last_entry_sl
            historic_orders_for_ml['third_last_entry_tp'] = third_last_entry_tp
            historic_orders_for_ml['third_last_entry_Lucro'] = third_last_entry_Lucro
            print(historic_orders_for_ml.shape[1])
        else:
            pass
        print(historic_orders_for_ml)

        # iniciando o ML
        y = historic_orders_for_ml['Lucro']
        x = historic_orders_for_ml.drop('Lucro', axis=1)

        x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.25)

        modelo = ExtraTreesClassifier()
        modelo.fit(x_treino, y_treino)

        resultado = modelo.score(x_teste, y_teste)
        print('Acuracia: ', resultado)


df = pd.read_excel("C:/Users/Thiago/Desktop/ReportHistory-em portugues.xlsx")
df = df.dropna(axis=1, how='all')
print(df[500:])
