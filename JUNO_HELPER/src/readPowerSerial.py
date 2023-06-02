'''
Created on 29 Αυγ 2018

@author: admin
'''
import fileinput
import serial
import sys
import re

def readPower(portCOM,metric,device,silent=False):# metric can be either V,I,TEMP,W,J device can be 1 for a72 2 for a53 3 for gpu
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = portCOM
    ser.timeout = 10
    
    if(ser.open()==False):
        print (ser.isOpen())
        print ("Can't open serial port")
        sys.exit()
            
    # look for command prompt
    breakLoop=False
    while breakLoop==False:
        ser.write(str.encode("debug\n"))
        ser.readline()                    # not interested in reading back what I wrote
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
                                
    newcmd = "cfg r "+ str(metric)+" "+"db1 0 0 "+str(device)+" \n"
    ser.write(str.encode(newcmd))
    
    #cfg w v db1 0 0 1 0.95      (sets A57=0.95V (0=SYS, 1=A57, 2=A53, 3=GPU))
    for i in range(10):
        inp = ser.readline()
        line=inp.decode()
        if('SoC ' in line):
            result=line.rstrip('\n').split(" ")[5]
            if (silent==True):
                print(str(result))
            ser.close()
            return result
    
    ser.close()
    return -1