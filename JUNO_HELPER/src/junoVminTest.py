'''
Created on 14 Jun 2017

@author: zachad01
'''
from sendRebootCommand import sendRebootCommand
from setVoltageThroughSerial import setVoltage
from paramiko import SSHClient, client
from waitTillSSHworks import waitTillSSHworks
#from setFrequencyThroughDebugger import setFrequency
from setFrequencyThroughSerial import setFrequency
import time
import os
from getLowestVol import getLowestVol
from disableApolloSSH import disableApollo
from checkAppStatusThroughSerial import checkAppStatus

targetHostname="juno_uni.in.cs.ucy.ac.cy"
targetSSHusername="root"
targetSSHpassword="UniServer"
workToCommand={}
#workToCommand["gaDiDt120droop"]="cd /media/oldDisk1/root/benchmarks/gaDiDtA72singleCore70mV/; taskset -c 4 ./gaDiDtA72singleCore70mV  &> /dev/null & taskset -c 5 ./gaDiDtA72singleCore70mV  &> /dev/null & exit" 
#workToCommand["sleep"]="taskset -c 4 sleep 100000000000000  &> /dev/null & taskset -c 5 sleep 100000000000000 &> /dev/null & exit"
#workToCommand["em500pw69Mhz"]="cd /media/oldDisk1/root/benchmarks/em500pw@69MHz; taskset -c 4  ./em500pw69MHz &>/dev/null & taskset -c 5  ./em500pw69MHz &>/dev/null & exit"

#workToCommand["emCyprus"]="cd /media/oldDisk1/root/benchmarks/emCyprus66MHzGood; taskset -c 4  ./emCyprus66MHzGood &>/dev/null & taskset -c 5  ./emCyprus66MHzGood &>/dev/null & exit"
workToCommand["didt126mv"]="cd /media/oldDisk1/root/benchmarks/didt126mvDroop; taskset -c 4 ./didt126mv  &> /dev/null & taskset -c 5 ./didt126mv &> /dev/null & exit"


debugCOM="COM7"
reps=9
nominal=900
SCRIPTS_BASE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/"
#SET_FREQUENCY_BAT="RUN_DS5_changeFreq.bat"
#SET_FREQUENCY_PY="changeFrequency.py"
frequency=1200
timeOut=210

code=waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,10)
while code==1:
    sendRebootCommand(debugCOM)
    code=waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,timeOut)

for rep in range(reps):
    for workload in workToCommand.keys():
        disableApollo(targetHostname,targetSSHusername,targetSSHpassword)
        setVoltage(1,float(nominal)/1000,debugCOM)
        #setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)
        setFrequency(frequency, portCOM=debugCOM, multiplier=20, supply=7)
        sshCommand=workToCommand[str(workload)]
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
        ssh.connect(targetHostname, username=targetSSHusername, password=targetSSHpassword)
        stdin,stdout,stderr=ssh.exec_command(command=sshCommand)
        dummy=stdout.readlines() #just do this to make exec blocking call
        ssh.close()
        time.sleep(3) # wait workload to start
        volDroop=nominal-getLowestVol()
        startVoltage=0.89
        endVoltage=0
        step=0.01
        voltage=startVoltage
        while voltage>=endVoltage:
            setVoltage(1,voltage,debugCOM)
            time.sleep(5)
            try:
                ssh = SSHClient()
                ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                ssh.connect(targetHostname, username=targetSSHusername, password=targetSSHpassword)
                ssh.close()
            except(Exception):
                vminToPrint=round(voltage, 2)
                print("OUTPUT "+str(workload)+" "+str(vminToPrint)+" "+str(volDroop))              
                setVoltage(1,0.9,debugCOM)  
             
                code=1
                while code==1:
                    sendRebootCommand(debugCOM)
                    code=waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,timeOut)
                setFrequency(frequency, portCOM=debugCOM, multiplier=20, supply=7)
                break                         
            voltage=voltage-step
        