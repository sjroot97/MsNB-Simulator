import loop, params, functions
import numpy as np

def initial(T_hot,T_cold):
    T_xcore = np.linspace(T_cold,T_hot,num=len(loop.xcore))
    T_xchimney = T_hot*np.ones(len(loop.xchimney))
    T_xhex = np.linspace(T_hot,T_cold,num=len(loop.xhex))
    T_xdowncomer = T_cold*np.ones(len(loop.xdowncomer))
    T_x =  np.concatenate((T_xcore,T_xchimney,T_xhex,T_xdowncomer))
    return T_x

#________________________________________________________________________
def smooth(arr,howmany):
    chunklength = len(arr)//howmany
    L = chunklength*np.arange(1,howmany)
    L[howmany//2:] += len(arr)%chunklength
    chunks = np.split(arr,L)
    
    list = []
    for chunk in chunks:
        list.append(np.linspace(chunk[0],chunk[-1],num=len(chunk)))
    
    smoothed_arr = np.concatenate(list)
    return smoothed_arr

def core(T_x):
    T_xcore = np.split(T_x,[loop.xcore[-1]+1])[0]
    return T_xcore

def chimney(T_x):
    T_xchimney = np.split(T_x,[loop.xchimney[0],loop.xchimney[-1]+1])[1]
    return T_xchimney

def hex(T_x):
    T_xhex = np.split(T_x,[loop.xhex[0],loop.xhex[-1]+1])[1]
    return T_xhex

def downcomer(T_x):
    T_xdowncomer = np.split(T_x,[loop.xdowncomer[0]])[1]
    return T_xdowncomer
    
    

#___________________________________________________________________________
def advance(T_x, velo, Qcore, Qhex):
    #Step 1, Calculate Core and HEX linear heat rate, temp, cp, and mass flow
    LHRcore=Qcore/len(loop.xcore) #kW/mm
    LHRhex=Qhex/len(loop.xhex)    #kW/mm

    Tcore=functions.list_ave(core(T_x))    #Celcius
    Thex=functions.list_ave(hex(T_x))      #Celcius

    CPcore=functions.cp(Tcore)   #J/kg-K
    CPhex=functions.cp(Thex)     #J/kg-K

    Mcore=functions.MassFlow(T_x,'core') #kg/s
    Mhex=functions.MassFlow(T_x,'hex')   #kg/s

    #Step 2, Calculate Core and HEX linear temperature rise
    dTcore=LHRcore/(Mcore*CPcore) #degC/mm
    dThex=LHRhex/(Mhex*CPhex)   #degC/mm

    #Step 3, calculate distance traveled during step - v*dt
    velo=int(round(functions.base_to_milli(velo),0))
    advance=np.arange(1,velo+1)

    #Step 4, roll and heat/cool
    for _ in advance:
        T_x=np.roll(T_x,1)
        T_xcore=core(T_x)+dTcore
        T_xchimney=chimney(T_x)
        T_xhex=hex(T_x)-dThex
        T_xdowncomer=downcomer(T_x)
        T_x =  np.concatenate((T_xcore,T_xchimney,T_xhex,T_xdowncomer))
    
    T_xcore = smooth(T_xcore,10)
    T_xchimney = smooth(T_xchimney,5)
    T_xhex = smooth(T_xhex,5)
    T_xdowncomer = smooth(T_xdowncomer,10)
    T_x =  np.concatenate((T_xcore,T_xchimney,T_xhex,T_xdowncomer))
    return T_x

def newadvance(T_x,velo,Qcore,Qhex):
    velo=int(round(functions.base_to_milli(velo),0))
    
    LHRcore=Qcore/len(loop.xcore) #kW/mm
    LHRhex=-Qhex/len(loop.xhex)    #kW/mm
    Q_core = LHRcore*np.ones(len(loop.xcore))
    Q_core[0:velo] = np.linspace(0,Q_core[velo],num=velo)
    Q_chimney = np.zeros(len(loop.xchimney))
    Q_hex = LHRhex*np.ones(len(loop.xhex))
    Q_hex[0:velo] = np.linspace(0,Q_hex[velo],num=velo)
    Q_downcomer = np.zeros(len(loop.xdowncomer))
    Q = np.concatenate((Q_core,Q_chimney,Q_hex,Q_downcomer))
    
    E_x = functions.T2mu(T_x)

    E_enter = E_x.copy()
    E_xcore=core(E_enter)
    E_xcore[-velo:] = E_xcore[-1]
    E_xhex=hex(E_enter)
    E_xhex[-velo:] = E_xhex[-1]
    E_enter = np.roll(E_enter,velo)

    E_exit = E_x.copy()
    
    dE_x = E_enter - E_exit + Q
    E_x += dE_x

    Tnew = functions.mu2T(E_x)
    return Tnew