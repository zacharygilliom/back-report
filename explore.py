import pandas as pd 
import numpy as np 
from datetime import date 

df = pd.read_excel('BackOrderReport.xlsx')

# today = date.today().strftime("%Y-%m-%d")
today = date.today().strftime("%m-%d-%Y")
# print(today)
today = today.replace("-", "/")
# print(today)
today = str(today)
df_past = df[df['Confirmed CTP'] < today]
df_future = df[df['Confirmed CTP'] > today]

# grouped = df.groupby('Sales Order')
print(df.columns)

df['Last Scanned Time'] = df['Last Scanned Time'].apply(lambda x: x[:10])
# print(df['Last Scanned Time'])

# for index, row in df.iterrows():
# today_scans = df.where(df['Last Scanned Time'] == today)
today_scans = df.query("`Last Scanned Time` == @today")
# print(today_scans1.shape)
# print(today_scans.shape)
# print(today_scans)

grouped_scan_location = today_scans.groupby('Last Scanned').sum()
print(grouped_scan_location)
