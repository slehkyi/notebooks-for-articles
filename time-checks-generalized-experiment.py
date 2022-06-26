import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

amount_of_checks = 1000  # how many times a person checks her/his phone

np.random.seed(666)
a = np.random.binomial(amount_of_checks, 0.044, size=10000)
p_a_2 = np.sum(a > 1) / 10000
p_a_3 = np.sum(a > 2) / 10000
p_a_4 = np.sum(a > 3) / 10000
print(" === Assuming average person checks their phone " + str(amount_of_checks) + " times per day === ")
print("Probability of seeing 'lucky time' two times per day: "
      + str(p_a_2) + ", three: " + str(p_a_3) + ", four: " + str(p_a_4))

n_sequential = 0
size = amount_of_checks
sample = 1000000

for s in range(sample):
    rare = np.random.random(size=size) < 0.044
    n_rare = np.sum(rare)
    if n_rare > 1:
        for i in range(size):
            if i == size-1:
                break
            elif rare[i] is True & rare[i+1] is True:
                n_sequential += 1
    if s % 1000 == 0:
        print('Processed: ' + str(s) + ' samples.')

print("Probability of two rare events one after another: " + str(float(n_sequential/sample)))

bins = np.arange(0, max(a) + 1.5) - 0.5

# plt.subplot(3, 1, 1)
plt.hist(a, bins=bins, normed=True, color='red')
plt.title('Phone usage')
plt.xlabel('Amount of "lucky hours spotted during the day"')
plt.ylabel('Probability')
plt.show()
