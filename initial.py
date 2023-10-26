import params, functions, TempProfile
import numpy as np

#Initialize Operating Range
Tmax = 700
Tmin = 600
dTmax= Tmax-Tmin


def MassFlow(T_x):     #input Celcius
    '''This function is called by Power in this file.'''
    v = functions.Velo(T_x)            #calculate fluid velocity
    rho=functions.density(functions.list_ave(TempProfile.hex(T_x))) #calculate average density of regime
    return rho*v*params.Ax,v          #output kg/s
#________________________________________________________________________

def Power(Th,Tc):                 #Input Celcius
    '''This function is called by algorithm in this file.'''
    T_x = TempProfile.initial(Th, Tc)
    m,v = MassFlow(T_x)
    cp_bar = functions.cp(functions.list_ave(TempProfile.hex(T_x)))                   #Calculate average heat capacity of regime
    dT = Th-Tc                          #Calculate temperature difference across regime
    power = m*cp_bar*dT
    return power,v   #Output kW

def algorithm(Q): #performs a binary search
    '''
    This function is called by the <Calculate Initial Conditions> block of simulation.py. It first checks the power from 700 to 600. Then uses binary search to change the cold temperature until the desired power is obtained, to a defined number of sig figs. Change variables Tmax and Tmin in this file to adjust the starting cold temp or hot temp
    '''
    dT = dTmax
    T_cold = Tmax-dT 
    Qcalc,_ = Power(Tmax,T_cold)
    error = Qcalc-Q
    
    dTs = [2*dT,dT] #setup for binary search
    
    i = 0
    while round(error,1): #Binary search, adjust the number in the second argument to change the rounding (decimal places of kW)
        change = abs(dTs[-2]-dTs[-1])*0.5 #how much should the cold temperature be adjusted by?
        if error>0: #positive, need less power
            dT -= change #increase cold temperature
        elif error<0: #negative, need more power
            dT += change #decrease cold temperature
        
        dTs.append(dT) #store temperature differential
        T_cold = Tmax-dT #calculate new cold temperature
        Qcalc,v = Power(Tmax,T_cold)  #calculate new Power
        error = Qcalc-Q #calculate difference between new power and desired power
        i +=1
    print(f'{i} binary search operations')
    return Tmax, T_cold, Qcalc, v
