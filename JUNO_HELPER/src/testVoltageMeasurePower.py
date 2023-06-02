'''
Created on 15 Jun 2017

@author: zachad01
'''
from setVoltageThroughSerial import setVoltage
from setFrequencyThroughSerial import setFrequency
from sendRebootCommand import sendRebootCommand
from readPowerSerial import readPower
#from setFrequencyThroughDebugger import setFrequency

SCRIPTS_BASE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/"
SET_FREQUENCY_BAT="RUN_DS5_changeFreq.bat"
SET_FREQUENCY_PY="changeFrequency.py"

#frequency=1284 #in MHZ
#frequency=1200
#frequency=300
domain=1
com="COM8"
vols = [0.83,0.85]
tries=5
for vol in vols:
    readings=[]
    setVoltage(domain,vol, com)
    for reading in range(tries):
        power=readPower(com,"w",domain,False)
        readings.append(float(power))
        #print(str(power))
    print(str(vol)+" "+str(sum(readings)/len(readings)))

#setVoltage(1, 0.9, "COM7")
#setFrequency(frequency, portCOM="COM7", multiplier=20, supply=7)
#sendRebootCommand("COM11")
#setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)