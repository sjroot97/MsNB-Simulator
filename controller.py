import functions
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
Control = True
#Control = False
bias = 111.41092285851987
Ku,Tu = 3e-4,45
KP = 0.45*Ku
tau_int = 0.83333*Tu
KI = KP/tau_int
tau_der = 0
KD = KP*tau_der

angle_memory = bias

cumu_error = 0
error_memory = 0
def drum(error):
    inst_error = error
    global cumu_error  #preserve cumulative error from one call to next
    cumu_error += error
    global error_memory #preserve previous error
    roc_error = functions.RoC(error_memory, error)
    error_memory = error
    
    angle = bias + KP*inst_error \
          + KI*cumu_error \
          + KD*roc_error

    return angle

coeff = [-2.79662670e-09,
         1.78852923e-06,
         -4.36111940e-04,
         4.82874795e-02,
         -2.00900479e+00]

def angle2reac(angle):
    reac = 0
    if not Control:
        return reac
    else: 
        for c in coeff:
            reac = reac*angle+c
    return reac