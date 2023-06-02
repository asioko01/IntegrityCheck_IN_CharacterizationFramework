'''
Created on May 5, 2017

@author: zhadji01
'''
import serial
import time
from serial import SerialTimeoutException
import traceback
from serial.serialutil import SerialException

class SerialHandler(object):
    '''
    classdocs
    '''
    ##error statuses
    WRITE_FAILED=1 ##basically used when system is unresponsive
    WRITE_SUCCESS=0
    LOGIN_FAILED=2
    UNEXPECTED_RESPONSE=3
    ##end of error statuses
    
    SUCCESS=0
    FAIL=1
    
    REACH_LOGIN_SCREEN_TIMEOUT=5
    LOGIN_STEPS_TIMEOUT=3
    EXPECTED_TIMEOUT=5
    RESPONSIVENESS_CHECK_TIMEOUT=2
    EXIT_TIMEOUT=15
    UNRESPONSIVE_TIMEOUT=25
    MAX_REACH_LOGIN_SCREEN_TRIES=10
    
    def __init__(self,port='COM8'):
        '''
        Constructor
        '''
        self.baudrate=115200
        self.port=port
        self.timeout=SerialHandler.UNRESPONSIVE_TIMEOUT
        self.openSerial()
        # configure the serial connections (the parameters differs on the device you are connecting to)
        '''self.ser = serial.Serial(port=self.port,baudrate=self.baudrate,timeout=self.timeout)
        self.ser.write_timeout=SerialHandler.UNRESPONSIVE_TIMEOUT
        if (self.ser.is_open==False):
            print("failed to open port")
            exit(1)
        self.trans_err_status=None 
        self.trans_output=None'''   
    #assumes that the serial starts from login screen.. 
    #if not though, this command will try to reach it.. before return this function will logout..
    #functin set the transOutput varialbe and if any step fails it will and set an error status  
    
    def transaction(self,cmd,username,passwd,waitTime=EXPECTED_TIMEOUT,flushPreviousInput=True): 
        self.trans_err_status=SerialHandler.WRITE_SUCCESS
        if(flushPreviousInput):
            self.ser.flushInput()
        if(self.isSerialResponsive()==False):
            self.trans_err_status= SerialHandler.WRITE_FAILED
            return
        if(self.isLoginScreenReady()==False):
            code=self.reachLoginScreenFromResponsiveSystem()
            tries=0
            while (tries<SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                code=self.reachLoginScreenFromResponsiveSystem()
                if(code==SerialHandler.SUCCESS):
                    break;
                tries=tries+1
            if(tries>=SerialHandler.MAX_REACH_LOGIN_SCREEN_TRIES):
                print("SERIAL_HANDLER: Failed to reach login screen exiting")
                exit(1)
            else:
                print("SERIAL_HANDLER: Succesfully reached login screen")
        ##the below code assumes login screen is ready
        code=self.performLogin(username, passwd) 
        if(code==SerialHandler.WRITE_FAILED):
            self.trans_err_status=SerialHandler.WRITE_FAILED
            return
        elif(code==SerialHandler.LOGIN_FAILED):
            print("SERIAL_HANDLER Login failed, assuming the user knows what he is doing we would suggest to consider system unreponsive")
            self.trans_err_status=SerialHandler.LOGIN_FAILED
            return
        elif(code==SerialHandler.UNEXPECTED_RESPONSE):
            print("SERIAL_HANDLER Unexpected response on login attempt, assuming the user knows what he is doing we would suggest to consider system unreponsive")
            self.trans_err_status=SerialHandler.UNEXPECTED_RESPONSE
            return
        
        ##asume login has succedded
        code=self.sendCMD(cmd, waitTime)
        if(code==SerialHandler.WRITE_FAILED):
            self.trans_err_status=SerialHandler.WRITE_FAILED
            return
        self.trans_output=self.read()
        self.sendCMD("exit", waitTime, flushPreviousInput)
        if(code==SerialHandler.WRITE_FAILED):
            self.trans_err_status=SerialHandler.WRITE_FAILED
            return
        if(self.isSerialResponsive()):
            return
        else:
            self.trans_err_status=SerialHandler.WRITE_FAILED;
            return 
                
    def getTransErrStatus(self):
        return self.trans_err_status
    
    def getTransOutput(self):
        return self.trans_output
    
    def sendCMD(self,cmd,waitTime=1,flushPreviousInput=True):
        if(flushPreviousInput):
            self.ser.flushInput()
        try:
            self.ser.write((cmd+ '\r\n').encode())
        except serial.SerialTimeoutException as e:
            traceback.print_exc()
            #self.bugFix()
            return SerialHandler.WRITE_FAILED
        except serial.SerialException as e:
            traceback.print_exc()
            #self.bugFix()
            return SerialHandler.WRITE_FAILED
        time.sleep(waitTime) #just give time to device to respond
        return SerialHandler.WRITE_SUCCESS
    
    def bugFix(self):
        import os
        devConPath="C:/Users/admin/Downloads/DevCon/amd64"
        usbHwid="@FTDIBUS\\VID_0403+PID_6001+A501JS9EA\\0000"
        toExecute="cd "+str(devConPath)+" && devcon.exe disable " + "\"" + str(usbHwid)+ "\""+ " PING 1.1.1.1 -n 1 -w 2000  > NULL   && devcon.exe enable "+ "\"" + str(usbHwid) + "\""+ " && PING 1.1.1.1 -n 1 -w 2000  > NULL"
        os.system(toExecute)
        
    def read(self):  #return response as string       
        try:
            out=None
            if(self.ser.in_waiting<=0):
                return out
        except SerialException as e:
            traceback.print_exc()
            #self.bugFix()
            
            
            return None
            
        while self.ser.in_waiting> 0:
            try:
                if (out==None):
                    out = self.ser.read(1)
                else:
                    out += self.ser.read(1)
            except SerialTimeoutException as e:
                traceback.print_exc()
                if(out!=None):
                    try:
                        out=out.decode("utf-8")
                    except UnicodeDecodeError as er:
                        traceback.print_exc()
                        print(str(er))
                        out=None
                #else:
                    #self.bugFix()
                return out
        try:    
            out=out.decode("utf-8")
        except UnicodeDecodeError as er:
            traceback.print_exc()
            #self.bugFix()
            print(str(er))
            out=None
        
        return out
    
    def isLoginScreenReady(self):
        try:
            self.sendCMD("\n")
            ser_response=self.read()
            print("empeik6")
        except serial.serialutil.SerialException as e:
            #self.bugFix()
            return False
        if(None == ser_response):
            print("SERIAL_HANDLER login screen not ready")
            return False
        else:
            print("empeik5")
            if ("xg2-1 login:" in ser_response or "juno_uni login:" in ser_response or "xg3 login:" in ser_response or "root@juno_uni:~#" in ser_response or "root@genericarmv8:~#" in ser_response):
                print("empeik7")
                return True
            else:
                print("empeik8")
                return False
    
    def reachLoginScreenFromResponsiveSystem(self):
        print("empeika31")
        self.sendCMD("exit",SerialHandler.REACH_LOGIN_SCREEN_TIMEOUT)
        print("empeika31")
        ser_response=self.read()
        if ser_response is None:
            return SerialHandler.FAIL
        if("xg2-1 login:" in ser_response or "juno_uni login:" in ser_response or "xg3 login:" in ser_response or "root@juno_uni:~#" in ser_response or "root@genericarmv8:~#" in ser_response):
            return SerialHandler.SUCCESS
        return SerialHandler.FAIL
    
    def isSerialResponsive(self,timeout=2):
        code=self.sendCMD("\n",timeout)
        if(code==SerialHandler.WRITE_FAILED):
            return False;
        ser_response=self.read()
        if(None == ser_response):
            print("SERIAL_HANDLER serial unresponsive")
            return False
        else:
            print("SERIAL_HANDLER serial responded with "+str(ser_response).replace("\n"," "))
            return True
    
    def hasBootedSuccesfully(self,lookFor="xg2-1 login:"):
        try:
            
            ser_response=self.read()
            if(ser_response!=None):
                print("OUTPUT "+str(ser_response))
            if(ser_response!= None and lookFor in ser_response):
                return True
            return False
        except serial.SerialTimeoutException as e:
            #self.bugFix()
            traceback.print_exc()
            return False
        except serial.SerialException as e:
            #self.bugFix()
            traceback.print_exc()
            return False
        
    def performLogin(self,username,passwd,timeout=LOGIN_STEPS_TIMEOUT):
        print("empeika31Login")
        self.sendCMD(username,timeout)
        print("empeika31NoTimeout")
        ser_response=self.read()
        if(None == ser_response):
            print("SERIAL_HANDLER loginFailed system unresponsive")
            return SerialHandler.WRITE_FAILED
        else:
            if ("Password:" in ser_response or True): #aproxe remove true
                self.sendCMD(passwd,timeout)
                ser_response=self.read()
                if(None == ser_response):
                    print("SERIAL_HANDLER loginFailed system unresponsive")
                    return SerialHandler.WRITE_FAILED
                else:
                    if("xg2-1 login:" in  ser_response or "juno_uni login:" in ser_response or "xg3 login:" in ser_response ): ##STILL ASK FOR LOGIN WRONG PASSWORD
                        print("SERIAL_HANDLER loginFailed")
                        return SerialHandler.LOGIN_FAILED
            else: 
                print("SERIAL_HANDLER unexpected string password was expected")
                return SerialHandler.UNEXPECTED_RESPONSE
        return SerialHandler.WRITE_SUCCESS

    def close(self):
        self.ser.close()
    
    def openSerial(self):
        #self.baudrate=115200
        #self.port=port
        #self.timeout=SerialHandler.UNRESPONSIVE_TIMEOUT
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(port=self.port,baudrate=self.baudrate,timeout=self.timeout)
        self.ser.write_timeout=SerialHandler.UNRESPONSIVE_TIMEOUT
        if (self.ser.is_open==False):
            print("failed to open port")
            exit(1)
        self.trans_err_status=None 
        self.trans_output=None 

def test():
       
    serialHandler = SerialHandler ()
    #serialHandler.performLogin("zhadji01","agoodpasswd")
    #serialHandler.sendCMD("taskset -c 0 /home/zhadji01/stress_tests/iplusplus 10000000000000 &")
    while True:
        serialHandler.sendCMD("cat /home/zhadji01/chf_helper_tmp/workload_status",waitTime=2)    
        ser_out=serialHandler.read()
        
        lines=ser_out.split("\n")
        count_of_lines=0
        for line in lines:
            if "WORKLOAD_SCRIPT" in line:
                count_of_lines=count_of_lines+1
                print(line)
        print(str(count_of_lines))
        exit(1)
        #count=0
        
        print("NEW ROUNDDDDDDDDDDDDDDDDDD")
        found=False
        for line in ser_out.split("\n"):
            print(line)
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
                            print("exit signal is "+str(tmp[i+1]))
                            found=True
                            break
                #count=count+1
        time.sleep(2)
    exit(1)
    
    if serialHandler.isSerialResponsive()==True:
        if serialHandler.isLoginScreenReady():
            code=serialHandler.performLogin("root", "root")
            if(code==SerialHandler.WRITE_FAILED):
                print("System unresponsive")
            elif(code==serialHandler.LOGIN_FAILED):
                print("Login failed")
            elif(code==serialHandler.UNEXPECTED_RESPONSE):
                print("trying to logout with exit")
                serialHandler.sendCMD("exit")
                ser_reponse=serialHandler.read()
                print(ser_reponse.decode("utf-8"))
            else:
                serialHandler.sendCMD("ls")
                ser_reponse=serialHandler.read()
                serialHandler.sendCMD("exit")
                ser_reponse=serialHandler.read()
                print(ser_reponse)
        else:
            
            tries=0
            while (tries<4):
                code=serialHandler.reachLoginScreenFromResponsiveSystem()
                if(code==SerialHandler.SUCCESS):
                    
                    break;
                tries=tries+1
            if(tries>=4):
                print("Failed to reach login screen")
            else:
                print("Succesfully reached login screen")
#test()