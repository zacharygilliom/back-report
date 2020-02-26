import pandas as pd 
import numpy as np 
from datetime import date
import matplotlib.pyplot as plt 
import matplotlib
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

df_backorder_analysis = df[df['Confirmed CTP'] < today]

df_backorder_analysis['Confirmed CTP'] = df_backorder_analysis['Confirmed CTP'].apply(lambda x: x.strftime("%Y-%m-%d"))


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

df_melt = df_backorder_analysis[['Sales Order', 'Confirmed CTP', 'Order Balance', 'Prod Balance']]
df_melted = pd.melt(df_melt, id_vars=['Sales Order', 'Confirmed CTP']).sort_values(['variable', 'value'])
print(df_melted.head())
# Pushing the final pivot table to excel file
final_table.to_excel('NUReport.xlsx', sheet_name='NU Report', index=False, index_label='Sales Order', na_rep='None')

# data visuals
fig, ax = plt.subplots(nrows=4, constrained_layout=True)
fig.suptitle('Distribution of Backordered Production Status')
sns.barplot(x='Last Scanned', y='Prod Balance', data=df_backorder_analysis, palette='dark',estimator=sum, ci=None, ax=ax[0])
ax[0].set_title('Number of Doors To Be Built at The Last Scanned Location.')
ax[0].set_xlabel('Last Scanned Location')
ax[0].set_ylabel('Count of Production Balance')

sns.lineplot(x='Confirmed CTP', y='Prod Balance', data=df_backorder_analysis, ax=ax[1], palette='dark', ci=None, estimator=sum)
ax[1].set_title('Quantity of Production Balance for Each CTP date')
ax[1].set_xlabel('Confirmed CTP Date')
ax[1].set_ylabel('Count of Production Balance')

sns.countplot(y='Name', data=df_backorder_analysis, ax=ax[2], palette='dark')
ax[2].set_title('Number of Line Items Backordered for Each Customer')
ax[2].set_xlabel('Count of Line Items')
ax[2].set_ylabel('Customer Name')

sns.barplot(x='Sales Order', y='value', data=df_melted, hue='variable', ax=ax[3], estimator=sum, ci=None, palette='dark')
ax[3].set_title('Order Balance and Prod Balance for each order')
ax[3].set_xlabel('Sales Order')
ax[3].set_ylabel('Count of Doors')

# plt.tight_layout()
plt.show()
# plt.savefig('images/output.png')
