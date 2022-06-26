import numpy as np
import pandas as pd


file = 'data/hashtags.csv'

data = pd.read_csv(file)

amount_of_tags = 27
selected_tags = []
top_limit = len(data)

for i in range(top_limit):
    rand_ind = np.random.randint(0, top_limit)
    to_select = data.iloc[rand_ind, 0]
    selected_tags.append(to_select)
    data.drop([rand_ind], axis=0)
    if len(selected_tags) == amount_of_tags:
        break

for i in range(amount_of_tags):
    print('#'+selected_tags[i])
