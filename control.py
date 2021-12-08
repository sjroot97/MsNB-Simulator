import inputs
import numpy as np
import matplotlib.pyplot as plt

def drum(Qhex,Qcore):
    error = Qhex-Qcore
    angle = inputs.bias + inputs.gain[inputs.Control]*error
    return angle

def feedback(angle):
    reac=0
    if inputs.Control == 'On':
        reac = -0.02768 - 0.0717*np.cos(1.5*np.deg2rad(angle)-1.1781)
    return reac
