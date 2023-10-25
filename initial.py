import params, functions
import numpy as np

#Initialize Operating Range
Tmax = 700
Tmin = 600
dTmax= Tmax-Tmin


def DiffP(Th,Tc): #input Celcius
    '''This function is called by DiffP in this file.'''
    hot=functions.density(Th) #calculate average density of hot leg
    cold=functions.density(Tc)#calculate average density of cold leg
    return (cold-hot)*params.h*9.81  #output Pa

def Velo(Th,Tc):   #input Celcius
    '''This function is called by MassFlow in this file.'''
    DrivingForce=DiffP(Th,Tc) #Convert Differential Pressure
    rho=functions.density((Th + Tc)/2) #Calculate Average Density of entire Loop
    v_squared = (2*DrivingForce)/(params.xi*rho)
    v = np.sqrt(v_squared)
    #print(f'{round(v*100,1)} cm/s')
    return v   #output m/s

def MassFlow(Th,Tc):     #input Celcius
    '''This function is called by Power in this file.'''
    v = Velo(Th,Tc)            #calculate fluid velocity
    rho=functions.density((Th + Tc)/2) #calculate average density of regime
    return rho*v*params.Ax,v          #output kg/s
#___________________________________________________________________________

def Power(Th,Tc):                 #Input Celcius
    '''This function is called by algorithm in this file.'''
    m,v = MassFlow(Th,Tc)           #calculate Mass Flow Rate
    cp_bar = functions.cp((Th+Tc)/2)                   #Calculate average heat capacity of regime
    dT = Th-Tc                          #Calculate temperature difference across regime
    power = m*cp_bar*dT
    return power,v   #Output kW



def algorithm(Q): #performs a binary seach
    '''
    This function is called by the <Calculate Initial Conditions> block of simulation.py. It first checks the power from 700 to 600. Then uses binary search to change the cold temperature until the desired power is obtained, to a defined number of sig figs. Change variables Tmax and Tmin in this file to adjust the starting cold temp or hot temp
    '''
    dT = dTmax
    T_cold = Tmax-dT 
    Qcalc,_ = Power(Tmax,T_cold)
    error = Qcalc-Q
    
    dTs = [2*dT,dT] #setup for binary search
    
    i = 0
    while round(error,3): #Binary search, adjust the number in the second argument to change the rounding (decimal places of kW)
        change = abs(dTs[-2]-dTs[-1])*0.5 #how much should the cold temperature be adjusted by?
        
        if error>0: #positive, need less power
            dT -= change  #increase cold temperature
        elif error<0: #negative, need more power
            dT += change #decrease cold temperature
        
        dTs.append(dT) #store temperature differential
        T_cold = Tmax-dT #calculate new cold temperature
        Qcalc,v = Power(Tmax,T_cold) #calculate new Power
        error = Qcalc-Q #calculate difference between new power and desired power
        i +=1 #count cycle
    print(f'{i} binary search operations')
    return Tmax, T_cold, Qcalc,v
