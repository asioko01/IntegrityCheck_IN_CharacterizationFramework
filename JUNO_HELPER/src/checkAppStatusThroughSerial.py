'''
Created on 9 Jun 2017

@author: zachad01
'''

import fileinput
import serial
import sys
import re

def checkAppStatus(command,portCOM):# for a57/a72 supply = 1 
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = portCOM
    ser.timeout = 2
    inp=0
    #print ser
    
    if(ser.open()==False):
        print (ser.isOpen())
        print ("Can't open serial port")
        sys.exit()
           
    #ser.write("help\n")
    
    
    '''
    # look for command prompt
    breakLoop=False
    while breakLoop==False:
        ser.write(str.encode(command+"\n"))
        print(ser.readline())                    # not interested in reading back what I wrote
        for i in range(10):
            inp = ser.readline()
            if(re.match(r'Debug>',inp.decode())):
                #print "found prompt"
                breakLoop=True
                break
            else:
                #print "looking for prompt: "+inp
                if(i==9):
                    print ("Error: Could not get prompt\n")
    '''
                    #continue
    ser.write(str.encode(command+"\n\n"))
    inp = ser.readline()
    print("input:"+str(inp))              
    ser.close()
    if(ser.isOpen()==True):
        print (ser.isOpen())
        print ("Can't close serial port")
        sys.exit()
    return inp
appcommand="/media/oldDisk1/root/benchmarks/a53emVirusGood/appcrashcheck.sh"
checkAppStatus(appcommand,"COM17")