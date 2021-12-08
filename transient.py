import numpy as np

def array(Q0,Q1,Q2,t01,t1,t12,t2):
    Q01 = np.linspace(Q0,Q1,num=t01)
    Q11 = Q1*np.ones(t1)
    Q12 = np.linspace(Q1,Q2,num=t12)
    Q22 = Q2*np.ones(t2+1)
    Qhex = np.concatenate((Q01,Q11,Q12,Q22))
    return Qhex
