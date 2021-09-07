import math
import cmath
# import scipy.integrate as I
import numpy as np
# from numpy import linalg as LA
import matplotlib.pyplot as plt
from matplotlib import mlab
# from scipy.optimize import fsolve
from mpmath import findroot
from sympy import Float

a1 = 1.23
a2 = 1.05
p = 10
q = 1
eps = 0.02
a = 30
# def f(L):
#     return L + 1 + a1 * cmath.exp(-L) + a2 * cmath.exp(-10*L)
# starting_guess = (0.05+1j)
# print(fsolve(f, starting_guess))

n = 2000 #2000 200
x = np.ndarray(n*2, dtype=np.complex128)
roots = []
r_real = []
r_imag = []
for i in range(-n,n):
    x[i] = complex(0,i*0.1) #0.01 0.1
# print(x)


for i in x:
    try:
        #a = findroot(lambda L: L + 1 + a1 * cmath.exp(-q*L) + a2 * cmath.exp(-p*L), i, solver='muller')
        a = findroot(lambda L: eps**2 * L**2 + eps*L+1 - 0.866*(1+a*eps**2)*cmath.exp(-L), i, solver='muller')
        print(a)
        roots.append(complex(Float(a.real,5),Float(a.imag,5)))
        r_real.append(Float(a.real,5))
        r_imag.append(Float(a.imag,5))
    except: 
        pass

roots = set(roots)
# for L in roots:
#     print(L)

plt.xlabel("real")
plt.ylabel("imag")
plt.plot(r_real,r_imag,".")
plt.grid()   
# plt.title(" p = {}, q = {}".format(p,q) + ", уравнение 1")
plt.show()
