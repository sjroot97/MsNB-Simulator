import params, functions
import numpy as np

#Initialize Operating Range
Tmax = 700
Tmin = 600
dTmax= Tmax-Tmin


def DiffP(Th,Tc): #input Celcius
    hot=functions.density(Th) #calculate average density of hot leg
    cold=functions.density(Tc)#calculate average density of cold leg
    return (cold-hot)*params.h*9.81  #output Pa

def Velo(Th,Tc):   #input Celcius
    DrivingForce=DiffP(Th,Tc) #Convert Differential Pressure
    rho=functions.density((Th + Tc)/2) #Calculate Average Density of entire Loop
    v_squared = (2*DrivingForce)/(params.xi*rho)
    v = np.sqrt(v_squared)
    #print(f'{round(v*100,1)} cm/s')
    return v   #output m/s

def MassFlow(Th,Tc):     #input Celcius
    v = Velo(Th,Tc)            #calculate fluid velocity
    rho=functions.density((Th + Tc)/2) #calculate average density of regime
    return rho*v*params.Ax,v          #output kg/s
#___________________________________________________________________________

def Power(Th,Tc):                 #Input Celcius
    m,v = MassFlow(Th,Tc)           #calculate Mass Flow Rate
    cp_bar = functions.cp((Th+Tc)/2)                   #Calculate average heat capacity of regime
    dT = Th-Tc                          #Calculate temperature difference across regime
    power = m*cp_bar*dT
    return power,v   #Output kW

def algorithm(Q): #performs a binary seach
    dT = dTmax
    T_cold = Tmax-dT 
    Qcalc,_ = Power(Tmax,T_cold)
    error = Qcalc-Q
    
    dTs = [2*dT,dT] #setup for binary search
    
    i = 0
    while round(error,3):
        change = abs(dTs[-2]-dTs[-1])*0.5
        if False:
            break
        if error>0: #positive, need less power
            dT -= change 
        elif error<0: #negative, need more power
            dT += change
        
        dTs.append(dT)
        T_cold = Tmax-dT
        Qcalc,v = Power(Tmax,T_cold)
        error = Qcalc-Q
        i +=1
    print(f'{i} binary search operations')
    return Tmax, T_cold, Qcalc,v
