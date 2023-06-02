'''
Created on 15 Μαΐ 2017

@author: admin
'''
import traceback
import time
import datetime
from time import struct_time



def getBinaryStringOfInt(anInteger):
    withoutZeroes=bin(anInteger)[2:]
    zeroesToAdd=32-len(withoutZeroes)
    toReturn=""
    for i in range(zeroesToAdd):
        toReturn=toReturn+"0"
    toReturn=toReturn+withoutZeroes
    return toReturn

def getNextOf(tokens,prevToken):
    try:
        i=0
        for i in range (len(tokens)):
            if(tokens[i]==prevToken):
                return tokens[i+1]
            i=i+1
    except(IndexError) as e:
        print(str(e.print_stack_trace()))
        raise IndexError("index error in getNextOf Utilites function")

        
def getTimestampInSecs(date_str,year=None):
    try:
        if(year is None):
            year=datetime.datetime.now().year
        #date_str="May 15 13:26:53"
        tokens= date_str.split(" ")
        month_str=tokens[0].upper()
        day=int(tokens[1])
        time_str=str(tokens[2])
        
        
        
        if month_str == "JAN":
        
            mnumber=1
        
        elif month_str=="FEB":
        
            mnumber=2;
        
        elif month_str=="MAR":
        
            mnumber=3;
        
        elif month_str=="APR":
        
            mnumber=4;
        
        elif month_str=="MAY":
        
            mnumber=5;
        
        elif month_str=="JUN":
        
            mnumber=6;
        
        elif month_str=="JUL":
        
            mnumber=7;
        
        elif month_str=="AUG":
        
            mnumber=8;
        
        elif month_str=="SEP":
        
            mnumber=9;
        
        elif month_str=="OCT":
        
            mnumber=10;
        
        elif month_str== "NOV":
        
            mnumber=11;
        
        elif month_str == "DEC":
        
            mnumber=12;
         
            
        tokens= time_str.split(":")
        hours=int(tokens[0])
        minutes=int(tokens[1])
        secs=int(tokens[2])
        
        #time_struct=struct_time()
        #time_struct.tm_year=year
        #time_struct.tm_mon=mnumber
        #time_struct.tm_mday=day
        #time_struct.tm_hour=hours
        #time_struct.tm_min=minutes
        #time_struct.tm_sec=secs
        #time_struct
        t=(year,mnumber,day,hours,minutes,secs,0,0,-1)
        timestamp = int(time.mktime(t))
        return timestamp
    except(IndexError,ValueError) as e:
        #print(str(e.print_stack_trace()))
        traceback.print_exc()
        raise Exception("index or value error in getTimestampInSec Utilites function")


#tmp=getBinaryStringOfInt(10)
#print(tmp)