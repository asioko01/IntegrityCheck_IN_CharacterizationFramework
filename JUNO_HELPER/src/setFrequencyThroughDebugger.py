'''
Created on 9 Jun 2017

@author: zachad01
'''
import fileinput
import os

def __setFrequencyToSet__(freq,pathToFrequencyPyScript):
    for line in fileinput.input(pathToFrequencyPyScript,inplace=1):
                if "print(v.SCC_SET_FATL(MYNR=50,freq=" in line:
                    print("print(v.SCC_SET_FATL(MYNR=50,freq="+str(freq)+"))")
                else:
                    print(line,end="");
    fileinput.close()

def setFrequency(freq,pathToFrequencyPyScript,pathToFrequencyBatScript):
    __setFrequencyToSet__(freq=freq*2, pathToFrequencyPyScript=pathToFrequencyPyScript)
    os.system(str("\"")+pathToFrequencyBatScript+str("\""))