import numpy as np

np.random.seed(666)
a_min = np.random.binomial(28, 0.044, size=10000)
p_a_min_2 = np.sum(a_min > 1) / 10000
p_a_min_3 = np.sum(a_min > 2) / 10000
p_a_min_4 = np.sum(a_min > 3) / 10000
print(" === Assuming average person checks their phone 28 times per day === ")
print("Probability of seeing 'lucky time' two times per day: "
      + str(p_a_min_2) + ", three: " + str(p_a_min_3) + ", four: " + str(p_a_min_4))

a_avg = np.random.binomial(47, 0.044, size=10000)
p_a_avg_2 = np.sum(a_avg > 1) / 10000
p_a_avg_3 = np.sum(a_avg > 2) / 10000
p_a_avg_4 = np.sum(a_avg > 3) / 10000
print(" === Assuming average person checks their phone 47 times per day === ")
print("Probability of seeing 'lucky time' two times per day: "
      + str(p_a_avg_2) + ", three: " + str(p_a_avg_3) + ", four: " + str(p_a_avg_4))

a_max = np.random.binomial(86, 0.044, size=10000)
p_a_max_2 = np.sum(a_max > 1) / 10000
p_a_max_3 = np.sum(a_max > 2) / 10000
p_a_max_4 = np.sum(a_max > 3) / 10000
print(" === Assuming average person checks their phone 86 times per day === ")
print("Probability of seeing 'lucky time' two times per day: "
      + str(p_a_max_2) + ", three: " + str(p_a_max_3) + ", four: " + str(p_a_max_4))

n_sequential = 0
size = 86
sample = 1000000

for _ in range(sample):
    rare = np.random.random(size=size) < 0.044
    n_rare = np.sum(rare)
    if n_rare > 1:
        for i in range(size):
            if i == size-1:
                break
            elif rare[i] is True & rare[i+1] is True:
                n_sequential += 1

print("Probability of two rare events one after another: " + str(float(n_sequential/sample)))
