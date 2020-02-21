import pandas as pd 
import numpy as np 
from datetime import date 

df = pd.read_excel('BackOrderReport.xlsx')

today = date.today().strftime("%Y-%m-%d")

df_past = df[df['Confirmed CTP'] < today]
df_future = df[df['Confirmed CTP'] > today]

grouped = df.groupby('Sales Order')
print(grouped.first(20))
print(grouped.last(20))
