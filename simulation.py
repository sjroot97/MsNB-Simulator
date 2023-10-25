#Clear command line output
import os; os.system('cls')

#Import user defined modules and third party libraries
print('import libraries')
import initial, params, loop, plots, functions, TempProfile, control
import numpy as np
#from scipy.signal import argrelextrema
from tqdm import tqdm as tqdm

#Delete image outputs in ./img/
print('refresh simulation environment')
plots.kill()


#Calculate Initial Conditions
'''
The algorithm function in the file initial.py uses binary search to identify the cold temperature that when paired with a hot temperature of 700 C gives the desired power output. It uses the natural circulation flow rate, heat capacity, and temperature difference to calculate the power for a given cold temperature, and adjusts the cold temperature as needed based on the result. 
'''
Q = 10000 #Input the starting thermal power in kW
print('determine initial conditions')
T_hot,T_cold,Q0,v = initial.algorithm(Q)
print(f'T_hot: {T_hot} degC')
print(f'T_cold: {T_cold} degC')
print(f'Power: {Q0} kW')
print(f'Velocity: {round(v*100,1)} cm/s')

#Initialize HEX transient
'''
Q0 is calculated above, Q1 is the power after the first power change, Q2 is the power after the second power change. tlen is the total time in seconds of the simulation (3600sec = 1hr). t01 is the time over which the first power change occurs (ramp function ~ use t01 = 0 for step response). t1 is the time in seconds for which the reactor is held at Q1. t12 is the time in seconds over which the second power change occurs. t2 is calculated and is the time between the end of the second power change and the end of the simulation
'''
Q1,Q2 = Q0,Q0
tlen = 3600
t01,t1,t12 = 600,600,0
t2=tlen-t01-t1-t12

print('set up HEX transient')
#forming the time array and heat exchanger power arrays
t=np.arange(0,tlen+1,params.dt) #time array
Q01 = np.linspace(Q0,Q1,num=t01)
Q11 = Q1*np.ones(t1)
Q12 = np.linspace(Q1,Q2,num=t12)
Q22 = Q2*np.ones(t2+1)
Qhex_t = np.concatenate((Q01,Q11,Q12,Q22)) #Independent variable for simulation
plots.t_vs_Q(t,Qhex_t,None)

#Define T(x)
'''
Calls function initial from file TempProfile.py, which assumes linear heat increase in the core, constant hot temperature in the riser/chimney, linear heat decrease in the heat exchanger, and constant cold temperature in the downcomer. It then plots the initial temperature profile 
'''
print('set up temperature profile')
T_x = TempProfile.initial(T_hot, T_cold)
plots.x_vs_Tx("img/animateTx_t/t-0.png",0.0,T_x,T_cold,T_hot)

#FEM
'''
With the problem defined, the 1D+time finite element model is set-up. Time arrays are initialized for the core power, flow velocity, and temperature profile, as well as reactivity. The flow reactivity is calculated, while the temperature reactivity is set to the inverse, on the assumption that the reactor is initially critical. The control drums will start at the bias point, so their reactivity is null. Then the period and reactivity rate of change are set to zero, again on the steady state critical assumption.
'''
print('set up FEM')
Qcore_t= [Q0]
v_t = [v]
T_x_t = [T_x]

Freac_t = [functions.FlowRxty(T_x)] #flow reactivity
Treac_t = [-Freac_t[0]] #temperature reactivity

CDtheta_t = [control.drum(Qhex_t[0],Qcore_t[0])] #control drum angle
Creac_t = [control.feedback(CDtheta_t[0])] #control reactivity

reac_t=[Freac_t[0]+Treac_t[0]+Creac_t[0]]
reac_dot_t = [0]
exponent=[0]

print('run simulation')
'''
The time loop makes the simulator calculate the new values necessary to advance the temperature profile. Descriptions of the functions called are included in the functions.py file. 
'''
for step in tqdm(t[1:]):
    T_x = TempProfile.advance(T_x, v ,Qcore_t[-1], Qhex_t[step-1])
    T_x_t.append(T_x)
    vnew = functions.Velo(T_x)
    v_t.append(vnew)

    Freac_t.append(functions.FlowRxty(T_x))
    Treac_t.append(Treac_t[-1] + functions.TempRxtyChange(T_x_t[-2],T_x_t[-1]))

    CDtheta_t.append(control.drum(Qhex_t[step],Qcore_t[-1]))
    Creac_t.append(control.feedback(CDtheta_t[-1]))

    reac_t.append(Freac_t[-1]+Treac_t[-1]+Creac_t[-1])
    reac_dot_t.append(functions.RoC(reac_t[-2], reac_t[-1]))

    '''
    the reactor period is defined as 0 if the new overall reactivity is 0, otherwise, it is calculated using the neutron generation time (prompt effects) and reactivity rate of change (delayed neutron effects).
    '''

    if reac_t[-1]==0:
        exponent.append(0)
    else:
        tau=params.lstar/reac_t[-1]+(params.beta_eff-reac_t[-1])/(params.lam*reac_t[-1]+reac_dot_t[-1])
        exponent.append(params.dt/tau)
    '''
    The new power is calculated using the reactor period and the previous power.
    '''
    Q=Qcore_t[-1]*np.exp(exponent[-1])
    Qcore_t.append(Q)

#Simulation done, plot data
print('plotting time arrays')
plots.t_vs_Q(t,Qhex_t,Qcore_t)
plots.t_vs_reac(t,Freac_t,Treac_t,reac_t)
plots.t_vs_exp(t,exponent)
plots.t_vs_velo(t,v_t)
plots.t_vs_angle(t,CDtheta_t)

print('plotting temperature profiles')
Tmin = np.min(np.array(T_x_t))
Tmax = np.max(np.array(T_x_t))

#Create GIF of temperature profiles
for step, T_x in tqdm(zip(t[1:],T_x_t),total=len(T_x_t)):
    if step*params.dt%60 ==0:
        path = "img/animateTx_t/t-" + str(int(round(step/60,0))) +".png"
        plots.x_vs_Tx(path, step, T_x, Tmin, Tmax)
plots.gif('img/animateTx_t')

exit()
maximums = argrelextrema(np.array(Qcore_t),np.greater)
minimums = argrelextrema(np.array(Qcore_t),np.less)

print('max', np.max(np.array(Qcore_t)))
print('local maximums')
for max in maximums:
    for i in max:
        print(round(t[int(i)]/60),Qcore_t[int(i)])


print('min', np.min(np.array(Qcore_t)))
print(' local minimums')
for min in minimums:
    for i in min:
        print(round(t[int(i)]/60),Qcore_t[int(i)])
