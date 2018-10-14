import pandas as pd
import numpy as np

cols = ['col0', 'col1', 'col2', 'col3', 'col4']
rows = ['row0', 'row1', 'row2', 'row3', 'row4']
data = np.random.randint(0, 100, size=(5, 5))
df = pd.DataFrame(data, columns=cols, index=rows)

df.head()

df['col1']['row1']

df.loc['row4', 'col2']

df.iloc[4, 2]

df_new = df[['col1', 'col2']]
df_new.head(3)

df_new = df[['col1', 'col2']][1:4]
df_new.head(3)

df['col0']
df.loc[:, 'col0']
df.iloc[:, 0]

df['col3'][2:5]

df.loc['row1':'row4', :]
df.iloc[1:4, :]

df.loc[:, 'col1':'col4']
df.iloc[:, 1:4]

df.loc['row1':'row4', 'col1':'col4']
df.iloc[1:4, 1:4]

df.loc['row2':'row4', ['col1', 'col3']]
df.iloc[[2, 4], 0:4]

df[df['col1'] > 20]
# assigning variable also works
condition = df['col1'] > 20
df[condition]

df[(df['col1'] > 25) & (df['col3'] < 30)]  # logical and
df[(df['col1'] > 25) | (df['col3'] < 30)]  # logical or
df[~(df['col1'] > 25)]  # logical not

df.iloc[3, 3] = 0
df.iloc[1, 2] = np.nan
df.iloc[4, 0] = np.nan
df['col5'] = 0
df['col6'] = np.NaN
df.head()

df.loc[:, df.all()]

df.loc[:, df.any()]

df.loc[:, df.isnull().any()]

df.loc[:, df.notnull().all()]

df_na_any = df.dropna(how='any')  # if any value in a row is NaN it will be dropped
df_na_all = df.dropna(how='all', axis=1)  # if all values in a row are NaN it will be dropped

# Find a column based on another
df['col1'][df['col2'] > 35]

df['col1'][df['col2'] > 35] += 5
df[df['col1'] > 35]

df['new_col'] = df['col4'].apply(lambda n: n*2)

df.index.str.upper()

df.index.map(str.lower)

red_vs_blue = {0:'blue', 12:'red'}

df['color'] = df['col3'].map(red_vs_blue)
df.head()

df['col7'] = df['col3'] + df['col4']
df.head()