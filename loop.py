import numpy as np
#Linear Path Length (mm)
Ri1 = 0
Ro = 1660
top = 2090
HEXi = 2340
HEXo = 2825
bottom = 4975
Ri2 = 5710

#Define Loop
xcore = np.arange(Ri1,Ro+1)
xchimney = np.arange(Ro+1,HEXi)
xhex = np.arange(HEXi,HEXo+1)
xdowncomer = np.arange(HEXo+1,Ri2)
x = np.concatenate((xcore,xchimney,xhex,xdowncomer))
