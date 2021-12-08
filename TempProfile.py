import loop, params, functions
import numpy as np


def initial(T_hot,T_cold):
    T_xcore = np.linspace(T_cold,T_hot,num=len(loop.xcore))
    T_xchimney = T_hot*np.ones(len(loop.xchimney))
    T_xhex = np.linspace(T_hot,T_cold,num=len(loop.xhex))
    T_xdowncomer = T_cold*np.ones(len(loop.xdowncomer))
    T_x =  np.concatenate((T_xcore,T_xchimney,T_xhex,T_xdowncomer))
    return T_x

def newinitial(Q, Tave):
    #Step 1, Calculate Core and HEX linear heat rate, temp, cp, and mass flow
    LHRcore=functions.kilo_to_base(Q/len(loop.xcore)) #W/mm
    LHRhex=functions.kilo_to_base(Q/len(loop.xhex))    #W/mm

    CP=functions.cp(Tave)   #J/kg-K
    M=functions.MassFlow(T_x,'core') #kg/s
#________________________________________________________________________
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
    LHRcore=functions.kilo_to_base(Qcore/len(loop.xcore)) #W/mm
    LHRhex=functions.kilo_to_base(Qhex/len(loop.xhex))    #W/mm

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
    for a in advance:
        T_x=np.roll(T_x,1)
        T_xcore=core(T_x)+dTcore
        T_xchimney=chimney(T_x)
        T_xhex=hex(T_x)-dThex
        T_xdowncomer=downcomer(T_x)
        T_x =  np.concatenate((T_xcore,T_xchimney,T_xhex,T_xdowncomer))


    return T_x
