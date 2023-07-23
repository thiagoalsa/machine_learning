import pandas as pd
import numpy as np


pd.reset_option('display.max_rows', 1000)
pd.reset_option('display.max_columns', 1000)

class DataView:
    def clean_customer(self, historic_df):
        # create 2 string one in english and other in portuguese for know if data is portuguese or english
        english = 'Trade History Report'  # name of first column
        portuguese = 'Relatório do Histórico de Negociação'  # name of first column

        # collect name of first column
        customer = historic_df.keys()
        customer = customer[0]

        # if the first column same portuguese DataFrame is in Portuguese
        if customer == portuguese:
            # collect the number of row index == 'Ordens' beacause there finish customer dataframe.
            pt_index = historic_df.loc[historic_df['Relatório do Histórico de Negociação'] == 'Ordens'].index[0]

            # create a historic data frame
            historic_orders = historic_df.loc[5:pt_index - 1]
            historic_orders = historic_orders.reset_index(drop=True)
            historic_orders = historic_orders.rename(columns=historic_orders.iloc[0]).loc[1:]
            historic_orders = historic_orders.dropna(axis=1, how='all')

            # Get a dictionary to store the new column names
            new_names = []
            names_list = ['Entrada', 'Entrada', 'Saida', 'Saida']
            count = 0
            # Iterate over the columns and rename the duplicates
            for col in historic_orders.columns:
                if col == 'Preço':
                    new_names.append(f'Preço {names_list[count]}')
                    count += 1
                    continue
                if col == 'Horário':
                    new_names.append(f'Horário {names_list[count]}')
                    count += 1
                    continue
                new_names.append(col)
            historic_orders.columns = new_names
            return historic_orders

        if customer == english:
            # collect the number of index the row 'Orders'
            en_index = historic_df.loc[historic_df['Trade History Report'] == 'Orders'].index[0]

            # create a historic data frame
            historic_orders = historic_df.loc[5:en_index - 1]
            historic_orders = historic_orders.reset_index(drop=True)
            historic_orders = historic_orders.rename(columns=historic_orders.iloc[0]).loc[1:]
            historic_orders = historic_orders.dropna(axis=1, how='all')
            # Get a dictionary to store the new column names
            new_names = []
            names_list = ['Entry', 'Entry', 'Close', 'Close']
            count = 0
            # Iterate over the columns and rename the duplicates
            for col in historic_orders.columns:
                if col == 'Price':
                    new_names.append(f'Price {names_list[count]}')
                    count += 1
                    continue
                if col == 'Time':
                    new_names.append(f'Time {names_list[count]}')
                    count += 1
                    continue
                new_names.append(col)
            historic_orders.columns = new_names
            return historic_orders


    def clean_graph_deals(self, historic_df):
        # create 2 string one in english and other in portuguese for know if data is portuguese or english
        english = 'Trade History Report'  # name of first column
        portuguese = 'Relatório do Histórico de Negociação'  # name of first column

        # collect name of first column
        customer = historic_df.keys()
        customer = customer[0]

        # if the first column same portuguese DataFrame is in Portuguese
        if customer == portuguese:
            # collect the number of row index == 'Transações' beacause there start and finish dataframe.
            pt_index_start = historic_df.loc[historic_df['Relatório do Histórico de Negociação'] == 'Transações'].index[0]
            pt_index_finish = historic_df.loc[historic_df['Relatório do Histórico de Negociação'] == 'Saldo:'].index[0]

            # use the first row for headings(name of columns)
            df = historic_df[pt_index_start + 1:pt_index_finish]
            df = df.reset_index(drop=True)
            df = df.rename(columns=df.iloc[0]).loc[1:]

            # remove row the Lucro == 0
            df = df.query('Lucro != 0')
            df = df.reset_index(drop=True)

            df = df['Saldo']
            return df

        if customer == english:
            # collect the number of row index == 'Transations' beacause there start dataframe.
            en_index_start = historic_df.loc[historic_df['Trade History Report'] == 'Deals'].index[0]
            en_index_finish = historic_df.loc[historic_df['Trade History Report'] == 'Balance:'].index[0]
            df = historic_df[en_index_start + 1:en_index_finish]
            df = df.reset_index(drop=True)
            df = df.rename(columns=df.iloc[0]).loc[1:]

            return df

'''
df = pd.read_excel("C:/Users/Thiago/Desktop/ReportHistory-em portugues.xlsx")
a = DataView().bar_graph(df)


plt.plot(a)
plt.axhline(y=a[0], color='red', linestyle='--', label='Abaixo negativo')
plt.ylabel('Saldo MT5')
plt.title('Historico de ganhos')
plt.legend()
plt.show()
'''