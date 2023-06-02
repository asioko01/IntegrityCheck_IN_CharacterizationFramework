'''
Created on 15 Jun 2017

@author: zachad01
'''
from setVoltageThroughSerial import setVoltage
from setFrequencyThroughSerial import setFrequency
from sendRebootCommand import sendRebootCommand
from readPowerSerial import readPower
from getLowestVol import getLowestVol
#from setFrequencyThroughDebugger import setFrequency

SCRIPTS_BASE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/"
SET_FREQUENCY_BAT="RUN_DS5_changeFreq.bat"
SET_FREQUENCY_PY="changeFrequency.py"

#frequency=1284 #in MHZ
#frequency=1200
#frequency=300
#while True:
#    power=readPower("COM8","w",1,False)
#    print(str(power))

#getLowestVol()
while True:
    power=readPower("COM8","w",1,False)
    print(str(power))
#setVoltage(1, 0.9, "COM7")
#setFrequency(frequency, portCOM="COM7", multiplier=20, supply=7)
#sendRebootCommand("COM11")
#setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)

