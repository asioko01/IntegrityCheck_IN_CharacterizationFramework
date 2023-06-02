'''
Created on 15 Jun 2017

@author: zachad01
'''
from setVoltageThroughSerial import setVoltage
from setFrequencyThroughSerial import setFrequency
from sendRebootCommand import sendRebootCommand
from getLowestVol import getLowestVol
from numpy import fft
import numpy as np
import os
import shutil
import fileinput
from paramiko import SSHClient
from paramiko import client
import paramiko
import socket
#from setFrequencyThroughDebugger import setFrequency

def fftwrapper(values,timestep,fname=None):
    
    signal = np.array(values,dtype=float)
    fourier = fft.fft(signal)
    n = signal.size
    timestep = 1/float(1600)
    freqs = fft.fftfreq(n, d=timestep)
    samples=0
    freqsToReturn=[]
    ampsToReturn=[]
    for freq,coef in zip(freqs,fourier):
        samples=samples+1
        if samples==1:
            continue #ignore the first frequency
        if samples > (len(values)/2): # dont plot the negative frequencies
            break
        #print(str(freq)+" "+str(np.abs(coef)))
        freqsToReturn.append(freq)
        ampsToReturn.append(np.abs(coef))
    
    if fname is not None:
        f=open(fname,"w")
        f.write("freq(MHz) Amp(mV) \n")
        for fre,amp in zip(freqsToReturn,ampsToReturn):
            f.write(str(fre)+" "+str(amp)+"\n")
        f.close()
    
    return freqsToReturn,ampsToReturn

def executeCommand(command):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
    ssh.connect("juno_uni.in.cs.ucy.ac.cy", username="root", password="UniServer")
    stdin,stdout,stderr=ssh.exec_command(command)
    out=stdout.readlines() #just do this to make exec blocking call
    err=stderr.readlines()            
    ssh.close()
    return out

SCRIPTS_BASE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/"
SET_FREQUENCY_BAT="RUN_DS5_changeFreq.bat"
SET_FREQUENCY_PY="changeFrequency.py"
nominal=0.9
nominalVol=nominal*1000
LAST_MEAS_FILE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/tmp"
iterat=3

#frequency=1284 #in MHZ
#frequency=1200
#frequency=1200
setVoltage(1, nominal, "COM7")
#setFrequency(1400, portCOM="COM7", multiplier=20, supply=7)
#setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)

#sendRebootCommand("COM7")

command="cd /home/zhadji01/ga; taskset -c 4 ./individual &>/dev/null &  taskset -c 5 ./individual &>/dev/null & exit"
while True:
    try:
        executeCommand(command=command)
        break;
    except(paramiko.SSHException,paramiko.BadHostKeyException,paramiko.AuthenticationException,socket.error):
        continue

print ("OUTPUT cpuFreq 99thDroop maxDroop 99thOvershoot maxOvershoot peak-peak(99th) peak-peak peakFreq peakAmp")
for freq in range(300,1200,50):
    setFrequency(freq, portCOM="COM7", multiplier=20, supply=7)
    #vol=getLowestVol(reps=1)
    #droop=nominal*1000-vol
    #print("OUTPUT "+str(freq)+" "+str(droop))
    mvs=[]
    freqs=[]
    amps=[]
    maxAmpFreq=0
    maxAmp=0
    index=-1
    for reps in range(iterat):
        os.system("cd \"C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS\" && RUN_DS5_measMV.bat && exit")
        
        for line in fileinput.input(LAST_MEAS_FILE):
            mvs.append(int(line))
            #min=int(line)
            #break
        if reps == 0:
            freqs,amps=fftwrapper(mvs, 1/1600,"C:/cygwin64/home/admin/freqSweepResults/"+str(int(freq))+"_fft")
            maxAmpFreq=0
            maxAmp=0
            index=-1
            for i in range(len(amps)):
                if(freqs[i]>200): #dont care about freqs above 200MHz
                    break
                if(amps[i]>maxAmp):
                    maxAmp=amps[i]
                    index=i
            maxAmpFreq=freqs[index]
            
    mvs.sort(reverse=True)
    toReturn=int(float(len(mvs))*0.99609375)
    min=mvs[toReturn]
    fileinput.close()
    
    print("OUTPUT "+str(freq)+" "+str(nominalVol-min)+" "+str(nominalVol-mvs[-1])+" "+str(mvs[7]-nominalVol)+" "+str(mvs[0]-nominalVol)+" "+str(mvs[7]-min)+" "+str(mvs[0]-mvs[-1])+" "+str(maxAmpFreq)+" "+str(maxAmp))