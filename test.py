import numpy as np
import matplotlib.pyplot as plt
#from pynverse import inversefunc
import copy
import loop, initial, TempProfile, plots, functions, params

velos = np.linspace(0.001,0.15,num=100)
flowreacs = functions.FlowRxty(velos)

plt.figure()
plt.plot(velos,flowreacs)

plt.show()






