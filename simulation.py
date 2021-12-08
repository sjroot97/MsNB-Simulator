import inputs, initial, params, loop, transient, plots, functions, TempProfile, control
import numpy as np

plots.kill()

#Define starting conditions
list = initial.algorithm(inputs.Q0)
T=round(float(list[0]),1)
dT=round(float(list[1]),3)
Q0=round(float(list[2]),2)

T_hot=T+dT
T_cold=T-dT

#Initialize T(x)
T_x = TempProfile.initial(T_hot, T_cold)
plots.x_vs_Tx("img/x_vs_Tx_initial.png",0.0,T_x)

#Initialize transient
t=np.arange(0,inputs.t+1,params.dt)
Qhex_t=transient.array(Q0,inputs.Q1,inputs.Q2,inputs.t01,inputs.t1,inputs.t12,inputs.t2)

#FEM
for step in t:
    if step == 0:
        Qcore_t= [Q0]
        v_t = [functions.Velo(T_x)]
        T_x_t = [T_x]

        Freac_t = [functions.FlowRxty(T_x)]
        Treac_t = [-Freac_t[-1]]

        CDtheta_t = [control.drum(Qhex_t[step],Qcore_t[-1])]
        Creac_t = [control.feedback(CDtheta_t[-1])]

        reac_t=[Freac_t[-1]+Treac_t[-1]+Creac_t[-1]]
        reac_dot_t = [0]
        exponent=[0]
    else:
        T_x = TempProfile.advance(T_x, v_t[-1] ,Qcore_t[-1], Qhex_t[step-1])
        T_x_t.append(T_x)
        v_t.append(functions.Velo(T_x))

        Freac_t.append(functions.FlowRxty(T_x))
        Treac_t.append(Treac_t[step-1] + functions.TempRxtyChange(T_x_t[step-1],T_x_t[step]))

        CDtheta_t.append(control.drum(Qhex_t[step],Qcore_t[-1]))
        Creac_t.append(control.feedback(CDtheta_t[-1]))

        reac_t.append(Freac_t[-1]+Treac_t[-1]+Creac_t[-1])
        reac_dot_t.append(functions.RoC(reac_t[step-1], reac_t[step]))

        if reac_t[-1]==0:
        #if 1==1:
            exponent.append(0)
        else:
            tau=params.lstar/reac_t[step]+params.beta_eff*reac_t[step]/(params.lam*reac_t[step]+reac_dot_t[step])
            exponent.append(params.dt/tau)

        Q=Qcore_t[step-1]*np.exp(exponent[-1])
        Qcore_t.append(Q)

    if step*params.dt%60 ==0:
        plots.x_vs_Tx("img/animateTx_t/t-" + str(int(round(step/60,0))) +".png",step, T_x)
        print(step)

plots.t_vs_Q(t,Qhex_t,Qcore_t)
plots.gif('img/animateTx_t')
plots.t_vs_reac(t,Freac_t,Treac_t,reac_t)
plots.t_vs_exp(t,exponent)
#plots.t_vs_velo(t,v_t)
plots.t_vs_angle(t,CDtheta_t)
