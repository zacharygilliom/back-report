import pandas as pd 
import numpy as np 
from datetime import date
import matplotlib.pyplot as plt 
import seaborn as sns 

sns.set_style('darkgrid')

df = pd.read_excel('BackOrderReport.xlsx')
# print(df.dtypes)
# print(df.head())

# Load in todays date.
today = date.today().strftime("%Y-%m-%d")

# Want to separate the data into two dataframes so we can later merge the two dataframes if they occur in both datafrmes
df_past = df[df['Confirmed CTP'] < today]
df_future=df[df['Confirmed CTP'] > today]

# Creating our two tables
table_past = pd.pivot_table(
	data=df_past,
	values=['Order Balance', 'Prod Balance'],
	index=['Sales Order', 'Name', 'Confirmed CTP'],
	aggfunc={'Order Balance':np.sum, 'Prod Balance':np.sum}
	)

table_future = pd.pivot_table(
	data=df_future,
	values=['Order Balance', 'Prod Balance'],
	index=['Sales Order', 'Name', 'Confirmed CTP'],
	aggfunc={'Order Balance':np.sum, 'Prod Balance':np.sum}
	)

# Resetting index so we can merge the two tables.
table_past.reset_index(inplace=True)
table_future.reset_index(inplace=True)

final_table = table_past.merge(table_future, 
			on=['Sales Order', 'Name'],
			suffixes=('_past', '_future'),
			how='left'
			)

# printing out some of our data
print("**** Table with past dates ****")
print(table_past)
print("**** Table with future dates ****")
print(table_future)
print('**** Final Table ****')
print(final_table)

# Need to format our date columns as we don't want any of the time values.
final_table['Confirmed CTP_past'] = final_table['Confirmed CTP_past'].apply(lambda x: x.strftime("%Y-%m-%d"))
final_table['Confirmed CTP_future'] = final_table['Confirmed CTP_future'].apply(lambda x: None if pd.isna(x) else x.strftime("%Y-%m-%d"))

# print(final_table[['Confirmed CTP_past', 'Confirmed CTP_future']].dtypes)

# Pushing the final pivot table to excel file
final_table.to_excel('NUReport.xlsx', sheet_name='NU Report', index=False, index_label='Sales Order', na_rep='None')

# data visuals
sns.barplot(x='Last Scanned', y='Prod Balance', data=df_past, palette='pastel',estimator=sum, ci=None)
plt.show()
