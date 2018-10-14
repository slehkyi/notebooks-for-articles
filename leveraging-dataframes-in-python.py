import pandas as pd
import numpy as np

cols = ['col1', 'col2', 'col3', 'col4', 'col5']
rows = ['row1', 'row2', 'row3', 'row4', 'row5']
df = pd.DataFrame(np.random.randint(0,100,size=(5, 5)), columns=cols, index=rows)

df.head()
