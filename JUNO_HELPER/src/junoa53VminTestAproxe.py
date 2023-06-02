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
#from checkAppStatusThroughSerial import checkAppStatus

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

#workToCommand["gaDiDt120droop"]="cd /media/oldDisk1/root/benchmarks/gaDiDtA72singleCore70mV/; taskset -c 4 ./gaDiDtA72singleCore70mV  &> /dev/null & taskset -c 5 ./gaDiDtA72singleCore70mV  &> /dev/null & exit" 
#workToCommand["sleep"]="taskset -c 4 sleep 100000000000000  &> /dev/null & taskset -c 5 sleep 100000000000000 &> /dev/null & exit"
#workToCommand["em500pw69Mhz"]="cd /media/oldDisk1/root/benchmarks/em500pw@69MHz; taskset -c 4  ./em500pw69MHz &>/dev/null & taskset -c 5  ./em500pw69MHz &>/dev/null & exit"

#workToCommand["emCyprus"]="cd /media/oldDisk1/root/benchmarks/emCyprus66MHzGood; taskset -c 4  ./emCyprus66MHzGood &>/dev/null & taskset -c 5  ./emCyprus66MHzGood &>/dev/null & exit"
#workToCommand["didt126mv"]="cd /media/oldDisk1/root/benchmarks/didt126mvDroop; taskset -c 4 ./didt126mv  &> /dev/null & taskset -c 5 ./didt126mv &> /dev/null & exit"
'''
workToCommand["A53DIDT107_11s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"
workToCommand["A53DIDT107_11s1"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"
workToCommand["A53DIDT107_11s2"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"
'''
#workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & taskset -c 4 ./107_5330_3600s  &> /dev/null & taskset -c 5 ./107_5330_3600s &> /dev/null & exit"
#workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & exit"

workToCommand["A53DIDT107_3600s4"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null & taskset -c 3 ./107_5330_3600s &> /dev/null & taskset -c 4 ./107_5330_3600s &> /dev/null & exit"
workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_3600s  &> /dev/null &  exit"
#workToCommand["A53DIDT107_3600s0"]="cd /media/oldDisk1/root/benchmarks/simpleLoop/ ;taskset -c 0 ./simpleLoop3600s  &> /dev/null &  exit"

workToCommand["A53DIDT107_11s3"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_11s  &> /dev/null & taskset -c 3 ./107_5330_11s &> /dev/null & taskset -c 4 ./107_5330_11s  &> /dev/null & taskset -c 5 ./107_5330_11s &> /dev/null & exit"

workToCommand["A53DIDT107_22s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_22s  &> /dev/null & taskset -c 3 ./107_5330_22s &> /dev/null & taskset -c 4 ./107_5330_22s  &> /dev/null & taskset -c 5 ./107_5330_22s &> /dev/null & exit"
#workToCommand["A53DIDT107_22s1"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_22s  &> /dev/null & taskset -c 3 ./107_5330_22s &> /dev/null & taskset -c 4 ./107_5330_22s  &> /dev/null & taskset -c 5 ./107_5330_22s &> /dev/null & exit"
workToCommand["A53DIDT107_44s0"]="cd /media/oldDisk1/root/benchmarks/a53emVirusGood/ ;taskset -c 0 ./107_5330_44s  &> /dev/null & taskset -c 3 ./107_5330_44s &> /dev/null & taskset -c 4 ./107_5330_44s  &> /dev/null & taskset -c 5 ./107_5330_44s &> /dev/null & exit"

workExpTime["A53DIDT107_11s"]=12
workExpTime["A53DIDT107_22s"]=23
workExpTime["A53DIDT107_44s"]=45

debugCOM="COM8"
interruptSamplePeriod=10
interruptSamples=100
reps=10
nominal=1000
startVoltage=900
endVoltage=800
step=5
dbname="junoTestVmin10reps"
frequency=950
timeOut=210
#ps aux | grep ./107
code=waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,10)
while code==1:
    sendRebootCommand(debugCOM)
    code=waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,timeOut)

for rep in range(reps):
    for workload in workToCommand.keys():
        sshHandler=SSHhandler(targetHostname=targetHostname, targetSSHusername=targetSSHusername,targetSSHpassword=targetSSHpassword)
        sshHandler.executeCommand(command="mount /dev/sdb1 /media/oldDisk1/")
        print("disk mounted")
        sshHandler.executeCommand(command="echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
        print("governor set to performance")
        setVoltage(2,float(nominal)/1000,debugCOM)
        setFrequency(float(frequency), portCOM=debugCOM, multiplier=16, supply=6)
        voltage=startVoltage
        while voltage>=endVoltage:
            setVoltage(2,float(nominal)/1000,debugCOM) 
            time.sleep(3)
            setVoltage(2,float(voltage)/1000,debugCOM) #vol
            
            time.sleep(3)
            try:
                executeCommand(hostname="10.16.20.179",username="root",password="root",command=workToCommand[workload],background=False,timeout=6)
                time.sleep(3)
                a=executeCommand(hostname="10.16.20.179",username="root",password="root",command="./getInterruptsA53.sh",background=False,timeout=6)
                sshCommand="./getInterruptsA53.sh"
                #sshCommand1="taskset -c 0 ./myInterrupt10ms>/dev/null & taskset -c 3 ./myInterrupt10ms>/dev/null & taskset -c 4 ./myInterrupt10ms>/dev/null & taskset -c 5 ./myInterrupt10ms>/dev/null &"
                sshCommand1="taskset -c 0 ./myInterrupt10ms>/dev/null & taskset -c 3 ./myInterrupt10ms>/dev/null & taskset -c 4 ./myInterrupt10ms>/dev/null & taskset -c 5 ./myInterrupt10ms>/dev/null &"
                ssh = SSHClient()
                ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                ssh.connect("10.16.20.179", username="root", password="root")
                stdin,stdout,stderr=ssh.exec_command(command=sshCommand)
                durat=time.time()
                dummy=stdout.readlines() #just do this to make exec blocking call
                #print(str(dummy))
                ssh = SSHClient()
                ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                ssh.connect("10.16.20.179", username="root", password="root")
                ssh.exec_command(command=sshCommand1)

                #for count in range(interruptSamplePeriod):
                                    
                count=100
                while count>=0:
                    time.sleep(1)
                    vol=readVoltage("COM8","V","2")
                    print(str(vol))
                    count=count-1
                
                ssh.connect("10.16.20.179", username="root", password="root")
                stdin,stdout,stderr=ssh.exec_command(command=sshCommand)
                print()
                print(str(time.time()-durat))
                dummy1=stdout.readlines() #just do this to make exec blocking call
                print()
                for d in range(len(dummy1)):
                    print(str(int(dummy1[d])-int(dummy[d])))    
                sshHandler.executeCommand(command="pkill simpleLoop3600s")
                #exit()
                    #print(str(readVoltage("COM16","OSC","6")))
                    #print(count)
                    #count+=1
                    #time.sleep(1)
                #sshHandler.executeCommand(command=workToCommand[workload])
            except(SSHException, BadHostKeyException, AuthenticationException,error,EOFError):
                setVoltage(2,float(nominal)/1000,debugCOM)
                toPrintstr="SYSCRASH "+workload+" "+str(voltage+step)+" -1"+"\n"
                with open("C:/Users/admin/Desktop/aproxe01/"+dbname+".txt","a") as fwrite:
                    fwrite.write(toPrintstr)
                print(toPrintstr)
                sendRebootCommand(debugCOM)
                print("restarting")
                time.sleep(60)
                print("trying to connect")
                break
            voltage=voltage-step
            continue
            if("11s" not in workload):
                time.sleep(1)
            else:
                time.sleep(1)            
            crash=checkForCrash(expExTime=workExpTime[workload[:-1]])
            crash=0
            if(crash>0):
                #setVoltage(2,float(nominal)/1000,debugCOM)
                toPrintstr="SYSCRASH "+workload+" "+str(voltage)+" "+str(crash)+"\n"
                with open("C:/Users/admin/Desktop/aproxe01/"+dbname+".txt","a") as fwrite:
                    fwrite.write(toPrintstr)
                print(toPrintstr)
                sendRebootCommand(debugCOM)
                print("restarting")
                time.sleep(60)
                print("trying to connect")
                break

                
            voltage=voltage-step
        