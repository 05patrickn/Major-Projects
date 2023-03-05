import numpy as np
from matplotlib import pyplot as plt
import random
from scipy.special import comb
from scipy.stats import norm


def hop_flea(x):

    N = len(x)
    i = random.randint(0, N-1)  # pick a random flea
    x[i] = 1 - x[i]            # hop the flea from dog 1 to dog 2
    return x

N = [50, 100, 200, 500]
for N in N:   
    x = [1]*N  # initial configuration (all on first dog)
    T=20*N
    N1 = np.ones(T)
    Sarray = np.array([np.log(comb(N, N))])
    for t in range(0, T):
        x = hop_flea(x)
        N1[t] = np.sum(x)
        Sarray = np.append(Sarray, np.log(comb(N, N1[t])))
    
    fig1, ax = plt.subplots(2, 1, dpi = 100, figsize = (8, 7))
    
    ax[0].plot(range(T), N1)
    ax[0].set_title('$N_1$ Sums')
    ax[1].set_xlabel('Time')
    ax[0].set_ylabel('Number of fleas on dog 1')
    
    ax[1].plot(range(T+1), Sarray)
    ax[1].set_title('$S(t)$ Entropy')
    ax[1].set_ylabel('$S=\ln g(N_1, N)$')   
    fig1.suptitle(f'N = {N}')
    

N = 500  # number of fleas
x = [1]*N  # initial configuration (all on first dog)
T=10000
N1 = np.ones(T)

for t in range(0, T):
    x = hop_flea(x)
    N1[t] = np.sum(x)

N1_last_half = N1[T//2:]

# calculate the mean and standard deviation of N1
mu = np.mean(N1_last_half)
sigma = np.std(N1_last_half)

dist = norm(mu, sigma)

x = np.linspace(0, N, 1000)
pdf = dist.pdf(x)

# plot the histogram and the normal distribution PDF
plt.hist(N1_last_half, bins=range(N+1), density=True)
plt.plot(x, pdf, label=f'Expected Gaussian \n Mean={mu:.0f} \n Std Dev={sigma:.0f}')

plt.xlabel('Number of fleas on dog 1')
plt.ylabel('Probability density')
plt.xlim(200,300)
plt.title('Histogram of N1(t) and expected Gaussian distribution')
plt.legend()
plt.show()
