from exemplo import AccuracyHistoric
import MetaTrader5 as mt5
import pandas as pd
import openpyxl

a = AccuracyHistoric()

# create 2 string one in english and other in portuguese for know if data is portuguese or english
english = 'Trade History Report'  # name of first column
portuguese = 'Relatório do Histórico de Negociação'  # name of first column

# import file data
customer1 = pd.read_excel('C:/Users/Thiago/Desktop/ReportHistory em ingles.xlsx')
customer2 = pd.read_excel("C:/Users/Thiago/Desktop/ReportHistory-em portugues.xlsx")

# collect name of first column
customer = customer2.keys()
customer = customer[0]

# if the first column in portuguese
if customer == portuguese:
    print('relatorio em portugues')
    # collect the number of index the row 'Ordens'
    ordens_index = customer2.loc[customer2['Relatório do Histórico de Negociação'] == 'Ordens'].index[0]

    # create a historic data frame
    historic_orders = customer2.loc[5:ordens_index - 1]
    historic_orders = historic_orders.reset_index(drop=True)
    historic_orders = historic_orders.rename(columns=historic_orders.iloc[0]).loc[1:]


# create a historic data frame for machine learning
    historic_orders_for_ml = historic_orders

    # Get a dictionary to store the new column names
    new_names = []
    count = 1
    # Iterate over the columns and rename the duplicates
    for col in historic_orders_for_ml.columns:
        if col == 'Preço':
            new_names.append(f'Preço_{count}')
            count += 1
            continue
        if col == 'Horário':
            new_names.append(f'Horário_{count}')
            count += 1
            continue
        new_names.append(col)
    historic_orders_for_ml.columns = new_names

    # rename the columns for machine learning
    historic_orders_for_ml = historic_orders_for_ml.rename(columns={'Horário_1': 'time',
                                                                    'Preço_2': 'price_open',
                                                                    'Tipo': 'type',
                                                                    'S / L': 'sl',
                                                                    'T / P': 'tp'})
    select_columns = ['time', 'price_open', 'type', 'sl', 'tp', 'Lucro']
    historic_orders_for_ml = historic_orders_for_ml.filter(items=select_columns)
    print(historic_orders_for_ml)


if customer == english:
    print('relatorio em ingles')
    # collect the number of index the row 'Orders'
    orders_index = customer1.loc[customer1['Trade History Report'] == 'Orders'].index[0]
    print(a)


