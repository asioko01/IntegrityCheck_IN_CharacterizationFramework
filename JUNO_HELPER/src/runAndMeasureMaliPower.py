'''
Created on 15 Jun 2017

@author: zachad01
'''
from setVoltageThroughSerial import setVoltage
from setFrequencyThroughSerial import setFrequency
from sendRebootCommand import sendRebootCommand
from readPowerSerial import readPower
from getLowestVol import getLowestVol
from executeCommandSSH import executeCommand
from threading import Thread
from paramiko import SSHClient, client
from pip._vendor.colorama.ansi import Back
#from setFrequencyThroughDebugger import setFrequency

#def executeSSHcommand(workload, commandPostFix):
#    command="cd /media/oldusb/benchmarks/maliBenchmarks/parboil; "+commandPostFix
#    executeCommand(hostname=hostname,username="root",password="",command=command,background=False)

def readPowerContinously(powerValues):
    while stop==False:
        power=readPower("COM8","w",3,False)
        print(str(power))
        powerValues.append(power)
        
SCRIPTS_BASE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/"
SET_FREQUENCY_BAT="RUN_DS5_changeFreq.bat"
SET_FREQUENCY_PY="changeFrequency.py"
hostname="10.16.20.172"
stop=False

workloadToCommand={}
f = open("parboilToCommand","r")
fout = open("mali_out","w")

for line in f:
    line=line.strip()
    tokens=line.split(" ")
    workload=tokens[0]
    command=""
    for i in range(1,len(tokens)):
        command=command+" "+str(tokens[i])
    command=command.strip()
    workloadToCommand[workload]=command
f.close()

for workload in workloadToCommand.keys():
    commandPostFix=workloadToCommand[workload]
    #t = Thread(target=executeSSHcommand,args=(workload, commandPostFix,))
    stop=False
    powerValues = []
    powerThread = Thread(target=readPowerContinously,args=(powerValues,))
    powerThread.start()
    command="cd /home/root/maliStuff/maliBenchmarks/parboil; "+commandPostFix
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
    ssh.connect(hostname, username="root", password="")
    #print ("sshcommand "+str(sshCommand))
    stdin,stdout,stderr=ssh.exec_command(command=command)
    lines=stdout.readlines() 
    ssh.close()
    stop=True
    powerThread.join()
    kernel_time=0
    passOrFail="Fail"
    for line in lines:
        line=line.strip()
        tokens=line.split(" ")
        if "Kernel"==tokens[0]:
            kernel_time=float(tokens[-1])
        if "Pass"==tokens[0]:
            passOrFail="Pass"
    maxPower=0
    for p in powerValues:
        if float(p) > maxPower:
            maxPower=float(p)
    fout.write(workload+" ")
    fout.write(str(maxPower)+" ")
    fout.write(str(kernel_time)+" ")
    fout.write(str(passOrFail))
    for p in powerValues:
        fout.write(" "+str(p))
    fout.write("\n")
    fout.flush()    
fout.close()