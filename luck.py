import numpy as np

luck = 777
actions = 100000
total_hits = []

for i in range(actions):
    a = np.random.randint(0, 1000)
    if a == luck:
        total_hits.append(i)


print(total_hits)
print(len(total_hits))
