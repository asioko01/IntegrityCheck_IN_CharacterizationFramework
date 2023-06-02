'''
Created on 14 Jun 2017

@author: zachad01
'''
import serial
import time

def sendRebootCommand(comID):

    ser = serial.Serial(comID)
    ser.baudrate=115200
    ser.timeout=3
    
    ser.write("\n".encode())
    while(True):
        line=str(ser.readline())
        print(line)
        if("Cmd>" in line):
            break;
        if("Debug>" in str(line)):
            while True:
                ser.write("exit\n".encode())
                line=ser.readline()
                print(line),;
                if("Cmd>" in str(line)):
                    break;
            break;
    print("Rebooting system\n")
    while True:
        ser.write("REBOOT\n".encode())
        line=str(ser.readline())
        if("Rebooting" in line):
            break;
    time.sleep(2)
    ser.close()
    print("reboot command has been issued successfully")