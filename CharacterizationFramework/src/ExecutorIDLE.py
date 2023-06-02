'''
Created on Mar 2, 2017

@author: zhadji01
'''
from Experiment import Experiment
import traceback
from paramiko import SSHClient, client
import paramiko
import socket
from threading import Timer
from threading import Thread
import time
import os
import subprocess
import sys
from json_helper import *
import math
from random import Random
from SerialHandler  import SerialHandler
import serial
import Utilites
import datetime
from Utilites import getTimestampInSecs, getNextOf, getBinaryStringOfInt
from MongoDBhandler import MongoDBhandler
from InputGenerator import platform

#JUNO RELATED STUFF
JUNO_DEBUG_PORT="COM8" #TODO add as json input.. fix magic variable
measureInterrupts=False
interruptFileName="idle3coreInterrupts0reschedPlus2"
#CURRENTCORERUNNING=0
JUNO_BOOST_INTERRUPTS=False
class NextVoltageGenerator: #helper class that returns the next voltage.. will help in comparing between random and incremental steps
    METHOD_INCREMENTAL=0
    METHOD_RANDOM=1
    NO_MORE_VOLTAGES=0
    def __init__(self,highVoltage,lowVoltage,voltageStep,method):
        self.highVoltage=highVoltage
        self.lowVoltage=lowVoltage
        self.voltageStep=voltageStep
        self.method=method
        self.voltageList=[]
        for voltage in range(highVoltage,lowVoltage-abs(voltageStep),-abs(voltageStep)):
            self.voltageList.append(voltage)
        if len(self.voltageList)==0:
            self.currentVol=self.NO_MORE_VOLTAGES
        else:
            self.currentVol=self.highVoltage
        self.rand=Random()
        self.rand.seed(0)
        if(self.method==self.METHOD_RANDOM):
            try:
                vol=self.rand.choice(self.voltageList)
                self.voltageList.remove(vol)
                self.currentVol=vol
            except(IndexError):
                self.currentVol=self.NO_MORE_VOLTAGES
        
    def cal_next(self): ##calculate next voltage ## no need to call this to calculate the first voltage
        if(self.method==self.METHOD_INCREMENTAL):
            self.currentVol=self.currentVol-abs(self.voltageStep)
            if self.currentVol<self.lowVoltage:
                self.currentVol=self.NO_MORE_VOLTAGES
        else:
            try:
                vol=self.rand.choice(self.voltageList)
                self.voltageList.remove(vol)
                self.currentVol=vol
            except(IndexError):
                self.currentVol=self.NO_MORE_VOLTAGES
            
    def get_vol(self): #get current voltage
        return self.currentVol

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
        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
            ssh.connect(self.targetHostName, username=self.targetSSHusername, password=self.targetSSHpassword)
            stdin,stdout,stderr=ssh.exec_command(command)
            self.out=stdout.readlines() #just do this to make exec blocking call
            self.err=stderr.readlines()       
            ssh.close()
        except(paramiko.SSHException, paramiko.BadHostKeyException, paramiko.AuthenticationException, socket.error,EOFError):
            self.commandStatus = self.COMMAND_FAILED;
            return
        self.commandStatus= self.COMMAND_SUCCESS

class WorkloadHandler:
    
    SUCCESS=0
    FAIL=1
    #TRUE=1
    #FALSE=0
    CHK_ALIVE_FREQ=10
    WORKLOAD_SCRIPT_ABORTED=2
    SYSTEM_CRASHED=1
    WORKLOAD_SCRIPT_FINISHED_SUCCESFULLY=0
    MAX_CHK_ALIVE_TRIES=1 ##BE CAREFULL IF YOU SET THIS HIHGER THAN 1 THEN THE SYSTEM CRASH TIMESTAMP will be off.. but you will be more sure that a crash occured 
    UNRESPONSIVE_TIMEOUT=5
    CPU_POWER_FILE="/tmp/chf_cpu_power"
    UNCORE_POWER_FILE="/tmp/chf_uncore_power"
    
    MEASURE_FILES={
    'pmd_power':'/tmp/pmd_power',
    'uncore_power':'/tmp/uncore_power',
    'dram1_power':'/tmp/dram1_power',
    'dram2_power':'/tmp/dram2_power',
    'pmd_temp':'/tmp/pmd_temp',
    'uncore_temp':'/tmp/uncore_temp',
    'dram1_temp':'/tmp/dram1_temp',
    'dram2_temp':'/tmp/dram2_temp',
    'dram3_temp':'/tmp/dram3_temp',
    'dram4_temp':'/tmp/dram4_temp',
    'dram5_temp':'/tmp/dram5_temp',
    'dram6_temp':'/tmp/dram6_temp',
    'dram7_temp':'/tmp/dram7_temp',
    'dram8_temp':'/tmp/dram8_temp'
    }
    
    '''
    a = {
    'a': 'value',
    'another': 'value',
    }
    FILES_ARRAY["pmd_power"]=/tmp/pmd_power
    FILES_ARRAY["uncore_power"]=/tmp/uncore_power
    FILES_ARRAY["dram1_power"]=/tmp/dram1_power
    FILES_ARRAY["dram2_power"]=/tmp/dram2_power
    FILES_ARRAY["pmd_temp"]=/tmp/pmd_temp
    FILES_ARRAY["uncore_temp"]=/tmp/uncore_temp
    FILES_ARRAY["dram1_temp"]=/tmp/dram1_temp
    FILES_ARRAY["dram2_temp"]=/tmp/dram2_temp
    FILES_ARRAY["dram3_temp"]=/tmp/dram3_temp
    FILES_ARRAY["dram4_temp"]=/tmp/dram4_temp
    FILES_ARRAY["dram5_temp"]=/tmp/dram5_temp
    FILES_ARRAY["dram6_temp"]=/tmp/dram6_temp
    FILES_ARRAY["dram7_temp"]=/tmp/dram7_temp
    FILES_ARRAY["dram8_temp"]=/tmp/dram8_temp
    '''   
        
    def __init__(self,sshHandler,serial,run,helperWorkloadScript,workloadStatusOutput,measurePowerScript=None):
        self.run=run  
        self.mode=None  
        self.sshHandler=sshHandler
        self.serial=serial
        #self.workloadSDCs=[]
        #self.workloadCrashes=[]
        self.systemCrash=False
        self.abnormal_workload_status=False
        self.voltageOfObservation=0
        self.helperWorkloadScript=helperWorkloadScript
        self.workloadStatusOutput=workloadStatusOutput
        self.measurePowerScript=measurePowerScript
        self.statusOutputLines=""
        
        self.pmd_errors=[]  #array of pmd_error object
        self.pmd_l2_errors=[]# array pmd_l2_errors object
        self.l3_errors=[] #array of l3_error object
        self.mcu_errors=[]#array of mcu_error objects
        self.pcie_errors=[]# array of pci_error objects
        self.sata_errors=[]#array of sata_error objects
        self.pmd_vrd_hot=None #int
        self.dimm_vrd_hot=None #int
        self.soc_vrd_hot=None #int
        #self.dimm_hot=None #int
        self.soc_overtemp=None #int
        ##toKillName
        tmp=str(self.helperWorkloadScript.split("/")[-1])
        self.toKillWorkScriptName=tmp#process to pkill up to 15 chars
        if len(tmp)>15:
            self.toKillWorkScriptName=tmp[0:14]
        
        self.start_timestamp=0
        for workload in self.run.workloads:
            workload.executionTime=None #zero the execuction time before a new run
    
    def setVoltageOfObservation(self,voltage):
        self.voltageOfObservation=voltage
    
    def getVoltageOfObservation(self):
        return self.voltageOfObservation
    
    def startWorkload(self):
        #work_dir cmd_line (please without stdout stder redirections) toKillName conventionName cores originalOutputPath runOutputPath type
        command=self.helperWorkloadScript+" "+str(self.voltageOfObservation)+" "
        for workload in self.run.workloads:
            command=command+str(workload.toHelperScript())+ " "
        command=command+" &"
        print(str(command))
        self.start_timestamp= int(round(time.time()))
        self.serial.sendCMD(command,waitTime=WorkloadHandler.UNRESPONSIVE_TIMEOUT)
        if self.measurePowerScript is not None: 
            #self.serial.sendCMD(self.measurePowerScript+" "+ self.CPU_POWER_FILE+" 0 1 5 "+ self.UNCORE_POWER_FILE + " & ")
            self.serial.sendCMD(self.measurePowerScript+" 0 2  &")
        #exit(1)
        #command=str(self.helperSciprt)+" "+str("\"")+str(self.run.command_line)+str("\"")+" "+str(self.run.active_cores)+" "+str(self.run.idle_cores)+" "+str(self.run.frequency)+" "+str(self.run.frequency_idle)+" "+str(self.run.smp_affinity)+" "+str(self.run.work_type)+" "+str(self.mode) +" &> /home/zhadji01/chf_helper_out & "
        #print(str("Command to execute "+command))
        #self.sshHandler.executeCommand(command)
        #if(self.sshHandler.hasCommandFailed()):
        #    return WorkloadHandler.FAIL
        #return WorkloadHandler.SUCCESS
    '''
    def calculateCPUPowerSSH(self):
        max_tries=3
        tries=0
        command="cat "+self.CPU_POWER_FILE+" | tail -n 1"
        self.sshHandler.executeCommand(command)
        while self.sshHandler.lastCommandStatus()==SSHhandler.COMMAND_FAILED and tries<=max_tries:
            self.sshHandler.executeCommand(command)
            tries=tries+1
        lines=self.sshHandler.lastCommandOut()
        if lines is None or len(lines)==0 or lines=="":
            return None
        line=lines[0]
        tokens=line.split(" ")
        power_values=[]
        for token in tokens:
            power_values.append(float(token))
        return power_values
        
    def calculateCPUPowerSerial(self):
        command="echo -n \"POWER_VALUES_CHF \";cat " + self.CPU_POWER_FILE+ " | tail -n 1 | tr ' ' '_'"
        self.serial.sendCMD(command,waitTime=2)
        ser_out=self.serial.read()
        #toReturn=None
        values=None
        for line in ser_out.split("\n"):
            if ("POWER_VALUES_CHF" in line):
                tokens=line.split(" ")
                values=getNextOf(tokens, "POWER_VALUES_CHF")
                break
        if(values is None):
            return None
        values_array=[]
        tokens=values.split("_")
        for token in tokens:
            values_array.append(float(token))
        return values_array
    '''
    
    def calculateMeasurementValues(self,measurement):
        max_tries=3
        tries=0
        command="cat "+self.MEASURE_FILES[measurement]+" "
        self.sshHandler.executeCommand(command)
        while self.sshHandler.lastCommandStatus()==SSHhandler.COMMAND_FAILED and tries<=max_tries:
            self.sshHandler.executeCommand(command)
            tries=tries+1
        lines=self.sshHandler.lastCommandOut()
        if lines is None or len(lines)==0 or lines=="":
            return None
        values=[]
        for line in lines:
            try:
                tokens=line.split(" ")
                if len(tokens)!=1:
                    break
                values.append(float(line))
            except Exception as e: 
                print(e)
                pass
        return values
    
    def calculateMeasurementSSH(self,measurement):
        max_tries=3
        tries=0
        command="cat "+self.MEASURE_FILES[measurement]+" | tail -n 1"
        self.sshHandler.executeCommand(command)
        while self.sshHandler.lastCommandStatus()==SSHhandler.COMMAND_FAILED and tries<=max_tries:
            self.sshHandler.executeCommand(command)
            tries=tries+1
        lines=self.sshHandler.lastCommandOut()
        if lines is None or len(lines)==0 or lines=="":
            return None
        line=lines[0]
        tokens=line.split(" ")
        power_values=[]
        for token in tokens:
            try:
                power_values.append(float(token))
            except:
                pass
        return power_values
        
    def calculateMeasurementSerial(self,measurement):
        command="echo -n \"POWER_VALUES_CHF \";cat " + self.MEASURE_FILES[measurement]+ " | tail -n 1 | tr ' ' '_'"
        self.serial.sendCMD(command,waitTime=2)
        ser_out=self.serial.read()
        #toReturn=None
        values=None
        for line in ser_out.split("\n"):
            if ("POWER_VALUES_CHF" in line):
                tokens=line.split(" ")
                values=getNextOf(tokens, "POWER_VALUES_CHF")
                break
        if(values is None):
            return None
        values_array=[]
        tokens=values.split("_")
        for token in tokens:
            try:
                values_array.append(float(token))
            except:
                pass
        return values_array
        
    def calculateErrorInfoAfterReboot(self,startTime,endTime,script):
        #self.serial.sendCMD("cat "+ self.workloadStatusOutput,waitTime=2)    
        #ser_out=self.serial.read()
        #lines=ser_out.split("\n")
        error_lines=[]
        
        self.sshHandler.executeCommand(command="year=`date | awk '{print $NF}'`; sudo "+ str(script) +" $year "+ str(startTime) +" "+str(endTime)) ##TODO check if this works correctly
        while self.sshHandler.lastCommandStatus()==SSHhandler.COMMAND_FAILED:
            self.sshHandler.executeCommand(command="year=`date | awk '{print $NF}'`; sudo "+ str(script) +" $year "+ str(startTime) +" "+str(endTime))
        
        lines=self.sshHandler.lastCommandOut()
        errString=""
        for line in lines:
            errString=errString+" "+line
            error_lines.append(line)        
            
            
        #if errString=="": 
        #    errString=None 
        if errString=="\r": 
            errString=""
            error_lines=[]
        
        self.__calculateHEIerrors__(error_lines)
           
        return errString
    
    def calculateErrorInfo(self):
        startRecording=0
        errString=""
        lines=[]
        for line in self.statusOutputLines:
            if "ERROR_OUTPUT" in line:
                if(startRecording==0):
                    startRecording=1
                else:
                    break
            elif(startRecording==1):
                errString=errString+line
                lines.append(line)
                
        #if errString=="":
        #    errString=None
        if errString=="\r": 
            errString=""
            lines=[]
            
        self.__calculateHEIerrors__(lines)
        
        return errString
    
    def __calculateHEIerrors__(self,lines):
       
            for line in lines:
                try:
                    tokens=line.split(" ")
                    if tokens [1] == '': #because if day digits are less than 2 e.g. Aug 1 2 3 etc.. then there is extra empty token for formating
                        date_str=tokens[0]+" "+tokens[2]+" "+tokens[3]
                    else: 
                        date_str=tokens[0]+" "+tokens[1]+" "+tokens[2]
                    
                    timestamp=getTimestampInSecs(date_str)
                    secs_after=timestamp-self.start_timestamp
                    
                    if "HEI_alert" in line and "soc_hot" in line:
                        toks=line.replace("="," ").replace("<","").split(" ")
                        self.soc_overtemp=int(getNextOf(toks,"reg_0x10"),0)                        
                    elif "HEI_alert" in line and "soc_vrhot" in line:
                        toks=line.replace("="," ").replace("<","").split(" ")
                        self.soc_vrd_hot=int(getNextOf(toks,"reg_0x11"),0)
                    elif "HEI_alert" in line and "pmd_vrhot" in line:
                        toks=line.replace("="," ").replace("<","").split(" ")
                        self.pmd_vrd_hot=int(getNextOf(toks,"reg_0x13"),0)
                    elif "HEI_alert" in line and "dimm_vrhot" in line:
                        toks=line.replace("="," ").replace("<","").split(" ")
                        self.dimm_vrd_hot=int(getNextOf(toks,"reg_0x12"),0)
                    elif   "HEI_alert" in line and "pmd_error" in line:
                        allErrors = line.replace(">","").split("<")
                        for index  in range(1,len(allErrors)):
                            error=allErrors[index]
                            error=error.replace(":","")
                            toks=error.replace("="," ").split(" ")
                            pmdId=int(getNextOf(toks,"pmd"))
                            error_type=int(getNextOf(toks,"reg_0x81"),0)
                            if(error_type!=0): #L1 error
                                bit_string=getBinaryStringOfInt(error_type) 
                                reverse_bit_string=bit_string[::-1] #get it and reverse it                              
                                for counter in range(0,6):
                                    bit=int(reverse_bit_string[counter])
                                    if bit==1:
                                        newPmdError= pmd_error()
                                        self.pmd_errors.append(newPmdError)
                                        newPmdError.time=secs_after
                                        newPmdError.cpu=pmdId*int(Executor.CORES_PER_PMD)+int(counter) // 8
                                        err_type_code=counter % 8
                                        if err_type_code==0:
                                            newPmdError.type="L1 ICF CErr"
                                        elif err_type_code==1:
                                            newPmdError.type="L1 ICF MultCErr"
                                        elif err_type_code==2:
                                            newPmdError.type="L1 LSU CErr"
                                        elif err_type_code==3:
                                            newPmdError.type="L1 LSU MultCErr"
                                        elif err_type_code==4:
                                            newPmdError.type="MMU CErr"
                                        elif err_type_code==5:
                                            newPmdError.type="MMU MultCerr"
                                        else:
                                            newPmdError.type="Unknown"
                                        #elif err_type_code==6:
                            
                            error_type=int(getNextOf(toks,"reg_0x82"),0)
                            if(error_type!=0): #L2 error
                                bit_string=getBinaryStringOfInt(error_type)
                                reverse_bit_string=bit_string[::-1] #get it and reverse it                          
                                newPMDl2Error=pmd_l2_error()
                                newPMDl2Error.time=secs_after       
                                                      
                                for counter in range(0,4):
                                    bit=int(reverse_bit_string[counter])
                                    if bit==1:                                     
                                        err_type_code=counter % 8
                                        if err_type_code==0:
                                            newPMDl2Error.severity="CErr"
                                        elif err_type_code==1:
                                            newPMDl2Error.severity="UcErr"
                                        elif err_type_code==2:
                                            newPMDl2Error.severity="MultCErr"
                                        elif err_type_code==3:
                                            newPMDl2Error.severity="MultUcErr"
                                        #else:
                                        #    newPMDl2Error.type="Unknown"
                                        
                                err_type=int(reverse_bit_string[8:10][::-1],2)
                                if err_type == 0:
                                    newPMDl2Error.type="outboundSDBparity"
                                elif err_type == 1:
                                    newPMDl2Error.type="inboundSDBparity" 
                                elif err_type == 2:
                                    newPMDl2Error.type="tag_ecc" 
                                elif err_type == 3:
                                    newPMDl2Error.type="data_ecc"        
                                
                                err_action=int(reverse_bit_string[10:13][::-1],2)
                                if err_type == 0:
                                    newPMDl2Error.type=str(err_action)                             
                                elif err_type == 1:
                                    if err_action==0:
                                        newPMDl2Error.ErrAction="non_cache_fill"
                                    elif err_action==5:
                                        newPMDl2Error.ErrAction="snoop_forward"
                                    elif err_action==6:
                                        newPMDl2Error.ErrAction="cache_fill" 
                                elif err_type == 2:
                                    newPMDl2Error.type=str(err_action) 
                                elif err_type == 3:
                                    if err_action==0:
                                        newPMDl2Error.ErrAction="other"
                                    elif err_action==1:
                                        newPMDl2Error.ErrAction="read_hit"
                                    elif err_action==2:
                                        newPMDl2Error.ErrAction="write_hit"
                                    elif err_action==3:
                                        newPMDl2Error.ErrAction="write_upgrades"
                                    elif err_action==4:
                                        newPMDl2Error.ErrAction="cache_flush"
                                    elif err_action==5:
                                        newPMDl2Error.ErrAction="data_forward"
                                    elif err_action==6:
                                        newPMDl2Error.ErrAction="fill_writeback"
                                    elif err_action==7:
                                        newPMDl2Error.ErrAction="tag_err_delay"
                                
                                err_grp=int(reverse_bit_string[13:16][::-1],2)
                                newPMDl2Error.ErrGrp=err_grp    
                                
                                add_err_info=int(getNextOf(toks,"reg_0x83"),0)
                                bit_string=getBinaryStringOfInt(add_err_info)
                                reverse_bit_string=bit_string[::-1]
                                newPMDl2Error.cpu=pmdId*int(Executor.CORES_PER_PMD)+int(reverse_bit_string[1])
                                errWay=int(reverse_bit_string[2:8][::-1],2)
                                errSyn=int(reverse_bit_string[8:16][::-1],2)
                                newPMDl2Error.ErrWay=errWay
                                newPMDl2Error.ErrSyn=errSyn
                                                                
                                rtos_info=int(getNextOf(toks, "reg_0x84"),0)
                                bit_string=getBinaryStringOfInt(rtos_info)
                                reverse_bit_string=bit_string[::-1]
                                if int(reverse_bit_string[0])==1:
                                    newPMDl2Error.rtos="timeout"
                                if int(reverse_bit_string[1])==1:
                                    newPMDl2Error.rtos="request_stuck"
                                
                                self.pmd_l2_errors.append(newPMDl2Error)
                                
                    elif   "HEI_alert" in line and "mem_error" in line:
                        allErrors = line.replace(">","").split("<")
                        for index  in range(1,len(allErrors)):
                            error=allErrors[index]
                            error=error.replace(":","")
                            toks=error.replace("="," ").split(" ")
                            mcuId=int(getNextOf(toks,"mcu"))
                            newMCUerror = mcu_error()
                            self.mcu_errors.append(newMCUerror)
                            newMCUerror.time=secs_after
                            newMCUerror.dimid=mcuId
                            bit_string=getBinaryStringOfInt(int(getNextOf(toks,"reg_0x91"),0))
                            reverse_bit_string=bit_string[::-1]
                            if int(reverse_bit_string[0])==1:
                                newMCUerror.type="CErr"
                            elif int(reverse_bit_string[1])==1:
                                newMCUerror.type="DemandUcErr"
                            elif int(reverse_bit_string[2])==1:
                                newMCUerror.type="BackUcErr"
                            elif int(reverse_bit_string[3])==1:
                                newMCUerror.type="MultUcErr"
                            newMCUerror.rank_error=int(reverse_bit_string[8:12][::-1],2)
                            newMCUerror.bank_error=int(reverse_bit_string[12:16][::-1],2)
                            newMCUerror.row_error=int(getNextOf(toks,"reg_0x92"),0)
                            newMCUerror.column_error=int(getNextOf(toks,"reg_0x93"),0)
                    
                    elif "HEI_alert" in line and "l3c_error" in line:
                        allErrors = line.replace(">","").split("<")
                        for index  in range(1,len(allErrors)):
                            error=allErrors[index]
                            toks=error.replace("="," ").split(" ")
                            newL3error=l3_error()                      
                            self.l3_errors.append(newL3error)
                            newL3error.time=secs_after
                            reg_75=int(getNextOf(toks,"reg_0x75"),0)
                            bit_string=getBinaryStringOfInt(reg_75)
                            reverse_bit_string=bit_string[::-1]
                            if(int(reverse_bit_string[0])==0):
                                newL3error.data_tag="data"
                            else:
                                newL3error.data_tag="tag"
                            
                            if int(reverse_bit_string[1])==1:
                                newL3error.type="CErr"
                            elif int(reverse_bit_string[2])==1:
                                newL3error.type="UcErr"
                            elif int(reverse_bit_string[3])==1:
                                newL3error.type="MultCErr"
                            elif int(reverse_bit_string[4])==1:
                                newL3error.type="MultUcErr"
                            elif int(reverse_bit_string[5])==1:
                                newL3error.type="UnEvict"
                            elif int(reverse_bit_string[6])==1:
                                newL3error.type="Retry"
                            elif int(reverse_bit_string[7])==1:
                                newL3error.type="MultiHit"
                            
                                    
                            reg_76=int(getNextOf(toks,"reg_0x76"),0)
                            bit_string=getBinaryStringOfInt(reg_76)
                            reverse_bit_string=bit_string[::-1]
                            newL3error.ErrGrp=int(reverse_bit_string[0:4][::-1],2)
                            newL3error.ErrWay=int(reverse_bit_string[4:10][::-1],2)
                            newL3error.ErrBank=int(reverse_bit_string[10:16][::-1],2)
                            reg_77=int(getNextOf(toks,"reg_0x77"),0)
                            bit_string=getBinaryStringOfInt(reg_77)
                            reverse_bit_string=bit_string[::-1]
                            newL3error.ErrSet=int(reverse_bit_string[0:7][::-1],2)
                            reg_78=int(getNextOf(toks,"reg_0x78"),0)
                            bit_string=getBinaryStringOfInt(reg_78)
                            reverse_bit_string=bit_string[::-1]
                            newL3error.ErrSyn=int(reverse_bit_string[0:9][::-1],2)
                    
                    elif "HEI_alert" in line and "pci_error" in line:
                        allErrors = line.replace(">","").split("<")
                        for index  in range(1,len(allErrors)):
                            error=allErrors[index]
                            error=error.replace(":","")
                            toks=error.replace("="," ").split(" ")                        
                            newPCIerror=pcie_error()
                            self.pcie_errors.append(newPCIerror)
                            newPCIerror.time=secs_after
                            newPCIerror.id=int(getNextOf(toks,"pci"))
                            register_str="0x%x" % int(192+newPCIerror.id)
                            bit_string=getBinaryStringOfInt(int(getNextOf(toks, "reg_"+register_str),0))
                            reverse_bit_string=bit_string[::-1]
                            newPCIerror.function=int(reverse_bit_string[0:3][::-1],2)
                            newPCIerror.device=int(reverse_bit_string[3:8][::-1],2)
                            err_code=int(reverse_bit_string[8:16][::-1],2)
                            if err_code==0:
                                newPCIerror.type="Data Link Layer error"
                            elif err_code==1:
                                newPCIerror.type="Surprise link down"
                            elif err_code==2:
                                newPCIerror.type="Unexpected completion"
                            elif err_code==3:
                                newPCIerror.type="Unsupported inbound request"
                            elif err_code==4:
                                newPCIerror.type="Poisoned TLP"
                            elif err_code==5:
                                newPCIerror.type="Flow Control Protocol Error"
                            elif err_code==6:
                                newPCIerror.type="Completion Timeout"
                            elif err_code==7:
                                newPCIerror.type="Completer Abort"
                            elif err_code==8:
                                newPCIerror.type="Receive Buffer Overflow"
                            elif err_code==9:
                                newPCIerror.type="ACS violation"
                            elif err_code==10:
                                newPCIerror.type="Malformed TLP"
                            elif err_code==11:
                                newPCIerror.type="ERR_FATAL message from downstream"
                            elif err_code==12:
                                newPCIerror.type="Unexpected completion"
                            
                    elif "HEI_alert" in line and "sata_error" in line:
                        allErrors = line.replace(">","").split("<")
                        for index  in range(1,len(allErrors)):
                            error=allErrors[index]
                            error=error.replace(":","")
                            toks=error.replace("="," ").split(" ")                        
                            controller=int(getNextOf(toks,"sata"))
                            register_str="0x%x" % int(208+controller)
                            bit_string=getBinaryStringOfInt(int(getNextOf(toks, "reg_"+register_str),0))
                            reverse_bit_string=bit_string[::-1]
                            port0=int(reverse_bit_string[0:8][::-1],2)
                            port1=int(reverse_bit_string[8:16][::-1],2)
                            #if port0==0:
                            #    newSataError.port=0
                            #    newSataError.type="not connected"
                            #if port0==1:
                            #    newSataError.port=0
                            #    newSataError.type="connected_normal"
                            if port0==2:
                                newSataError=sata_error()
                                self.sata_errors.append(newSataError)
                                newSataError.time=secs_after
                                newSataError.controller=int(getNextOf(toks,"sata"))
                                newSataError.port=0
                                newSataError.type="connected_error"
                            #if port1==0:
                            #    newSataError.port=1
                            #    newSataError.type="not connected"
                            #if port1==1:
                            #    newSataError.port=1
                            #    newSataError.type="connected_normal"
                            if port1==2:
                                newSataError=sata_error()
                                self.sata_errors.append(newSataError)
                                newSataError.time=secs_after
                                newSataError.controller=int(getNextOf(toks,"sata"))
                                newSataError.port=1
                                newSataError.type="connected_error"
                except (Exception,ValueError,IndexError) as e:
                    traceback.print_exc()
                    print("EXCEPTION while calculating the hei errors")
                    continue

    def calculateWorkloadStatus(self):
        work_index=0
        
        for line in self.statusOutputLines:
            if "WORKLOAD_SCRIPT" in line:
                tokens=line.split(" ")
                try:
                    self.run.workloads[work_index].exitCode=int(tokens[1])
                    self.run.workloads[work_index].crash=bool(int(tokens[2]))
                    if str(tokens[3])=="null":
                        self.run.workloads[work_index].sdc=None
                    else:
                        self.run.workloads[work_index].sdc=bool(int(tokens[3]))
                except:
                    self.run.workloads[work_index].exitCode=None
                    self.run.workloads[work_index].crash=None
                    self.run.workloads[work_index].sdc=True
                try:
                    self.run.workloads[work_index].executionTime=float(tokens[4])
                except ValueError:
                    print("VALUE_ERROR in calculating execution time")
                    self.run.workloads[work_index].executionTime=None
                if len(tokens)>5:
                    try:
                        qos_value=float(tokens[5])
                        self.run.workloads[work_index].qos=quality_metric()
                        self.run.workloads[work_index].qos.value=qos_value
                    except ValueError:
                        print("VALUE_ERROR in calculating qos ")
                        self.run.workloads[work_index].qos=None                               
                work_index=work_index+1 
     
            
                
     
    ##JUNO DROOP RELATED STUFF
    MEASURE_DROOP=False#TODO fix magic variables
    MAX_DROOP=0
    MEASURE_EM=False
    FREQ_AMP_PAIRS=[]
    
    def __measureFFTlowestVol__(self):
        os.system("C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python36-32\\python.exe " +  "C:/Users/admin/Desktop/liClipseWorkspace/JUNO_HELPER/src/measureFFTLowestVol.py" +  " -f " + "\"" + "C:/cygwin64/home/admin/specCharC0C1activeC0C1/"+ self.run.workloads[0].toKillName + "\"" + " -e 320 -o 1")
        #os.system("C:\Python34\python.exe "+ "\"" +  "C:/Users/zachad01/My Documents/LiClipse Workspace/TalkToAnalyzer/src/getAmplitudesAtRange.py" + "\"" + " -f " + "\"" + "C:/cygwin64/home/zachad01/specChar/"+ self.run.workloads[0].toKillName + "\"")
    def __getEM__(self):
        from Utility import getAmpRms
        freq,amp=getAmpRms(72, 75, 1, True, 1, 1, 1)
        WorkloadHandler.FREQ_AMP_PAIRS.append((freq,amp))
        
    def __measureVoltageVsurge__(self):
        import fileinput
        nomVoltage=self.voltageOfObservation
        LAST_MEAS_FILE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/tmp"
        #print("Taking the measurement");
        #os.system("cd \"C:/Users/zachad01/My Documents/LiClipse Workspace/PAUL_SCRIPTS\" && debugger.exe --stop_on_connect=false --cdb-entry \"ARM Development Boards::Juno ARM Development Platform (r2)::Bare Metal Debug::Bare Metal Debug::Debug Cortex-M3::DSTREAM\" --cdb-entry-param Connection=USB:000059 --script \"C:\/Users/zachad01/My Documents/LiClipse Workspace/PAUL_SCRIPTS/zac_getLowestVoltage.py\" && exit"); #for taking the measurement 
        os.system("cd \"C:/Users/admin\Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS\" && debugger_restart.bat && exit")
        os.system("cd \"C:/Users/admin\Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS\" && RUN_DS5_lowestVol.bat && exit")
        droop=nomVoltage-nomVoltage
        if(os.path.exists(LAST_MEAS_FILE)==False):
            return droop
        values=[]
        for line in fileinput.input(LAST_MEAS_FILE):
            values.append(int(line))
            #break
        fileinput.close()
        droop=nomVoltage-min(values)
        if droop >  WorkloadHandler.MAX_DROOP:
            WorkloadHandler.MAX_DROOP=droop
        #return droop
    ##END OF DROOP RELATED STUFF
    
    MIN_WORKLOAD_OUTPUT_COLUMNS=5
    def waitWorkloadToFinish(self):
        secs=0
        chk_alive_tries=0
        counter=0
        if  WorkloadHandler.MEASURE_DROOP==True and self.run.platform=="juno":
            WorkloadHandler.MAX_DROOP=0
        if WorkloadHandler.MEASURE_EM:
            WorkloadHandler.FREQ_AMP_PAIRS=[]
            
        start_time = int(time.time())
        while True :
            if  WorkloadHandler.MEASURE_DROOP==True and self.run.platform=="juno":
                self.__measureVoltageVsurge__()
            
            if self.run.customChar==True and secs>=10:
                self.__measureFFTlowestVol__()
                self.serial.sendCMD("pkill -9 "+self.run.workloads[0].toKillName,waitTime=WorkloadHandler.UNRESPONSIVE_TIMEOUT)
                time.sleep(6)
            
            if WorkloadHandler.MEASURE_EM:
                self.__getEM__()
            
            time.sleep(WorkloadHandler.CHK_ALIVE_FREQ)   ##TODO HOW OFTEN TO CHECK ... think about the value of this variable                   
            #check if chf_helper_workload process is running
            #self.serial.isSerialResponsive(timeout=)
            code=self.serial.sendCMD("pkill -0 "+self.toKillWorkScriptName+" &>/dev/null; echo \"toKill $?\"", waitTime=WorkloadHandler.UNRESPONSIVE_TIMEOUT)#a bit conservative
            ser_out=self.serial.read()
            chk_alive_tries=chk_alive_tries+1
            
            end_time=int(time.time())
            secs=end_time-start_time
            
            if self.run.run_timeout is not None and  secs>self.run.run_timeout:
                code=SerialHandler.WRITE_FAILED
            
            if (code==SerialHandler.WRITE_FAILED or ser_out==None) and chk_alive_tries==self.MAX_CHK_ALIVE_TRIES:
                ##system unresponsive
                self.systemCrash=True
                return WorkloadHandler.SYSTEM_CRASHED
            elif (code==SerialHandler.WRITE_FAILED or ser_out==None) and chk_alive_tries<self.MAX_CHK_ALIVE_TRIES:
                continue
            else:
                chk_alive_tries=0
            
            found=False
            exitCode=0
            for line in ser_out.split("\n"):
                #print(line)
                if(found==True):
                    break;
                if "toKill" in line:  
                    tmp=line.split(" ")
                    for i in range(len(tmp)):
                        print(str(tmp[i]))
                        if(str(tmp[i]).strip()=="toKill"):
                            if(str(tmp[i+1]).strip()=="$?"):
                                continue
                            else:
                                print("WORKLOAD_HELPER_SCRIPT EXIT SIGNAL IS "+str(tmp[i+1]))
                                try:
                                    if(counter<10):
                                        exitCode=0
                                    else:
                                        exitCode=1
                                    counter+=1
                                except(ValueError):
                                    exitCode=0 #just assume it is still running and retry probing the status in the next iteration
                                found=True
                                break
            
            if(exitCode==0):##still running
                #secs+=WorkloadHandler.CHK_ALIVE_FREQ
                continue        
            
            if(exitCode==1):##succsfully finished check if output is not corrupt
                if WorkloadHandler.MEASURE_DROOP==True and self.run.platform=="juno":
                    pname=self.run.workloads[0].toKillName
                    print("DROOP "+str(pname)+" "+str(WorkloadHandler.MAX_DROOP))
                self.serial.sendCMD("pkill -SIGTERM chf_measure",waitTime=2) ##TODO this means that chf_measure_power script name should be fixed... make it fixed not an option (though is good to have it as a non-null indication
                self.serial.read()    
                self.serial.sendCMD("cat "+ self.workloadStatusOutput,waitTime=2)    
                ser_out=self.serial.read()
                if(ser_out==None):
                    count_of_lines=0
                else:
                    lines=ser_out.split("\n")
                    count_of_lines=0
                    for line in lines:
                        if "WORKLOAD_SCRIPT" in line:
                            count_of_lines=count_of_lines+1
                            if(len(line.split(" "))<WorkloadHandler.MIN_WORKLOAD_OUTPUT_COLUMNS):
                                self.abnormal_workload_status=True
                                return WorkloadHandler.WORKLOAD_SCRIPT_ABORTED #so the script produced abnormal output ?? consider system not responsive??
                            #print(line)
                if(count_of_lines!=len(self.run.workloads)):
                    self.abnormal_workload_status=True
                    return WorkloadHandler.WORKLOAD_SCRIPT_ABORTED #so the script produced abnormal output ?? consider system not responsive??
                
                self.statusOutputLines=lines

                return WorkloadHandler.WORKLOAD_SCRIPT_FINISHED_SUCCESFULLY  
 
    def hasSystemCrashOccured(self):
        return self.systemCrash
    
class Executor:
    
    #DEF_RUN=None
    DEF_TARG_HOST="xg2-1.in.cs.ucy.ac.cy"
    DEF_USER="zhadji01"
    DEF_PASSWD="agoodpasswd"
    #DEF_HELP_SCRIPT_WORKLOAD="/home/zhadji01/chf_helper_workload.sh"
    #IDLE_CORE_FREQ=300
    
    ##constants
    ALIVE=0
    APP_CRASH=1
    SYSTEM_CRASH=2
    SDC_OCCURED=3
    WAIT_FOR_AUTO_RESTART=250#seconds
    AUTO_RESTART_LOW_THRESH=20#seconds
    SAFE_VOL=980
    
    MAX_FREQUENCY=2400
    CORES_PER_PMD=2
    
    CONTINUE_AFTER_APP_CRASH_SDC=True
    RELATIVE_FREQ=False
    
    #DIFF_HELPER_SCRIPT="/home/zhadji01/diff_helper.sh"
    
    SUCCESS=0
    FAIL=1
    
    
    ##

    
    #run=DEF_RUN
    #targetHostName=DEF_TARG_HOST
    #targetSSHusername=DEF_USER
    #targetSSHpassword=DEF_PASSWD
    #helperSciprt=DEF_HELP_SCRIPT
        
    def __init__(self,helperScriptSetup,helperScriptWorkload,workloadStatusOutput,targetHostname="xg2-1.in.cs.ucy.ac.cy",targetSSHusername="zhadji01",targetSSHpassword="agoodpasswd",serialPort="COM3",sysLogParsingScript="/home/zhadji01/printErrorsWithinTimestamps",measurePowerScipt=None):
        #self.run=run
        self.targetHostName=targetHostname
        self.targetSSHusername=targetSSHusername
        self.targetSSHpassword=targetSSHpassword
        self.helperScriptSetup=helperScriptSetup
        self.helperScriptWorkload=helperScriptWorkload
        self.workloadStatusOutput=workloadStatusOutput
        self.serial=SerialHandler(serialPort)
        self.sysLogParsingScript=sysLogParsingScript
        self.measurePowerScript=measurePowerScipt


    @staticmethod
    def convertJsonToObject(data): #expects json string
        try:
            targetHostName=data["targetHostName"]
        except(KeyError) as err:
            targetHostName=Executor.DEF_TARG_HOST
            print(str(err))
            traceback.print_exc()
           
        try:
            targetSSHusername=data["targetSSHusername"]
        except(KeyError) as err:
            targetSSHusername=Executor.DEF_USER
            print(str(err))
            traceback.print_exc()
           
        try:
            targetSSHpassword=data["targetSSHpassword"]
        except(KeyError) as err:
            targetSSHpassword=Executor.DEF_PASSWD
            print(str(err))
            traceback.print_exc()
        
        try:
            measurePowerScript=data["measurePowerScript"]
        except(AttributeError,KeyError) as err:
            measurePowerScript=None 
           
        try:
            helperScriptWorkload=data["helperScriptWorkload"]
            helperScriptSetup=data["helperScriptSetup"]
            workloadStatusOutput=data["workloadStatusOutput"]
            serialPort=data["serialPort"]
            sysLogParsingScript=data["sysLogParsingScript"]
        except(KeyError) as err:
            #helperScript=Executor.DEF_HELP_SCRIPT    
            print(str(err))
            traceback.print_exc()
            exit(1)
        
        runExec=Executor(helperScriptSetup,helperScriptWorkload,workloadStatusOutput,targetHostname=targetHostName,targetSSHusername=targetSSHusername,targetSSHpassword=targetSSHpassword,serialPort=serialPort,sysLogParsingScript=sysLogParsingScript,measurePowerScipt=measurePowerScript)
        return runExec

    def calculateStableExperimentalFactors(self,run):        
        sshHandler=SSHhandler(targetHostname=self.targetHostName, targetSSHusername=self.targetSSHusername,targetSSHpassword=self.targetSSHpassword)
        run.dramVol=[]
        i2cnum=1
        if (int(run.platform)==4):#xgene3
            sshHandler.executeCommand("/home/root_desktop/chf_scripts/getI2cNum.sh")
            while(sshHandler.hasCommandFailed()):
                sshHandler.executeCommand("/home/root_desktop/chf_scripts/getI2cNum.sh")
            i2cnum=int(sshHandler.lastCommandOut()[0].replace("\n",""))
        sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x1 w`")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x1 w`")
        run.slimpro_version=int(sshHandler.lastCommandOut()[0])
        
        '''sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x3 w`")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x3 w`")
        run.platform=sshHandler.lastCommandOut()[0].replace("\n","")''' #let run platform do be specifed from user for now
        
        sshHandler.executeCommand("uname -a")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("uname -a")
        run.os_version=sshHandler.lastCommandOut()[0].replace("\n","")
        
        sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x36 w`")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x36 w`")
        run.dramVol.append(int(sshHandler.lastCommandOut()[0]))
        
        sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x37 w`")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x37 w`")
        run.dramVol.append(int(sshHandler.lastCommandOut()[0]))
        
        sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x41 w`")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x41 w`")
        run.dramFrequency=int(sshHandler.lastCommandOut()[0])
        
        sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x40 w`")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x40 w`")
        run.dramRefresh=int(sshHandler.lastCommandOut()[0])
        
        if run.coreVol is not None and run.vminComponent!="CORE": #ignore coreVol input in case core is the Vmin component
            sshHandler.executeCommand("sudo i2cset -y "+str(i2cnum)+"  0x2f 0x34 "+str(run.coreVol)+ " w")
            while(sshHandler.hasCommandFailed()):
                sshHandler.executeCommand("sudo i2cset -y "+str(i2cnum)+"  0x2f 0x34 "+str(run.coreVol)+ " w")
        else: 
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x34 w`")
            while(sshHandler.hasCommandFailed()):
                sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x34 w`")
            run.measuredCoreVol=int(sshHandler.lastCommandOut()[0])
        
        if run.uncoreVol is not None and run.vminComponent!="UNCORE": #ignore uncoreVol input in case uncore is the Vmin component
            sshHandler.executeCommand("sudo i2cset -y "+str(i2cnum)+"  0x2f 0x35 "+str(run.uncoreVol)+ " w")
            while(sshHandler.hasCommandFailed()):
                sshHandler.executeCommand("sudo i2cset -y "+str(i2cnum)+"  0x2f 0x35 "+str(run.uncoreVol)+ " w")
        else:
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x35 w`")
            while(sshHandler.hasCommandFailed()):
                sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x35 w`")
            run.measuredUncoreVol=int(sshHandler.lastCommandOut()[0])
        
        sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x42 w`")
        while(sshHandler.hasCommandFailed()):
            sshHandler.executeCommand("printf \"%d\n\" `sudo i2cget -y "+str(i2cnum)+"  0x2f 0x42 w`")
        run.uncoreFreq=int(sshHandler.lastCommandOut()[0])
    
    def configureJuno(self,run):
        from sendRebootCommand import sendRebootCommand
        from setVoltageThroughSerial import setVoltage
        from waitTillSSHworks import waitTillSSHworks
        from setFrequencyThroughSerial import setFrequency
        from getLowestVol import getLowestVol
        from disableApolloSSH import disableApollo
        
        sshHandler=SSHhandler(targetHostname=self.targetHostName, targetSSHusername=self.targetSSHusername,targetSSHpassword=self.targetSSHpassword)
        id=0
        for onlineOffline in run.onlineOfflineCores:
            sshHandler.executeCommand(command="echo " +str(onlineOffline) + " > /sys/devices/system/cpu/cpu" + str(id)+"/online")
            sshHandler.executeCommand(command="echo performance > /sys/devices/system/cpu/cpu" + str(id)+"/cpufreq/scaling_governor")
            id=id+1 #TODO this all part is discarded by disableApollo/disableAtlas part below .. also in configureA53 function
        print("governor set to performance")
        tries=0
        while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
            if self.serial.isSerialResponsive(timeout=2)==False:
                print("ERROR SYSTEM IS NOT RESPONSIVE BEFORE ATTEMPTING TO CONFIGURE.. trying again")
                tries=tries+1
                #exit(1)
            else:
                break
        
        if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):    
            print("ERROR SYSTEM IS NOT RESPONSIVE BEFORE ATTEMPTING TO CONFIGURE.. exitting")
            sys.exit(1) 
            
        if(self.serial.isLoginScreenReady()==False):
            code=self.serial.reachLoginScreenFromResponsiveSystem()
            tries=0
            while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                code=self.serial.reachLoginScreenFromResponsiveSystem()
                if(code==SerialHandler.SUCCESS):
                    break;
                tries=tries+1
            if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                print("ERROR CANNOT REACH LOGIN SCREEN..exiting")
                sys.exit(1)
        tries=0
        while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
            code=self.serial.performLogin(self.targetSSHusername, self.targetSSHpassword,timeout=2)
            if(code==SerialHandler.WRITE_FAILED):
                print("ERROR CANNOT LOGIN TO SYSTEM WRITE_FAILED.. exiting")
                tries=tries+1
                #exit(1)
            elif(code==SerialHandler.LOGIN_FAILED):
                print("ERROR CANNOT LOGIN TO SYSTEM Wrong credentials.. exiting")
                tries=tries+1
                #exit(1)
            elif(code==SerialHandler.UNEXPECTED_RESPONSE):
                print("ERROR CANNOT LOGIN TO SYSTEM Unexpected system response.. exiting")
                tries=tries+1
                #exit(1)
            else:
                break
        if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):    
            print("ERROR CANNOT LOGIN..exiting")
            sys.exit(1)
            
        nominal=1000
        disableApollo(self.targetHostName,self.targetSSHusername,self.targetSSHpassword)
        setVoltage(1,float(nominal)/1000,JUNO_DEBUG_PORT)
        #setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)
        setFrequency(run.core_to_frequencies[4], portCOM=JUNO_DEBUG_PORT, multiplier=20, supply=7)
        
    def configureJunoA53(self,run):
        from sendRebootCommand import sendRebootCommand
        from setVoltageThroughSerial import setVoltage
        from waitTillSSHworks import waitTillSSHworks
        from setFrequencyThroughSerial import setFrequency
        from getLowestVol import getLowestVol
        from disableAtlas import disableAtlas
        from executeCommandSSH import executeCommand
        
        sshHandler=SSHhandler(targetHostname=self.targetHostName, targetSSHusername=self.targetSSHusername,targetSSHpassword=self.targetSSHpassword)
        id=0
        for onlineOffline in run.onlineOfflineCores:
            sshHandler.executeCommand(command="echo " +str(onlineOffline) + " > /sys/devices/system/cpu/cpu" + str(id)+"/online")
            id=id+1
        sshHandler.executeCommand(command="echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
        print("governor set to performance")
        tries=0
        while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
            print("empeika1")
            if self.serial.isSerialResponsive(timeout=2)==False:
                print("ERROR SYSTEM IS NOT RESPONSIVE BEFORE ATTEMPTING TO CONFIGURE.. trying again")
                tries=tries+1
                #exit(1)
            else:
                break
        print("empeika2")   
        if(self.serial.isLoginScreenReady()==False):
            print("empeika31")
            code=self.serial.reachLoginScreenFromResponsiveSystem()
            tries=0
            while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                code=self.serial.reachLoginScreenFromResponsiveSystem()
                if(code==SerialHandler.SUCCESS):
                    break;
                tries=tries+1
            if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                print("ERROR CANNOT REACH LOGIN SCREEN..exiting")
                sys.exit(1)
        tries=0
        print("empeika31")
        while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
            
            
            code=self.serial.performLogin(self.targetSSHusername, self.targetSSHpassword,timeout=2)
            if(code==SerialHandler.WRITE_FAILED):
                print("ERROR CANNOT LOGIN TO SYSTEM WRITE_FAILED.. exiting")
                tries=tries+1
                #exit(1)
            elif(code==SerialHandler.LOGIN_FAILED):
                print("ERROR CANNOT LOGIN TO SYSTEM Wrong credentials.. exiting")
                tries=tries+1
                #exit(1)
            elif(code==SerialHandler.UNEXPECTED_RESPONSE):
                print("ERROR CANNOT LOGIN TO SYSTEM Unexpected system response.. exiting")
                tries=tries+1
                #exit(1)
            else:
                break
        if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):    
            print("ERROR CANNOT LOGIN..exiting")
            sys.exit(1)
            
        nominal=1000
        disableAtlas(self.targetHostName,self.targetSSHusername,self.targetSSHpassword)
        if(JUNO_BOOST_INTERRUPTS):
            executeCommand(hostname="10.16.20.179",username="root",password="root",command="pkill selfLoop",background=False)     
        executeCommand(hostname="10.16.20.179",username="root",password="root",command="mount /dev/sdb1 /media/oldDisk1/",background=False)
        if(JUNO_BOOST_INTERRUPTS):
            executeCommand(hostname="10.16.20.179",username="root",password="root",command="pkill selfLoop",background=False)     
            '''
            if(CURRENTCORERUNNING==0):
                commandInterrupt="taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & taskset -c 5 ./selfLoop>/dev/null &"
            elif(CURRENTCORERUNNING==1):
                commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & taskset -c 5 ./selfLoop>/dev/null &"
            elif(CURRENTCORERUNNING==2):
                commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 3 ./selfLoop>/dev/null &  taskset -c 5 ./selfLoop>/dev/null &"
            elif(CURRENTCORERUNNING==3):
                commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & "
            executeCommand(hostname="10.16.20.179",username="root",password="root",command=commandInterrupt,background=False)            
            CURRENTCORERUNNING+=1      
            '''           
        setVoltage(2,float(nominal)/1000,JUNO_DEBUG_PORT)
        #setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)
        setFrequency(run.core_to_frequencies[0], portCOM=JUNO_DEBUG_PORT, multiplier=16, supply=6)
            
       
    def configureTheTarget(self,run):
        
        sshHandler=SSHhandler(targetHostname=self.targetHostName, targetSSHusername=self.targetSSHusername,targetSSHpassword=self.targetSSHpassword)
        id=0
        for onlineOffline in run.onlineOfflineCores:
            sshHandler.executeCommand(command="echo " +str(onlineOffline) + " > /sys/devices/system/cpu/cpu" + str(id)+"/online")
            id=id+1
        
        convertedFreqStr=""
        for frequency in run.core_to_frequencies:
            if  Executor.RELATIVE_FREQ == True:
                convertedFreq=int(float(frequency)/Executor.MAX_FREQUENCY*1000)
            else:
                convertedFreq=str(frequency)+"M"
            #convertedFrequencies.append(convertedFreq)
            convertedFreqStr=convertedFreqStr+str(convertedFreq)+","
            
        convertedFrequencies=list(convertedFreqStr)
        convertedFrequencies.pop()
        convertedFreqStr= ''.join(convertedFrequencies)
        
        idle_cores_str=""
        for core in run.idle_cores:
            idle_cores_str=idle_cores_str+str(core)+","
            
        tmp=list(idle_cores_str)
        tmp.pop()
        idle_cores_str=''.join(tmp)
        
        if self.serial.isSerialResponsive(timeout=2)==False:
            print("ERROR SYSTEM IS NOT RESPONSIVE BEFORE ATTEMPTING TO CONFIGURE..exiting")
            exit(1)
  
        if(self.serial.isLoginScreenReady()==False):
            code=self.serial.reachLoginScreenFromResponsiveSystem()
            tries=0
            while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                code=self.serial.reachLoginScreenFromResponsiveSystem()
                if(code==SerialHandler.SUCCESS):
                    break;
                tries=tries+1
            if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                print("ERROR CANNOT REACH LOGIN SCREEN..exiting")
                exit(1)
        
        tries=0
        while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
            code=self.serial.performLogin(self.targetSSHusername, self.targetSSHpassword,timeout=2)
            if(code==SerialHandler.WRITE_FAILED):
                print("ERROR CANNOT LOGIN TO SYSTEM WRITE_FAILED.. trying again")
                tries=tries+1
                #exit(1)
            elif(code==SerialHandler.LOGIN_FAILED):
                print("ERROR CANNOT LOGIN TO SYSTEM Wrong credentials.. trying again")
                tries=tries+1
                #exit(1)
            elif(code==SerialHandler.UNEXPECTED_RESPONSE):
                print("ERROR CANNOT LOGIN TO SYSTEM Unexpected system response.. trying again")
                tries=tries+1
                #exit(1)
            else:
                break
        if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):    
            print("ERROR CANNOT LOGIN..exiting")
            sys.exit(1)
        
        
        command=str(self.helperScriptSetup)+" "+str(convertedFreqStr)+" "+str(idle_cores_str)+" "+str(run.smp_affinity)
        print(str("Command to execute "+command))
        code=self.serial.sendCMD(command, waitTime=30)#wait time empirically chosen 4 seconds are actually required chosen two times more
        if code==SerialHandler.WRITE_FAILED:
            print("Can not configure the system.. exitting")
            exit(1)
            
        self.calculateStableExperimentalFactors(run)
        
    
    BREAK_ON_FIRST_EMERGENCY=False
    
    def calculateMesurementsPowerHelper(self,jsonOutput,workloadHandler,key1,key2):
        cpuPowerValues=workloadHandler.calculateMeasurementSSH(key1) #key1 pmd_power
        if jsonOutput.power is None: 
            jsonOutput.power=[]
        power_obj= power()
        power_obj.type=key2 #key2 pmd
        power_obj.min_max_avg=cpuPowerValues
        power_obj.values=workloadHandler.calculateMeasurementValues(key1)
        power_obj.timestep=2 #TODO fix magic variable
        jsonOutput.power.append(power_obj) 
    
    def calculateMesurementsTempHelper(self,jsonOutput,workloadHandler,key1,key2):
        tempPowerValues=workloadHandler.calculateMeasurementSSH(key1) #key1 pmd_power
        if jsonOutput.temperature is None:
            jsonOutput.temperature=[]
        temp_obj= temperature()
        temp_obj.type=key2 #key2 pmd
        temp_obj.min_max_avg=tempPowerValues
        temp_obj.values=workloadHandler.calculateMeasurementValues(key1)
        temp_obj.timestep=2 #TODO fix magic variable
        jsonOutput.temperature.append(temp_obj) 
    
    def readHealthData(self,jsonOutput,workloadHandler,rebootOccured=False,startTime=None,endTime=None):
        if self.measurePowerScript is not None and rebootOccured==False: ##if reboot occured is due to crash.. in case of crash the values most likely are broken therefore don't read them
            ### power
            self.calculateMesurementsPowerHelper(jsonOutput, workloadHandler, "pmd_power", "pmd")
            self.calculateMesurementsPowerHelper(jsonOutput, workloadHandler, "uncore_power", "SoC_VRD")
            self.calculateMesurementsPowerHelper(jsonOutput, workloadHandler, "dram1_power", "DIMM_VRD1")
            self.calculateMesurementsPowerHelper(jsonOutput, workloadHandler, "dram2_power", "DIMM_VRD2")
            ##
                        
            ##temp
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "pmd_temp", "pmd")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "uncore_temp", "SoC_VRD")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram1_temp", "CH0_DIMM0")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram2_temp", "CH0_DIMM1")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram3_temp", "CH1_DIMM0")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram4_temp", "CH1_DIMM1")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram5_temp", "CH2_DIMM0")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram6_temp", "CH2_DIMM1")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram7_temp", "CH3_DIMM0")
            self.calculateMesurementsTempHelper(jsonOutput, workloadHandler, "dram8_temp", "CH3_DIMM1")
            ##
        if self.sysLogParsingScript is not None:
            errString=""
            if rebootOccured==False:
                errString=workloadHandler.calculateErrorInfo()
            else:
                ## calculate error messages after reboot
                errString=workloadHandler.calculateErrorInfoAfterReboot(startTime, endTime, self.sysLogParsingScript)
            ##ASSIGN ERROR MESSAGES
            jsonOutput.err_messages=errString
            jsonOutput.soc_overtemp=workloadHandler.soc_overtemp
            jsonOutput.pmd_errors=workloadHandler.pmd_errors
            jsonOutput.pmd_l2_errors=workloadHandler.pmd_l2_errors
            jsonOutput.l3_errors=workloadHandler.l3_errors
            jsonOutput.mcu_errors=workloadHandler.mcu_errors
            jsonOutput.pcie_errors=workloadHandler.pcie_errors
            jsonOutput.sata_errors=workloadHandler.sata_errors
            jsonOutput.dimm_vrd_hot=workloadHandler.dimm_vrd_hot
            jsonOutput.pmd_vrd_hot=workloadHandler.pmd_vrd_hot
            jsonOutput.soc_vrd_hot=workloadHandler.soc_vrd_hot
            ##########################################
    
    def printRunOutput(self,jsonOutput):
        if MongoDBhandler.Global is None:
            print("JSON "+str(returnJsonAsString(jsonOutput))+"\n") #print output
        else:
            MongoDBhandler.Global.insertDoc(jsonpickle.decode(jsonpickle.encode(jsonOutput,unpicklable=False))) 
    
    def sendRebootCommand(self,platform):
        if int(platform) == 4: #4 is xgene3
            while True:
                try:                
                    ssh = SSHClient()
                    ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                    #ssh.connect("zhadji01-Desktop.in.cs.ucy.ac.cy", username="zhadji01", password="root", timeout=5) -aproxe01
                    ssh.connect("10.16.20.174", username="xi_latte", password="Alohomora", timeout=5)
                    stdin,stdout,stderr=ssh.exec_command(command="ipmitool -H 10.16.20.189 -U ADMIN -P ADMIN -I lanplus power off; sleep 10; ipmitool -H 10.16.20.189 -U ADMIN -P ADMIN -I lanplus power on")
                    self.out=stdout.readlines() #just do this to make exec blocking call
                    self.err=stderr.readlines()       
                    ssh.close()
                    break
                except(paramiko.SSHException, paramiko.BadHostKeyException, paramiko.AuthenticationException, socket.error,EOFError):
                    #print("Failed to reboot through ipmi.. cannot connect to virtual box.. retrying..")             
                    continue;
        else:
            print("ERROR SEND REBOOT COMMAND NOT DEFINED FOR PLATFORM "+str(platform))
            sys.exit(1)
        
    def execute_full_exp(self,run,CURRENTCORERUNNING,testUntilUnsafe=True):
        from executeCommandSSH import executeCommand
        ##ssh is deprecated
        sshHandler=SSHhandler(targetHostname=self.targetHostName, targetSSHusername=self.targetSSHusername,targetSSHpassword=self.targetSSHpassword)
        voltage_generator=NextVoltageGenerator(run.start_voltage,run.end_voltage,int(run.vol_inc),NextVoltageGenerator.METHOD_INCREMENTAL)
        voltage=voltage_generator.get_vol()
        while voltage!=NextVoltageGenerator.NO_MORE_VOLTAGES: 
          
            ##TODO order matters, two options a) set first voltage then start benchmark b) start benchmark then immediately set voltage
            #vmin=voltage
            #ASSSUMPTION AT THE BEGINNING OF EACH VOLTAGE STEP WE HAVE STABLE STATE, 
            #BECAUSE WE CHECK STABILITY AT THE END OF EACH VOLTAGE STEP
            workloadHandler = WorkloadHandler (sshHandler,self.serial,run,self.helperScriptWorkload,self.workloadStatusOutput,self.measurePowerScript)
            if "juno_a53" in str(run.platform):
                
                executeCommand(hostname="10.16.20.179",username="root",password="root",command="./getInterruptsA53Plus.sh >> IDLE3CORES0",background=False)
                if(JUNO_BOOST_INTERRUPTS):
                    executeCommand(hostname="10.16.20.179",username="root",password="root",command="pkill selfLoop",background=False)     
                    '''
                    if(CURRENTCORERUNNING==0):
                        commandInterrupt="taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & taskset -c 5 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==1):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & taskset -c 5 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==2):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 3 ./selfLoop>/dev/null &  taskset -c 5 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==3):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null & "
                    executeCommand(hostname="10.16.20.179",username="root",password="root",command=commandInterrupt,background=False)            
                    '''
                    '''
                    if(CURRENTCORERUNNING==0):
                        commandInterrupt="taskset -c 3 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==1):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 4 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==2):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 3 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==3):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null & taskset -c 3 ./selfLoop>/dev/null &"
                    '''
                    
                    if(CURRENTCORERUNNING==0):
                        commandInterrupt="taskset -c 3 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==1):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==2):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null &"
                    elif(CURRENTCORERUNNING==3):
                        commandInterrupt="taskset -c 0 ./selfLoop>/dev/null &"
                    
                    executeCommand(hostname="10.16.20.179",username="root",password="root",command=commandInterrupt,background=False)       
                    #CURRENTCORERUNNING+=1
                workloadHandler.UNRESPONSIVE_TIMEOUT=1
            workloadHandler.setVoltageOfObservation(voltage)
            if "juno_a53" in str(run.platform): #for juno we cannot set voltage from the helper script hence we have to use the serial
                from setVoltageThroughSerial import setVoltage
                setVoltage(2,float(voltage)/1000,JUNO_DEBUG_PORT)
            elif "juno" in str(run.platform):
                from setVoltageThroughSerial import setVoltage
                setVoltage(1,float(voltage)/1000,JUNO_DEBUG_PORT)            
            startTime=int(time.time())
            #workloadHandler.startWorkload()
            if(measureInterrupts):
                executeCommand(hostname="10.16.20.179",username="root",password="root",command="./getInterruptsA53Plus.sh >> "+interruptFileName,background=False)
            

                
            code=workloadHandler.waitWorkloadToFinish()
            print("workload finished")
            if(measureInterrupts):
                executeCommand(hostname="10.16.20.179",username="root",password="root",command="./getInterruptsA53Plus.sh >> "+interruptFileName,background=False)
            endTime=int(time.time())
            
            
            if "juno_a53" in str(run.platform):
                from setVoltageThroughSerial import setVoltage
                setVoltage(2,float(1000)/1000,JUNO_DEBUG_PORT)
            elif "juno" in str(run.platform):
                from setVoltageThroughSerial import setVoltage                               
                setVoltage(1,float(1000)/1000,JUNO_DEBUG_PORT)
         
            ###construct (initialize) json output
            jsonOutput= expOut()
            run.jsonExpOutInit(jsonOutput)
            
            if WorkloadHandler.MEASURE_EM==True:
                jsonOutput.EM=WorkloadHandler.FREQ_AMP_PAIRS
            ##bunch of boring output data
            jsonOutput.date=workloadHandler.start_timestamp
            jsonOutput.system_crash=workloadHandler.systemCrash
            jsonOutput.core_vol=run.coreVol
            jsonOutput.dram_vol=[]
            for dramVoltage in run.dramVol:
                jsonOutput.dram_vol.append(dramVoltage)
            jsonOutput.dram_freq=run.dramFrequency
            if run.dramRefresh is not None:
                jsonOutput.dram_refresh=float(float(run.dramRefresh)*100)/1000000
            jsonOutput.uncore_freq=run.uncoreFreq
            jsonOutput.uncore_vol=run.uncoreVol
            jsonOutput.os_version=run.os_version
            jsonOutput.platform=run.platform
            jsonOutput.slimpro_rev=run.slimpro_version
            
            if run.vminComponent=="CORE":
                jsonOutput.core_vol=workloadHandler.getVoltageOfObservation()
                if run.measuredUncoreVol is not None:
                    jsonOutput.uncore_vol=run.measuredUncoreVol
            elif run.vminComponent=="UNCORE":
                jsonOutput.uncore_vol=workloadHandler.getVoltageOfObservation()
                if run.measuredCoreVol is not None:
                    jsonOutput.core_vol=run.measuredCoreVol
            ##end of bunch of boring output data
            
            ##here begins the interesting part
            if (code==workloadHandler.WORKLOAD_SCRIPT_FINISHED_SUCCESFULLY): ##SYSTEM CRASH NOT HAPPENED
                #run.system_crash=False
                workloadHandler.calculateWorkloadStatus()               
                self.readHealthData(jsonOutput,workloadHandler,False) #write to json power,temp,perf counter errors bla bla bla
                i=0
                workloadUnsafe=False
                for workload in run.workloads:
                    jsonOutput.workloads[i].crash=workload.crash
                    jsonOutput.workloads[i].sdc=workload.sdc
                    jsonOutput.workloads[i].exitCode=workload.exitCode
                    jsonOutput.workloads[i].exec_time=workload.executionTime
                    jsonOutput.workloads[i].quality_metric=workload.qos
                    if workload.crash==True or workload.sdc==True:
                        workloadUnsafe=True
                    i=i+1
                self.printRunOutput(jsonOutput)      
                if workloadUnsafe==True:
                    if testUntilUnsafe==True:
                        if voltage >= run.end_voltage:
                            run.end_voltage=voltage+10 #modify the end voltage to test until unsafe next time
                        #self.sendRebootCommand(run.platform) only available for X-Gene3
                        self.__handleRestart_(run.platform)
                        break; #break the vmin process if workload didn't finish correctly      
                #end of not system crash if
            else:  ### SYSTEM_CRASH case essentialy this must be true if workloadHandler.abnormal_workload_status==True or workloadHandler.systemCrash==True:            
                i=0
                for workload in run.workloads:
                    #if jsonOutput.workloads[i].exec_time == None:
                    jsonOutput.workloads[i].exec_time=int(int(endTime)-int(startTime))-(WorkloadHandler.UNRESPONSIVE_TIMEOUT*WorkloadHandler.MAX_CHK_ALIVE_TRIES)# record seconds to system crash time since we cannot read workload execution time due to system crash
                    jsonOutput.workloads[i].crash=None #we could not observe this because of the crash, hence, put in null
                    jsonOutput.workloads[i].sdc=None
                    jsonOutput.workloads[i].exitCode=None
                    jsonOutput.workloads[i].quality_metric=None
                    i=i+1
                    
                #self.__handleRestartSerial__()
                self.__handleRestart_(run.platform)
                
                ### write to json after reboot errors, temp, power perf counters etc
                self.readHealthData(jsonOutput,workloadHandler,True,startTime,endTime)    
                ###
                
                if testUntilUnsafe==True:
                    if voltage >= run.end_voltage:
                        run.end_voltage=voltage+10 #modify the end voltage to test until unsafe next time
                if workloadHandler.abnormal_workload_status==True:
                    print("ABNORMAL WORKLOAD SCRIPT OUTPUT CONSIDERED SYSTEM_CRASH "+str(jsonOutput))
                self.printRunOutput(jsonOutput)
                break #if system crash occur break the vmin process
                ###end of system crash if
                    
            voltage_generator.cal_next() #calc next voltage
            voltage=voltage_generator.get_vol()
        
        ### end of main while
        #self.__handleRestart_(run.platform) #TODO this is to avoid dropping voltage till system crash
        
    def closeSerial(self):
        self.serial.close()
    
    def openSerial(self):
        self.serial.openSerial()        
   
    def execute(self,run,mode=1):
        if run.run_type==Experiment.RUN_TYPE_CRASH:
            self.execute_crash_only_exp(run,mode)
        elif run.run_type==Experiment.RUN_TYPE_ALL:
            self.execute_full_exp(run,mode)

    def handleRestartSerial_(self):
        print("Waiting for auto restart")
        start = time.time() 
        while True:
            end = time.time()
            timePassed=(end-start)
            if(timePassed>self.WAIT_FOR_AUTO_RESTART):
                print("waiting for auto restart reached the time limit.. proceeding with turning off plug")
                break       
            if timePassed<200:
                hasBooted=self.serial.hasBootedSuccesfully()
            else:
                hasBooted=self.serial.isLoginScreenReady() ##after two minutes start checking whether we missed the xg2-1: login string..I have experienced this happening
            if(hasBooted):
                print("waiting for auto restart took "+str(end-start)+" seconds")
                if((end-start)<self.AUTO_RESTART_LOW_THRESH):
                    print("Auto restart took only "+str(end-start)+" something going wrong.. restart by plug")
                    break;
                return
            
        os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
        print("turning off at voltage ")
        time.sleep(7)  # wait for 5 second.. don't know just feel need to wait before powering again
        command = "C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 check | C:/cygwin64/bin/grep -o 'ON\|OFF' \""
        
        while True:
            # os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
            result = subprocess.check_output(command, shell=True)
            if "ON" in str(result):
                print("plug is ON and should not be")
                os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
                print("turning off at voltage ")
                time.sleep(6)  # wait for 5 second.. don't know just feel need to wait before powering again
            elif "OFF" in str(result):
                print ("plug is OFF.. as it should")
                break
            else:
                print("no response received.. keep trying to get plug status")
                continue   
                     
        os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 on\"")
        print("turning on at voltage ")
        time.sleep(4)
        start = time.time() 
        
        while True: ##wait for board to go back online
            # os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
            result = subprocess.check_output(command, shell=True)
            if "ON" in str(result):
                print("plug is ON and should be")
                break
            elif "OFF" in str(result):
                print ("plug is OFF.. it shouldnt")
                os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 on\"")
                print("turning on at voltage ")
                time.sleep(4)  # wait for 4 second.. don't know just feel need to wait before powering again
                start = time.time() 
                break
            else:
                print("no response received.. keep trying to get plug status")
                continue        
        while True:
            end = time.time()
            timePassed=(end-start)
            if timePassed<200:
                hasBooted=self.serial.hasBootedSuccesfully()
            else:
                hasBooted=self.serial.isLoginScreenReady() ##after two minutes start checking whether we missed the xg2-1: login string..I have experienced this happening
            if(hasBooted):
                break
            else: # coninue trying if server has not restarted yet
                # todo CHECK plug status here.. had a case where plug was not turned on.. when it should be
                #command = "C:/cygwin64/bin/bash.exe -l -c\"/home/zhadji01/hs100.sh 192.168.159.129 9999 check | C:/cygwin64/bin/grep -o 'ON\|OFF' \""
                command = "C:/cygwin64/bin/bash.exe -l -c  \"/home/zhadji01/hs100.sh 192.168.159.129 9999 check | C:/cygwin64/bin/grep -o 'ON\|OFF' \""
                # os.system("C:/cygwin64/bin/bash.exe -l -c\"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
                result = subprocess.check_output(command, shell=True)
    
                if "ON" in str(result):
                    print("plug is ON as it should be")
                    if timePassed>600: #something very wrong happened need to restart board
                        #start=time.time()
                        print("turning off plug.. seems hang during boot occured")
                        os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
                        time.sleep(6)
                elif "OFF" in str(result):
                    print ("plug is OFF.. turning it on")
                    os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 on\"")
                    time.sleep(6)  # wait few seconds
                    start = time.time() 
                    continue
                else:
                    print ("unknown response received from plug.. continue waiting the board to boot")
                    continue;   
    
    RESTART_SERIAL=True
    
    def handleRestartXG3(self):
        print("Waiting for auto restart")
        start = time.time()
        maxloginScreenTries=3
        loginScreenTries=0
        waitForAutoRestart=self.WAIT_FOR_AUTO_RESTART
        while True:
            end = time.time()
            timePassed=(end-start)
            if(timePassed>waitForAutoRestart):
                print("waiting for auto restart reached the time limit.. proceeding with turning off plug")
                break       
            if timePassed<200:
                hasBooted=self.serial.hasBootedSuccesfully()
            else:
                hasBooted=self.serial.isLoginScreenReady() ##after two minutes start checking whether we missed the xg2-1: login string..I have experienced this happening
                #loginScreenTries=loginScreenTries+1
                #if loginScreenTries> maxloginScreenTries:
                #    break
            if(hasBooted):
                print("waiting for auto restart took "+str(end-start)+" seconds")
                if((end-start)<self.AUTO_RESTART_LOW_THRESH):
                    print("Auto restart took only "+str(end-start)+" something going wrong.. restart by plug")
                    break;
                return
            
        ##Reset the server
        while True:
            try:                
                ssh = SSHClient()
                ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                ssh.connect("10.16.20.174", username="xi_latte", password="Alohomora", timeout=5)
                stdin,stdout,stderr=ssh.exec_command(command="ipmitool -H 10.16.20.189 -U ADMIN -P ADMIN -I lanplus power off; sleep 10; ipmitool -H 10.16.20.189 -U ADMIN -P ADMIN -I lanplus power on")
                self.out=stdout.readlines() #just do this to make exec blocking call
                self.err=stderr.readlines()       
                ssh.close()
                break
            except(paramiko.SSHException, paramiko.BadHostKeyException, paramiko.AuthenticationException, socket.error,EOFError):
                #print("Failed to reboot through ipmi.. cannot connect to virtual box.. retrying..")             
                continue;
        
        loginScreenTries=0
        start=time.time()
        while True: ##wait for board to go back online
            end = time.time()
            timePassed=(end-start)
            if(timePassed>self.WAIT_FOR_AUTO_RESTART):
                # coninue trying if server has not restarted yet
                ##Reset the server
                while True:
                    try:                
                        ssh = SSHClient()
                        ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                        ssh.connect("10.16.20.174", username="xi_latte", password="Alohomora", timeout=5)
                        stdin,stdout,stderr=ssh.exec_command(command="ipmitool -H 10.16.20.189 -U ADMIN -P ADMIN -I lanplus power off; sleep 10; ipmitool -H 10.16.20.189 -U ADMIN -P ADMIN -I lanplus power on")
                        self.out=stdout.readlines() #just do this to make exec blocking call
                        self.err=stderr.readlines()       
                        ssh.close()
                        break
                    except(paramiko.SSHException, paramiko.BadHostKeyException, paramiko.AuthenticationException, socket.error,EOFError):
                        #print("Failed to reboot through ipmi.. cannot connect to virtual box.. retrying..")             
                        continue;
                start=time.time()
                loginScreenTries=0 
            
            if timePassed<200:
                hasBooted=self.serial.hasBootedSuccesfully()
            else:
                hasBooted=self.serial.isLoginScreenReady() ##after two minutes start checking whether we missed the xg2-1: login string..I have experienced this happening
                #loginScreenTries=loginScreenTries+1
                #if loginScreenTries> maxloginScreenTries:
                   
                    
            if(hasBooted):
                break
    
    def __handleRestart_(self,platform):
        #time.sleep(7) #wait for the disk to finish any i/o
        #connected=False
        if "juno" in str(platform): #TODO fix this in the future
            from sendRebootCommand import  sendRebootCommand
            from waitTillSSHworks import waitTillSSHworks
            from executeCommandSSH import executeCommand
            timeOut=300
            '''' #start of ssh reboot code
            code=1
            while code==1:    
                sendRebootCommand(JUNO_DEBUG_PORT)
                code=waitTillSSHworks(self.targetHostName,self.targetSSHusername,self.targetSSHpassword,timeOut)
            return
            ''' #end of ssh reboot code
            ##serial reboot code
            #executeCommand(hostname="10.16.20.179",username="root",password="root",command="umount /media/oldDisk1/",background=False)
            sendRebootCommand(JUNO_DEBUG_PORT)
            start = time.time() 
            while True:
                time.sleep(1)
                end = time.time()
                if((end-start)>timeOut):
                    print("waiting for auto restart reached the time limit.. proceeding with Reboot")
                    sendRebootCommand(JUNO_DEBUG_PORT)
                    start = time.time()
                command = "cd C:/Users/admin/Documents/DevCon/x86/ && chf_helper_renalbeUSBs.bat"
                while True:
                    try:
                        result = subprocess.check_output(command, shell=True)
                        break
                    except subprocess.CalledProcessError:
                        traceback.print_exc()
                        print("RESTART HANDLER FAILED TO RE-ENABLE THE USBS.. Trying again")
                        time.sleep(5)
                        continue
                self.closeSerial()
                self.openSerial()
                #hasBooted=self.serial.hasBootedSuccesfully(lookFor="juno_uni login:")
                timePassed=(end-start)
                if timePassed<60:
                    print("empika1")
                    hasBooted=self.serial.hasBootedSuccesfully(lookFor="root@juno_uni:~#")
                else:
                    print("empika2")
                    hasBooted=self.serial.isLoginScreenReady() ##after two minutes start checking whether we missed the xg2-1: login string..I have experienced this happening
                if hasBooted==True:
                    print("efkika")
                    return 
        if Executor.RESTART_SERIAL==True:
            if int(platform) == 4: #4 is xgene3
                self.handleRestartXG3()
            elif int(platform)==2:#is xgene2)    
                self.handleRestartSerial_()
        else:
            print("Waiting for auto restart")
            start = time.time() 
            while True:
                end = time.time()
                if((end-start)>self.WAIT_FOR_AUTO_RESTART):
                    print("waiting for auto restart reached the time limit.. proceeding with turning off plug")
                    break 
                try:                
                    ssh = SSHClient()
                    ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                    ssh.connect(self.targetHostName, username=self.targetSSHusername, password=self.targetSSHpassword, timeout=5)            
                    # time.sleep(2)
                    #connected=True
                    ssh.close()
                    end = time.time()
                    print("waiting for auto restart took "+str(end-start)+" seconds")
                    if((end-start)<self.AUTO_RESTART_LOW_THRESH):
                        print("Auto restart took only "+str(end-start)+" something going wrong.. restart by plug")
                        break;
                    return
                except(paramiko.SSHException, paramiko.BadHostKeyException, paramiko.AuthenticationException, socket.error,EOFError):
                    ##server still not up waiting                
                    continue;
            os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
            print("turning off at voltage ")
            time.sleep(7)  # wait for 5 second.. don't know just feel need to wait before powering again
            command = "C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 check | C:/cygwin64/bin/grep -o 'ON\|OFF' \""
            while True:
                # os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
                result = subprocess.check_output(command, shell=True)
                if "ON" in str(result):
                    print("plug is ON and should not be")
                    os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
                    print("turning off at voltage ")
                    time.sleep(6)  # wait for 5 second.. don't know just feel need to wait before powering again
                elif "OFF" in str(result):
                    print ("plug is OFF.. as it should")
                    break
                else:
                    print("no response received.. keep trying to get plug status")
                    continue            
                    os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 on\"")
                    print("turning on at voltage ")
                    time.sleep(4)
            while True: ##wait for board to go back online
                # os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
                result = subprocess.check_output(command, shell=True)
                if "ON" in str(result):
                    print("plug is ON and should be")
                    break
                elif "OFF" in str(result):
                    print ("plug is OFF.. it shouldnt")
                    os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 on\"")
                    print("turning on at voltage ")
                    time.sleep(4)  # wait for 4 second.. don't know just feel need to wait before powering again
                    break
                else:
                    print("no response received.. keep trying to get plug status")
                    continue        
            while True:
                try:
                    ssh = SSHClient()
                    ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
                    ssh.connect(self.targetHostName, username=self.targetSSHusername, password=self.targetSSHpassword, timeout=5)            
                    # time.sleep(2)
                    break
                except(paramiko.SSHException, paramiko.BadHostKeyException, paramiko.AuthenticationException, socket.error): # coninue trying if server has not restarted yet
                    # todo CHECK plug status here.. had a case where plug was not turned on.. when it should be
                    #command = "C:/cygwin64/bin/bash.exe -l -c\"/home/zhadji01/hs100.sh 192.168.159.129 9999 check | C:/cygwin64/bin/grep -o 'ON\|OFF' \""
                    command = "C:/cygwin64/bin/bash.exe -l -c  \"/home/zhadji01/hs100.sh 192.168.159.129 9999 check | C:/cygwin64/bin/grep -o 'ON\|OFF' \""
                    # os.system("C:/cygwin64/bin/bash.exe -l -c\"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
                    result = subprocess.check_output(command, shell=True)
        
                    if "ON" in str(result):
                        print("plug is ON as it should be")
                    elif "OFF" in str(result):
                        print ("plug is OFF.. turning it on")
                        os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 on\"")
                        time.sleep(6)  # wait few seconds
                        continue
                    else:
                        print ("unknown response received from plug.. continue waiting the board to boot")
                        continue;   
            ssh.close()