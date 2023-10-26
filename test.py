import numpy as np
import matplotlib.pyplot as plt
#from pynverse import inversefunc
import copy
import loop, initial, TempProfile, plots, functions, params

print(functions.coeff)
E = functions.EnergyArray
T = functions.TempArray
T_calc = functions.mu2T(E)
print(T_calc-T)
plt.figure()
plt.plot(E,functions.TempArray)
plt.plot(E,T_calc)
plt.show()

plt.plot(E,T_calc-T)
plt.show()






