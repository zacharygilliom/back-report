import pandas as pd 
import numpy as np 
from datetime import date

df = pd.read_excel('BackOrderReport.xlsx')
print(df.dtypes)
print(df.head())
# df['Confirmed CTP'].astype
# df['Confirmed CTP'] = pd.to_datetime(df['Confirmed CTP'])
# df.astype({'Confirmed CTP': 'date'}).dtypes
# np.datetime64(date.utcnow()).astype(datetime)
today = date.today().strftime("%Y-%m-%d")

df_past = df[df['Confirmed CTP'] < today]
df_future=df[df['Confirmed CTP'] > today]

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
table_past.reset_index(inplace=True)
table_future.reset_index(inplace=True)

final_table = table_past.merge(table_future, 
			on=['Sales Order', 'Name'],
			suffixes=('_past', '_future'),
			how='left'
			)

# test_table = df_past.pivot(index='Sales Order', values=['Confirmed CTP', 'Order Balance', 'Prod Balance'])
# final_table_1 = table_past.join(table_future,
# 								on='Sales Order')

print(table_past)
print(table_future)

print(final_table)

final_table['Confirmed CTP_past'] = final_table['Confirmed CTP_past'].apply(lambda x: x.strftime("%Y-%m-%d"))
final_table['Confirmed CTP_future'] = final_table['Confirmed CTP_future'].apply(lambda x: None if pd.isna(x) else x.strftime("%Y-%m-%d"))

print(final_table[['Confirmed CTP_past', 'Confirmed CTP_future']].dtypes)

# final_table.set_index(['Sales Order', 'Name', 'Confirmed CTP_past'])

final_table.to_excel('NUReport.xlsx', sheet_name='NU Report', index=False, index_label='Sales Order', na_rep='None')


