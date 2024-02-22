#./loop.py
import numpy as np
#Linear Path Length (mm)
'''Define the ends of all of the regimes'''
Ri1 = 0
Ro = 1660
top = 2090
HEXi = 2340
HEXo = 2825
bottom = 4975
Ri2 = 5710

#Define Loop
'''Create arrays for each regime then concatenate into one loop array'''
xcore = np.arange(Ri1,Ro+1)
xchimney = np.arange(Ro+1,HEXi)
xhex = np.arange(HEXi,HEXo+1)
xdowncomer = np.arange(HEXo+1,Ri2)
x = np.concatenate((xcore,xchimney,xhex,xdowncomer))

#New code since thesis was published
#Make non-linear power array
coreshape = np.sin(np.pi*(xcore+1)/len(xcore))
coreprofile = coreshape/sum(coreshape) #normalizes

#Check if shape is right. Only executes if you run this file, not when imported
if __name__ == "__main__":
    print(np.sum(coreprofile))
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(coreshape,xcore)
    plt.xlabel('Relative Power')
    plt.ylabel('Height in core')
    plt.show()