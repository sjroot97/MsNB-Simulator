import numpy as np
import control as ct

#Prefilter
def prefilter(Qhex,time,tau):
    num = [1]
    den = [tau,1]
    pf = ct.TransferFunction(num,den)
    response_in = Qhex-Qhex[0]
    _,response_out = ct.forced_response(pf,T=time,U=response_in)
    Qcore_SP = Qhex[0] + response_out
    return Qcore_SP

#Proportional Control Loop
Control = 'On'
#Control = 'Off'
bias = 120.14
gain = {'On':4e-4, 'Off':0}


def drum(Qhex,Qcore):
    error = Qhex-Qcore
    angle = bias + gain[Control]*error
    return angle

def feedback(angle):
    reac=0
    if Control == 'On':
        reac = -0.02768 - 0.0717*np.cos(1.5*np.deg2rad(angle)-1.1781)
    return reac
