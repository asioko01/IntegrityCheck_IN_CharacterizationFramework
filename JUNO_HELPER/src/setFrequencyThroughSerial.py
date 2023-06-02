'''
Created on 9 Jun 2017

@author: zachad01
'''
import fileinput
import serial
import sys
import re
import time

def setFrequency(frequency,portCOM,multiplier=20,supply=7):# for a72 use 7 for sys use 0
    ref=frequency/multiplier
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
        ser.readline()                     # not interested in reading back what I wrote
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
                                
    newcmd = "cfg w osc mb 0 0 "+str(supply)+" "+str(ref)+" \n" # supply 6 a53 supply 7 a72 supply 8 GPU
    ser.write(str.encode(newcmd))
        
    
    # look for success message
    for i in range(10):
    
        inp = ser.readline()
        #(re.match(r'clock set ='),inp.decode())
        if('clock set =' in inp.decode()):
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