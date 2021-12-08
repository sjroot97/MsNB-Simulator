#Transient
t   = 3600 #sec
Q0  = 300  #kW
t01 = 600  #sec
Q1  = 340  #kW
t1  = 600  #sec
t12 = 600  #sec
Q2  = Q0
t2=t-t01-t1-t12

#Proportional Control Loop
#Control = 'On'
Control = 'Off'
bias = 120.14
gain = {'On':1e-4, 'Off':0}
