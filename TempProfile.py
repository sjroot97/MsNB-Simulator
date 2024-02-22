import loop, functions
import numpy as np

def initial(T_hot,T_cold):
    '''
    Define linear arrays in the heat transfer regimes, then converts those arrays back to temperature. Concatenates the regime arrays into a total temperature profile array.
    '''
    T_xcore = np.linspace(T_cold,T_hot,num=len(loop.xcore))
    T_xchimney = T_hot*np.ones(len(loop.xchimney))
    T_xhex = np.linspace(T_hot,T_cold,num=len(loop.xhex))
    T_xdowncomer = T_cold*np.ones(len(loop.xdowncomer))
    T_x =  np.concatenate((T_xcore,T_xchimney,T_xhex,T_xdowncomer))
    return T_x

#_______________________________________________________________
'''
These six functions split the full temperature array into regime arrays
'''
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
    
def coldleg(T_x):
    T_xcoldleg = np.split(T_x,[loop.HEXi,loop.bottom])[1]
    return T_xcoldleg
    
def hotleg(T_x):
    T_xhotleg = np.split(T_x,[loop.top])[0]
    return T_xhotleg

#_______________________________________________________________
def advance(T_x,velo,Qcore,Qhex):
    '''
    This function is the heart of the simulator. It rounds and converts the velocity to an integer mm/s. It generates power arrays where the core and heat exchanger have linear heat rates, with edge effects being considered to account for the fact that not some of the distance traversed is done in the riser or downcomer. The temperature profile is then converted to energy. It follows a uniform state uniform flow assumption where the change in energy is equal to the fluid internal energy entering minus the fluid internal energy entering, plus the heat into the control volume. It neglects gravimetric, kinetic, and PV differentials, as in liquids the temperature/heat capacity effects dominate. The entering fluid is obtained by "rolling" back the energy array by the velocity (times the timestep length), again considering edge effects. The new energy array is computed and converted to temperature, then returned to simulation.py
    '''
    velo=int(round(functions.base_to_milli(velo),0))
    
    LHRcore=Qcore/len(loop.xcore) #kW/mm
    LHRhex=-Qhex/len(loop.xhex)    #kW/mm
    Q_core = LHRcore*np.ones(len(loop.xcore))
    #Q_core = Qcore*loop.coreprofile
    Q_core[0:velo] = np.linspace(0,Q_core[velo],num=velo)
    Q_chimney = np.zeros(len(loop.xchimney))
    Q_hex = LHRhex*np.ones(len(loop.xhex))
    Q_hex[0:velo] = np.linspace(0,Q_hex[velo],num=velo)
    Q_downcomer = np.zeros(len(loop.xdowncomer))
    Q_x = np.concatenate((Q_core,Q_chimney,Q_hex,Q_downcomer))
    
    E_x = functions.T2mu(T_x)

    E_enter = E_x.copy()
    E_xcore=core(E_enter)
    E_xcore[-velo:] = E_xcore[-1]
    E_xhex=hex(E_enter)
    E_xhex[-velo:] = E_xhex[-1]
    E_enter = np.roll(E_enter,velo)

    E_exit = E_x.copy()
    
    dE_x = E_enter - E_exit + Q_x
    E_x += dE_x

    Tnew = functions.mu2T(E_x)
    return Tnew