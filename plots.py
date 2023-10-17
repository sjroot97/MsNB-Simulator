import matplotlib.pyplot as plt
import numpy as np
import glob
from PIL import Image
import os
import TempProfile, functions, loop

def x_vs_Tx(path,t,T_x,Tmin,Tmax):
    ymin=Tmin
    ymax=Tmax

    plt.figure()
    plt.ylim(ymin-1, ymax+1)
    plt.plot(loop.xcore, TempProfile.core(T_x), label='core', color = 'red')
    plt.plot(loop.xchimney, TempProfile.chimney(T_x), label='chimney', color = 'orange')
    plt.plot(loop.xhex, TempProfile.hex(T_x), label='heat exchanger', color = 'blue')
    plt.plot(loop.xdowncomer, TempProfile.downcomer(T_x), label='downcomer', color = 'green')
    plt.xlabel('Position along Loop, x (mm)')
    plt.ylabel('Temperature at position x, T(x) (°C)')
    plt.title('Temperature (°C) along MsNB Loop, t='+ str(int(round(t/60,0)))+ 'min')
    plt.legend(loc='best')
    plt.savefig(path)
    plt.clf()
    plt.close()

def t_vs_Q(t,Qhex,Qcore):
    plt.figure()
    plt.ylim(0,11000)
    plt.plot(t/60,Qhex,label='Heat Exchanger')
    if Qcore != None:
        plt.plot(t/60,Qcore, label='Core')
        plt.legend(loc='best')
    plt.xlabel('time, t (min)')
    plt.ylabel('Heat Exchanger Power Demand at time t, Q_hex(t) (kW)')
    plt.savefig("img/t_vs_Qt.png")
    plt.clf()
    plt.close()

def t_vs_reac(t,Flow,Temp,Total):
    plt.figure()
    #plt.plot(t/60,Flow,label='Flow Reactivity')
    #plt.plot(t/60,Temp, label='Temperature Reactivity')
    plt.plot(t/60,Total, label='Reactivity')
    plt.xlabel('time, t (min)')
    plt.ylabel('Reactivity')
    #plt.legend(loc='best')
    plt.savefig("img/t_vs_reac.png")
    plt.clf()
    plt.close()

def t_vs_exp(t,exp):
    plt.figure()
    plt.plot(t/60,exp)
    plt.xlabel('time, t (min)')
    plt.ylabel('dT (sec) per Reactor Period (sec)')
    plt.savefig("img/t_vs_exponent.png")
    plt.clf()
    plt.close()

def t_vs_velo(t,v):
    plt.figure()
    plt.plot(t/60,v)
    plt.xlabel('time, t (min)')
    plt.ylabel('velocity, v (m/sec)')
    plt.savefig("img/t_vs_velocity.png")
    plt.clf()
    plt.close()

def t_vs_angle(t,theta):
    plt.figure()
    plt.ylim(120.139,120.141)
    plt.xlim(t[0],t[-1]/60)
    #plt.yticks(np.array([0,15,30,45,60,75,90,105,120,135,150,165,180]))
    plt.plot(t/60,theta)
    plt.xlabel('time, t (min)')
    plt.ylabel("Control Drum Orientation (°)")
    plt.savefig("img/t_vs_angle.png")
    plt.clf()
    plt.close()

def gif(frame_folder):
    frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.PNG"), key=os.path.getmtime)]
    frame_one = frames[0]
    frame_one.save("img/Tx_t.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)

def kill():
    import os
    dir= 'img/animateTx_t'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir,f))
    dir= 'img'
    for f in os.listdir(dir):
        if os.path.isfile(os.path.join(dir,f)):
            os.remove(os.path.join(dir,f))
