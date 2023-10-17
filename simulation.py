import os; os.system('cls')
print('import libraries')
import inputs, initial, params, loop, plots, functions, TempProfile, control
import numpy as np
from scipy.signal import argrelextrema
from tqdm import tqdm as tqdm

print('refresh simulation environment')
plots.kill()

#Calculate Initial Conditions
Q = 10000
print('determine initial conditions')
T_hot,T_cold,Q0,v = initial.algorithm(Q)
print(f'T_hot: {T_hot} degC')
print(f'T_cold: {T_cold} degC')
print(f'Power: {Q0} kW')
print(f'Velocity: {round(v*100,1)} cm/s')

#Define T(x)
print('set up temperature profile')
T_x = TempProfile.initial(T_hot, T_cold)
plots.x_vs_Tx("img/animateTx_t/t-0.png",0.0,T_x,T_cold,T_hot)

#Initialize HEX transient
Q1,Q2 = 8000,Q0
tlen = 3600
t01,t1,t12 = 600,600,600
t2=tlen-t01-t1-t12

print('set up HEX transient')
t=np.arange(0,tlen+1,params.dt)
Q01 = np.linspace(Q0,Q1,num=t01)
Q11 = Q1*np.ones(t1)
Q12 = np.linspace(Q1,Q2,num=t12)
Q22 = Q2*np.ones(t2+1)
Qhex_t = np.concatenate((Q01,Q11,Q12,Q22))
plots.t_vs_Q(t,Qhex_t,None)

#FEM
print('set up FEM')
Qcore_t= [Q0]
v_t = [v]
T_x_t = [T_x]

Freac_t = [functions.FlowRxty(T_x,v)]
Treac_t = [-Freac_t[0]]

CDtheta_t = [control.drum(Qhex_t[0],Qcore_t[0])]
Creac_t = [control.feedback(CDtheta_t[0])]

reac_t=[Freac_t[0]+Treac_t[0]+Creac_t[0]]
reac_dot_t = [0]
exponent=[0]

print('run simulation')
for step in tqdm(t[1:]):
    T_x = TempProfile.advance(T_x, v ,Qcore_t[-1], Qhex_t[step-1])
    v_t.append(v)
    #v_t.append(functions.Velo(T_x))
    T_x_t.append(T_x)

    Freac_t.append(functions.FlowRxty(T_x,v))
    Treac_t.append(Treac_t[-1] + functions.TempRxtyChange(T_x_t[-2],T_x_t[-1]))

    CDtheta_t.append(control.drum(Qhex_t[step],Qcore_t[-1]))
    Creac_t.append(control.feedback(CDtheta_t[-1]))

    reac_t.append(Freac_t[-1]+Treac_t[-1]+Creac_t[-1])
    reac_dot_t.append(functions.RoC(reac_t[-2], reac_t[-1]))

    if reac_t[-1]==0:
    #if 1==1:
        exponent.append(0)
    else:
        tau=params.lstar/reac_t[-1]+(params.beta_eff-reac_t[-1])/(params.lam*reac_t[-1]+reac_dot_t[-1])
        exponent.append(params.dt/tau)

    Q=Qcore_t[-1]*np.exp(exponent[-1])
    Qcore_t.append(Q)



print('plotting temperature profiles')
Tmin = np.min(np.array(T_x_t))
Tmax = np.max(np.array(T_x_t))

for step, T_x in tqdm(zip(t[1:],T_x_t),total=len(T_x_t)):
    if step*params.dt%60 ==0:
        path = "img/animateTx_t/t-" + str(int(round(step/60,0))) +".png"
        plots.x_vs_Tx(path, step, T_x, Tmin, Tmax)
plots.gif('img/animateTx_t')

print('plot other properties')
plots.t_vs_Q(t,Qhex_t,Qcore_t)
plots.t_vs_reac(t,Freac_t,Treac_t,reac_t)
plots.t_vs_exp(t,exponent)
plots.t_vs_velo(t,v_t)
plots.t_vs_angle(t,CDtheta_t)

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
