import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns

sns.set()

pattern = 'data/madrid*.csv'
csv_files = glob.glob(pattern)

frames = []

for csv in csv_files:
    df = pd.read_csv(csv, index_col='date', parse_dates=True)
    frames.append(df)

df = pd.concat(frames)

df_time = df[['O_3', 'PM10']][df['station'] == 28079008].dropna()

df_plot = df_time.resample('M').mean()
plt.plot(df_plot)
plt.title('O3 and PM10 air polution levels')
plt.ylabel('micrograms per cubic meter (mg/m3)')
plt.xticks(rotation=45)
plt.show()
