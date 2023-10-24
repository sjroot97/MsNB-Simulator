#import whatever we need
import params, loop, TempProfile
import numpy as np
#from pynverse import inversefunc
#___________________________________________________________________________
#___________________________________________________________________________
#___________________________________________________________________________

#Basic Calculations
def absT(T):            #input Celcius
    return T+273.15     #output Kelvin
#___________________________________________________________________________

def base_to_kilo(x):    #input base
    return x/1000       #output kilo
#___________________________________________________________________________

def kilo_to_base(x):    #input kilo
    return x*1000       #output base
#___________________________________________________________________________

def base_to_centi(x):   #input base
    return x*100        #output centi
#___________________________________________________________________________

def base_to_milli(x):   #input base
    return x*1000        #output milli
#___________________________________________________________________________

def list_ave(list):                 #input list
    return sum(list)/len(list)      #output float
#___________________________________________________________________________

def RoC(x1,x2): #time rate of change
    return (x2-x1)/params.dt
#___________________________________________________________________________
#___________________________________________________________________________

#Physical Properties
def cp(T):                          #input Celcius
    T=absT(T)                       #Convert T to Kelvin
    return (1.0634*T+976.78)/1000          # output kJ/kg-K
#___________________________________________________________________________

def density(T):                              #input Celcius
    T=absT(T)                                #Convert T to Kelvin
    return 1000*(4.6820365-T*9.4601046e-4)   #output kg/m3\
        
def T2mu(T):
    Tref = 600
    m_x = density(T)*(params.Ax*.001) #kg
    u_x = cp((T+Tref)/2)*(T-Tref)
    E_x = m_x*u_x
    return E_x

#T2mu_inverse = inversefunc(T2mu)

TempArray = np.linspace(500,900,num=10000)
EnergyArray = T2mu(TempArray)

coeff = np.polyfit(EnergyArray,TempArray,3)

def mu2T(E):
    value = np.zeros(len(E))
    for c in coeff:
        value = value*E+c
    return value

#___________________________________________________________________________
#___________________________________________________________________________

#System Quantities
def DiffP(T_x):                 #input Celcius

    hot=density(list_ave(TempProfile.chimney(T_x)))
    #hot=density(list_ave(np.concatenate((TempProfile.chimney(T_x),TempProfile.core(T_x)))))             #calculate average density of hot leg
    cold=density(list_ave(TempProfile.downcomer(T_x)))            #calculate average density of cold leg
    return (cold-hot)*params.h*9.81     #output Pa
#___________________________________________________________________________

def Velo(T_x):                                 #input Celcius
    DrivingForce=DiffP(T_x)                    #Convert Differential Pressure
    rho=density(list_ave(T_x))                #Calculate Average Density of entire Loop
    v_squared = (2*DrivingForce)/(params.xi*rho)
    if v_squared<0.05**2:    v_squared=0.05**2
    if v_squared>0.15**2:    v_squared=0.10**2
    v = np.sqrt(v_squared)   #output m/s
    return v# 0.05 #m/s
#___________________________________________________________________________

def MassFlow(T_x, regime):     #input Celcius
    v = Velo(T_x)            #calculate fluid velocity
    if regime == "core":
        list = TempProfile.core(T_x)
        Tave = list_ave(list)    #calculate average temperature in regime
    elif regime == "hex":
        list = TempProfile.hex(T_x)
        Tave = list_ave(list)    #calculate average temperature in regime
    rho=density(Tave)          #calculate average density of regime
    return rho*v*params.Ax          #output kg/s

#___________________________________________________________________________

#___________________________________________________________________________
#___________________________________________________________________________

#Reactivity
def TempRxtyChange(previous,current):      #input Celcius
    T1=list_ave(TempProfile.core(previous))
    T2=list_ave(TempProfile.core(current))
    dT=T2-T1         #convert T from Celcius to Kelvin
    return params.alphaT*dT #unitless
#___________________________________________________________________________

def FlowRxty(T_x):                                    #input Celcius
    v=base_to_centi(Velo(T_x))                               #calculate fluid velocity
    L = loop.Ri2-loop.Ro                                       #calculate out of core path length
    H = loop.Ro-loop.Ri1                                       #calculate in core path length
    rho = -(L/(L+H))*params.beta_eff*(1-np.exp(-params.alphaF*v)) #unitless
    return rho
#___________________________________________________________________________
