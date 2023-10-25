import numpy as np

#Proportional Control Loop
#Control = 'On'
Control = 'Off'
bias = 120.14
gain = {'On':1e-4, 'Off':0}

def drum(Qhex,Qcore):
    error = Qhex-Qcore
    angle = bias + gain[Control]*error
    return angle

def feedback(angle):
    reac=0
    if Control == 'On':
        reac = -0.02768 - 0.0717*np.cos(1.5*np.deg2rad(angle)-1.1781)
    return reac
