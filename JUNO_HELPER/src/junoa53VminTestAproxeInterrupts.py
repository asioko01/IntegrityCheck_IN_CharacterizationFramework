'''
Created on 14 Jun 2017

@author: zachad01
'''
import subprocess
from sendRebootCommand import sendRebootCommand
from setVoltageThroughSerial import setVoltage
from paramiko import SSHClient, client,SSHException, BadHostKeyException, AuthenticationException
from waitTillSSHworks import waitTillSSHworks
from executeCommandSSH import executeCommand
from socket import error
#from setFrequencyThroughDebugger import setFrequency
from setFrequencyThroughSerial import setFrequency
import time
import os
from getLowestVol import getLowestVol
from disableApolloSSH import disableApollo
import time
from readVoltageThroughSerial import readVoltage
import serial
from SerialHandler  import SerialHandler
#from checkAppStatusThroughSerial import checkAppStatus
serial
class SSHhandler: #class that handles ssh commands to the target machine
    
    COMMAND_FAILED=1
    COMMAND_SUCCESS=0
    
    def __init__(self,targetHostname="xg2-1.in.cs.ucy.ac.cy",targetSSHusername="zhadji01",targetSSHpassword="agoodpasswd"):
        self.targetHostName=targetHostname
        self.targetSSHusername=targetSSHusername
        self.targetSSHpassword=targetSSHpassword
        self.out="" ## stdout and stderr of ssh commands
        self.err=""
        self.commandStatus=self.COMMAND_FAILED
    
    def lastCommandStatus(self):
        return self.commandStatus
    
    def lastCommandOut(self):
        return self.out
    
    def lastCommandErr(self):
        return self.err
    
    def hasCommandFailed(self):
        if(self.commandStatus==self.COMMAND_FAILED):
            return True
        return False
    
    def executeCommand(self,command):
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
            ssh.connect(self.targetHostName, username=self.targetSSHusername, password=self.targetSSHpassword)
            stdin,stdout,stderr=ssh.exec_command(command)
            self.out=stdout.readlines() #just do this to make exec blocking call
            self.err=stderr.readlines()       
            ssh.close()

def checkForCrash(expExTime=10,hz=1):
    startTime=time.time()
    command = ['ping', '-n', '1', '-w','1','10.16.20.178']
    appcommand="/media/oldDisk1/root/benchmarks/a53emVirusGood/appcrashcheck.sh"
    FNULL = open(os.devnull, 'w')
    flag=0
    appflag=0
    crashTime=0
    currTime=time.time()-startTime
    while(flag==0 and currTime<=expExTime and appflag==0):
        flag=subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)
        if(flag == 0):
            try:  
                outp = None
                tries=3
                while outp is None and tries>=0:
                    try:
                        # connect
                        #outp=executeCommand(hostname="10.16.20.178",username="root",password="root",command=appcommand,background=False,timeout=1)
                        #outp=[5]
                        #outp=checkAppStatus(appcommand,"COM17")
                        print("input:"+outp)
                    except:
                        tries-=1
                        time.sleep(1)
                        pass                
            except(SSHException, BadHostKeyException, AuthenticationException,error,EOFError): #SSHException, BadHostKeyException, AuthenticationException,socket.error,EOFError
                print("appcrash!")
                appflag=1
                return time.time()-startTime
            try:
                currTime=time.time()-startTime
                if(float(outp[0])<5 and currTime<expExTime-int(0.2*expExTime)):
                    print("appcrash",outp[0],str(currTime))
                    appflag=1
            except(IndexError):
                print("no response from ssh")
                appflag=1
                return time.time()-startTime
        currTime=time.time()-startTime
        time.sleep(1)
    flag=subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)
    if(flag> 0 or appflag>0):
        print("somthing")
        return currTime
    else:
        print("itsaiight")
        return flag
            
targetHostname="10.16.20.179"
targetSSHusername="root"
targetSSHpassword="root"
workToCommand={}
workExpTime={}
'''
#workToCommand["gaDiDt120droop"]="cd /media/oldDisk1/root/benchmarks/gaDiDtA72singleCore70mV/; taskset -c 4 ./gaDiDtA72singleCore70mV  &> /dev/null & taskset -c 5 ./gaDiDtA72singleCore70mV  &> /dev/null & exit" 
#workToCommand["sleep"]="taskset -c 4 sleep 100000000000000  &> /dev/null & taskset -c 5 sleep 100000000000000 &> /dev/null & exit"
#workToCommand["em500pw69Mhz"]="cd /media/oldDisk1/root/benchmarks/em500pw@69MHz; taskset -c 4  ./em500pw69MHz &>/dev/null & taskset -c 5  ./em500pw69MHz &>/dev/null & exit"

#workToCommand["emCyprus"]="cd /media/oldDisk1/root/benchmarks/emCyprus66MHzGood; taskset -c 4  ./emCyprus66MHzGood &>/dev/null & taskset -c 5  ./emCyprus66MHzGood &>/dev/null & exit"
#workToCommand["didt126mv"]="cd /media/oldDisk1/root/benchmarks/didt126mvDroop; taskset -c 4 ./didt126mv  &> /dev/null & taskset -c 5 ./didt126mv &> /dev/null & exit"
'''
'''
workToCommand["A53DIDT107_11s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"
workToCommand["A53DIDT107_11s1"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"
workToCommand["A53DIDT107_11s2"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"
'''
'''
#workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & taskset -c 4 ./107_5330_3600s  &> /dev/null & taskset -c 5 ./107_5330_3600s &> /dev/null & exit"
#workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & exit"

#AworkToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & taskset -c 4 ./107_5330_3600s &> /dev/null & exit"
#workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null &  exit"
workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/simpleLoop/ ;taskset -c 0 ./simpleLoop3600s  &> /dev/null &  exit"

workToCommand["A53DIDT107_11s3"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"

workToCommand["A53DIDT107_22s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_22s  &> /dev/null & taskset -c 3 ./107_5330_22s &> /dev/null & taskset -c 4 ./107_5330_22s  &> /dev/null & taskset -c 5 ./107_5330_22s &> /dev/null & exit"
#workToCommand["A53DIDT107_22s1"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_22s  &> /dev/null & taskset -c 3 ./107_5330_22s &> /dev/null & taskset -c 4 ./107_5330_22s  &> /dev/null & taskset -c 5 ./107_5330_22s &> /dev/null & exit"
workToCommand["A53DIDT107_44s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_44s  &> /dev/null & taskset -c 3 ./107_5330_44s &> /dev/null & taskset -c 4 ./107_5330_44s  &> /dev/null & taskset -c 5 ./107_5330_44s &> /dev/null & exit"
'''
#workToCommand["A53DIDT_SELFLOOP3CORES5"]="taskset -c 5 /media/oldDisk1/root/benchmarks/a53emVirusGood/107_5330_3600s &> /dev/null & taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & taskset -c 0 ./selfLoop>/dev/null &"
#workToCommand["A53DIDT_SELFLOOP3CORES0"]="taskset -c 0 /media/oldDisk1/root/benchmarks/a53emVirusGood/107_5330_3600s &> /dev/null & taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & taskset -c 5 ./selfLoop>/dev/null &"
#workToCommand["A53DIDT_IDLE3CORES0"]="taskset -c 0 /media/oldDisk1/root/benchmarks/a53emVirusGood/107_5330_3600s &> /dev/null &"
#workToCommand["A53DIDT_IDLE3CORES5"]="taskset -c 5 /media/oldDisk1/root/benchmarks/a53emVirusGood/107_5330_3600s &> /dev/null &"
#workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & taskset -c 4 ./107_5330_3600s  &> /dev/null & taskset -c 5 ./107_5330_3600s &> /dev/null & exit"
#workToCommand["A53DIDT_SELFLOOP2CORES1,2"]="taskset -c 0 /media/oldDisk1/root/benchmarks/a53emVirusGood/107_5330_3600s &> /dev/null & taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & exit"
#workToCommand["A53DIDT107_3600s012"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & taskset -c 4 ./107_5330_3600s  &> /dev/null & exit"
workToCommand["A53DIDT_SELFLOOP1CORES1"]="taskset -c 0 /media/oldDisk1/root/benchmarks/a53emVirusGood/107_5330_3600s &> /dev/null & taskset -c 3 ./selfLoop>/dev/null & exit"


workExpTime["A53DIDT107_11s"]=12
workExpTime["A53DIDT107_22s"]=23
workExpTime["A53DIDT107_44s"]=45

debugCOM="COM8"
serial=SerialHandler("COM9")
interruptSamplePeriod=10
interruptSamples=1
reps=100
nominal=1000
startVoltage=1000
endVoltage=1000
step=5
dbname="junoTestVmin10reps"
frequency=950
timeOut=210
#ps aux | grep ./107
code=waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,10)
while code==1:
    sendRebootCommand(debugCOM)
    code=waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,timeOut)


#executeCommand(hostname="10.16.20.179",username="root",password="root",command=workToCommand["A53DIDT_IDLE3CORES"],background=False,timeout=6)
#a=executeCommand(hostname="10.16.20.179",username="root",password="root",command="./getInterruptsA53.sh",background=False,timeout=6)
sshCommand="./getInterruptsA53Plus.sh"
sshHandler=SSHhandler(targetHostname=targetHostname, targetSSHusername=targetSSHusername,targetSSHpassword=targetSSHpassword)
sshHandler.executeCommand(command="mount /dev/sdb1 /media/oldDisk1/")
print("disk mounted")
sshHandler.executeCommand(command="echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
print("governor set to performance")
setVoltage(2,float(nominal)/1000,debugCOM)
time.sleep(3)
setFrequency(float(frequency), portCOM=debugCOM, multiplier=16, supply=6)
time.sleep(3)
for workload in workToCommand:
    print(str(workload))
    executeCommand(hostname="10.16.20.179",username="root",password="root",command=workToCommand[workload],background=False,timeout=6)
    for rep in range(reps):
        '''
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
        ssh.connect("10.16.20.179", username="root", password="root")
        stdin,stdout,stderr=ssh.exec_command(command=sshCommand)
        
        dummy=stdout.readlines() #just do this to make exec blocking call
        '''
        durat=time.time()
        serial.sendCMD(sshCommand,waitTime=2)
        ser_out=serial.read()
        out=ser_out.split("\r\n")
        #print(out[1:-2])
        time.sleep(interruptSamplePeriod)
            
        '''                   
        ssh.connect("10.16.20.179", username="root", password="root")
        stdin,stdout,stderr=ssh.exec_command(command=sshCommand)
        print(str(time.time()-durat),end=" ")
        dummy1=stdout.readlines() #just do this to make exec blocking call
        '''
        print(str(time.time()-durat),end=" ")
        serial.sendCMD(sshCommand,waitTime=2)
        ser_out=serial.read()
        out1=ser_out.split("\r\n")
        #print(out1[1:-2])
        
        #for d in range(len(dummy1)):
            #print(str(int(dummy1[d])-int(dummy[d])),end=" ")
        for d in range(1,len(out1)-2):
            print(str(int(out1[d])-int(out[d])),end=" ") 
        print() 
    print()
    serial.sendCMD("pkill 3600; pkill self",waitTime=2)
    
        