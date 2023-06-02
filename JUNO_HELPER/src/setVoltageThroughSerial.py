'''
Created on 9 Jun 2017

@author: zachad01
'''

import fileinput
import serial
import sys
import re

def setVoltage(supply,voltage,portCOM):# for a57/a72 supply = 1 
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = portCOM
    ser.timeout = 2
    #print ser
    
    if(ser.open()==False):
        print (ser.isOpen())
        print ("Can't open serial port")
        sys.exit()
           
    #ser.write("help\n")
    
    
    
    # look for command prompt
    breakLoop=False
    while breakLoop==False:
        ser.write(str.encode("debug\n"))
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
                    #continue
                                
    newcmd = "cfg w v db1 0 0 "+str(supply)+" "+str(voltage)+" \n"
    ser.write(str.encode(newcmd))
    
    #cfg w v db1 0 0 1 0.95      (sets A57=0.95V (0=SYS, 1=A57, 2=A53, 3=GPU))
    
    
    
    # look for success message
    for i in range(10):
        inp = ser.readline()
        if(re.match(r'SoC voltage '+str(supply)+' set =',inp.decode())):
            print (inp.decode().rstrip('\n'))
            #print "found prompt"
            break
        else:
            #print "looking for prompt: "+inp
            if(i==9):
                print ("Error: Could not get confirmation\n")
                sys.exit()
               

    # look for command prompt
    for i in range(10):
        inp = ser.readline()
        if(re.match(r'Debug>',inp.decode())):
            #print "found prompt"
            break
        else:
            #print "looking for prompt: "+inp
            if(i==9):
                print ("Error: Could not get prompt\n")
                sys.exit()
            

    ser.close()
    if(ser.isOpen()==True):
        print (ser.isOpen())
        print ("Can't close serial port")
        sys.exit()