import numpy as np
import matplotlib.pyplot as plt
from pynverse import inversefunc
import copy
import loop, initial, TempProfile, plots, functions, params

Q = 10000
print('determine initial conditions')
T_hot,T_cold,Q0,v = initial.algorithm(Q)


print('start everything else')
velo=int(round(functions.base_to_milli(v),0))

T_x = TempProfile.initial(T_hot, T_cold)
T_exit = T_x.copy()

T_xcore=TempProfile.core(T_exit)
T_xcore[-velo:] = T_xcore[-1]
T_xhex=TempProfile.hex(T_exit)
T_xhex[-velo:] = T_xhex[-1]
#T_exit =  np.concatenate((T_xcore,T_xchimney,T_xhex,T_xdowncomer))

T_enter = np.roll(T_x,velo)



LHRcore=Q0/len(loop.xcore) #kW/mm
LHRhex=-Q0/len(loop.xhex)    #kW/mm


E_x = functions.T2mu(T_x)

E_enter = E_x.copy()
E_xcore=TempProfile.core(E_enter)
E_xcore[-velo:] = E_xcore[-1]
E_xhex=TempProfile.hex(E_enter)
E_xhex[-velo:] = E_xhex[-1]
E_enter = np.roll(E_enter,velo)

E_exit = E_x.copy()

Q_core = LHRcore*np.ones(len(loop.xcore))
Q_core[0:velo] = np.linspace(0,Q_core[velo],num=velo)
Q_chimney = np.zeros(len(loop.xchimney))
Q_hex = LHRhex*np.ones(len(loop.xhex))
Q_hex[0:velo] = np.linspace(0,Q_hex[velo],num=velo)
Q_downcomer = np.zeros(len(loop.xdowncomer))
Q = np.concatenate((Q_core,Q_chimney,Q_hex,Q_downcomer))
print('stop everything else')

dE_x = E_enter - E_exit + Q
E_x += dE_x

print('start inverse')
Tnew = functions.mu2T(E_x)
print('stop inverse')


#error = T_x - Tnew



plots.x_vs_Tx("img/testTx4",0.0,Tnew,T_cold,T_hot)

#plots.x_vs_Tx("img/testerror",0.0,error,0.9999,-0.9999)

#T_xcore=TempProfile.core(T_x)










