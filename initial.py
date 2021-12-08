import params, functions
import numpy as np

#Initialize Operating Range
Tmax = 700
Tmin = 600
dTmax=4
dTmin=1
dT0 = (dTmax+dTmin)/2

def DiffP(Th,Tc):                 #input Celcius
    hot=functions.density(Th)             #calculate average density of hot leg
    cold=functions.density(Tc)            #calculate average density of cold leg
    return (cold-hot)*params.h*9.81     #output Pa

def Velo(Th,Tc):                                 #input Celcius
    DrivingForce=DiffP(Th,Tc)                    #Convert Differential Pressure
    rho=functions.density((Th + Tc)/2)                #Calculate Average Density of entire Loop
    v_squared = (2*DrivingForce)/(params.xi*rho)
    #return np.sqrt(v_squared)   #output m/s
    return 0.05 #m/s

def MassFlow(Th,Tc,Ti,To):     #input Celcius
    v = Velo(Th,Tc)            #calculate fluid velocity
    rho=functions.density((Th + Tc)/2)           #calculate average density of regime
    return rho*v*params.Ax          #output kg/s
#___________________________________________________________________________

def Power(Th,Tc,Ti,To):                 #Input Celcius
    m = MassFlow(Th,Tc,Ti,To)           #calculate Mass Flow Rate
    cp_bar = functions.cp((Ti+To)/2)                   #Calculate average heat capacity of regime
    dT = To-Ti                          #Calculate temperature difference across regime
    return(functions.base_to_kilo(m*cp_bar*dT))   #Output kW

def algorithm(Q):
    Qmax= Power(Tmax+dTmax,Tmax-dTmax,Tmax-dTmax,Tmax+dTmax)
    Qmin= Power(Tmin+dTmin,Tmin-dTmin,Tmin-dTmin,Tmin+dTmin)
    if Q>Qmax:
        print('Out of range, too large')
    elif Q<Qmin:
        print('Out of range, too small')
    else:
        step=1
        Ts = np.arange(Tmin,Tmax+step,step)
        Qs = Power(Ts+dT0,Ts-dT0,Ts-dT0,Ts+dT0)
        Qres = np.abs(Q-Qs)
        i = np.where(Qres==np.amin(Qres))
        T = Ts[i]

        step=0.005
        dTs = np.arange(dTmin, dTmax+step, step)
        Qs = Power(T+dTs,T-dTs,T-dTs,T+dTs)
        Qres = np.abs(Q-Qs)
        i = np.where(Qres==np.amin(Qres))
        dT = dTs[i]
        Qcalc = Power(T+dT,T-dT,T-dT,T+dT)
        return [T, dT, Qcalc]
