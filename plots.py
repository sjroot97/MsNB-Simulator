import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from adjustText import adjust_text
import numpy as np
import glob
from PIL import Image
import os
import TempProfile, loop, controller

def x_vs_Tx(path,t,T_x,Tmin,Tmax):
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f (°C)'))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f mm'))
    ymin=Tmin
    ymax=Tmax

    plt.figure(figsize=(8,4.5))
    plt.ylim(ymin-1, ymax+1)
    plt.plot(loop.xcore, TempProfile.core(T_x), label='core', color = 'red')
    plt.plot(loop.xchimney, TempProfile.chimney(T_x), label='chimney', color = 'orange')
    plt.plot(loop.xhex, TempProfile.hex(T_x), label='heat exchanger', color = 'blue')
    plt.plot(loop.xdowncomer, TempProfile.downcomer(T_x), label='downcomer', color = 'green')
    plt.xlabel('Position along Loop')
    plt.ylabel('Molten Salt Temperature')
    plt.title('Temperature (°C) along MsNB Loop, t='+ str(int(round(t/60,0)))+ 'min')
    plt.legend(loc='best')
    plt.savefig(path)
    plt.clf()
    plt.close()

def t_vs_Q(t,Qhex,Qcore,SP):
    fig,ax = plt.subplots(figsize=(8,4.5))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f MW'))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f min'))
    plt.plot(t/60,Qhex/1e3,label='Heat Exchanger',color='blue')
    plt.plot(t/60,np.array(SP)/1e3, label='Core Set-Point',color='orange',linestyle=':')
    if Qcore != None:
        Qcore = np.array(Qcore)
        plt.plot(t/60,Qcore/1e3, label='Core',color='orange')
    plt.legend(loc='best')
    plt.xlabel('time')
    plt.ylabel('Power duty and load vs. time')
    
    Quant = False
    if Quant:
        ax.grid(b=True, which='both', color='gray', linestyle='-')
        start = Qhex[0]/1e3
        stop =  Qhex[-1]/1e3
        step = stop-start
        
        print(f'minimum {np.min(Qcore)}')
        print(f'maximum {np.max(Qcore)}')
        
        delay = start+0.1*step
        rise = start+0.9*step
        settlelow,settlehigh =stop - 0.05*step, stop + 0.05*step
        
        plt.axhline(delay, linestyle=":",color='black') #delaytime 10%
        plt.axhline(rise, linestyle=":",color='black')
        plt.axhline(settlelow, linestyle=":",color='black')
        plt.axhline(settlehigh, linestyle=":",color='black')
        plt.show()
    
    plt.savefig("img/t_vs_Qt.png")
    plt.clf()
    plt.close()

def t_vs_reac(t,Flow,Temp,Total):
    plt.figure(figsize=(8,4.5))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f min'))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d pcm'))
    Flow,Temp,Total = np.array(Flow),np.array(Temp),np.array(Total)
    plt.plot(t/60,Flow*1e5,label='Flow Reactivity')
    plt.plot(t/60,Temp*1e5, label='Temperature Reactivity')
    plt.plot(t/60,Total*1e5, label='Reactivity')
    plt.xlabel('time')
    plt.ylabel('Reactivity')
    plt.legend(loc='best')
    plt.savefig("img/t_vs_reac.png")
    plt.clf()
    plt.close()
    
def auto_reac_phase(Flow,Temp,Times):
    plt.figure(figsize=(8,4.5))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.d pcm'))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.d pcm'))
    Flow,Temp = np.array(Flow)*1e5,np.array(Temp)*1e5
    max = np.max(np.array([np.max(Temp),-np.min(Flow)]))
    min = np.min(np.array([np.min(Temp),-np.max(Flow)]))
    pad = 3
    plt.xlim(min-pad,max+pad)
    plt.ylim(-max-pad,-min+pad)
    
    plt.plot(Temp,Flow,color='blue')
    plt.plot([max,min],[-max,-min],linestyle=':',color='black',alpha=0.5)
    timeslices = np.cumsum(np.trim_zeros(np.array(Times),'b'))
    plt.scatter(Temp[timeslices],Flow[timeslices],color='darkorange',zorder=5)

    ts,texts = [],[]
    for t,F,T in zip(timeslices,Flow[timeslices],Temp[timeslices]):
        text = f'  {t//60} min  '
        if text not in texts: 
            texts.append(text)
            ts.append(plt.text(T,F,text))

    plt.tight_layout()
    xavoid = np.concatenate((Temp,np.linspace(max,min,num=100)))
    yavoid = np.concatenate((Flow,np.linspace(-max,-min,num=100)))
    adjust_text(ts,x=xavoid,y=yavoid,force_text=0.2,force_points=0.2,arrowprops={'arrowstyle':'->','color':'darkorange'})
    plt.xlabel('Temperature Reactivity')
    plt.ylabel('Flow Reactivity')
    
    plt.gca().locator_params(axis='both', nbins=6)
    
    plt.title('Passive Feedback Phase Space')
    plt.savefig("img/auto_reac_phase.png",bbox_inches='tight')
    plt.clf()
    plt.close()
    
def contr_reac_phase(Flow,Temp,Control,Times):
    plt.figure(figsize=(8,4.5))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.d pcm'))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.d pcm'))
    Flow,Temp,Control = np.array(Flow)*1e5,np.array(Temp)*1e5,np.array(Control)*1e5
    Passive = Flow+Temp
    max = np.max(np.array([np.max(Passive),-np.min(Control)]))
    min = np.min(np.array([np.min(Passive),-np.max(Control)]))
    pad = 3
    plt.xlim(min-pad,max+pad)
    plt.ylim(-max-pad,-min+pad)
    
    plt.plot(Passive,Control,color='blue')
    plt.plot([max,min],[-max,-min],linestyle=':',color='black',alpha=0.5)
    timeslices = np.cumsum(np.trim_zeros(np.array(Times),'b'))
    plt.scatter(Passive[timeslices],Control[timeslices],color='darkorange',zorder=5)

    ts,texts = [],[]
    for t,P,C in zip(timeslices,Passive[timeslices],Control[timeslices]):
        text = f'  {t//60} min  '
        if text not in texts: 
            texts.append(text)
            ts.append(plt.text(P,C,text))
        

    plt.tight_layout()
    xavoid = np.concatenate((Passive,np.linspace(max,min,num=100)))
    yavoid = np.concatenate((Control,np.linspace(-max,-min,num=100)))
    adjust_text(ts,x=xavoid,y=yavoid,force_text=0.2,force_points=0.2,arrowprops={'arrowstyle':'->','color':'darkorange'})
    plt.xlabel('Passive Reactivity')
    plt.ylabel('Control Drum Reactivity')
    
    plt.gca().locator_params(axis='both', nbins=6)
    
    plt.title('Controlled Feedback Phase Space')
    plt.savefig("img/contr_reac_phase.png",bbox_inches='tight')
    plt.clf()
    plt.close()

def t_vs_exp(t,exp):
    plt.figure(figsize=(8,4.5))
    plt.plot(t/60,exp)
    plt.xlabel('time')
    plt.ylabel('dT (sec) per Reactor Period (sec)')
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f min'))
    plt.savefig("img/t_vs_exponent.png")
    plt.clf()
    plt.close()

def t_vs_velo(t,v):
    plt.figure(figsize=(8,4.5))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f cm/s'))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f min'))
    v=np.array(v)
    plt.plot(t/60,v*100)
    plt.xlabel('time')
    plt.ylabel('Flow Velocity')
    plt.savefig("img/t_vs_velocity.png")
    plt.clf()
    plt.close()

def t_vs_angle(t,theta):
    offset = np.floor(controller.bias)
    theta -= offset
    #dtheta = np.diff(theta,append=0)
    fig,ax = plt.subplots(figsize=(8,4.5))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f°'))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f min'))
    #plt.ylim(np.floor(np.min(theta)),t[-1]/60)
    #plt.yticks(np.array([0,15,30,45,60,75,90,105,120,135,150,165,180]))
    plt.text(0,1.01,f'+{offset}°',transform=ax.transAxes)
    plt.plot(t/60,theta)
    #plt.plot(t/60,dtheta)

    plt.xlabel('time')
    plt.ylabel("Control Drum Orientation")

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
            pass
            #os.remove(os.path.join(dir,f))
