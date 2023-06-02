'''
Created on 15 Jun 2017

@author: zachad01
'''
from setVoltageThroughSerial import setVoltage
from setFrequencyThroughSerial import setFrequency
from sendRebootCommand import sendRebootCommand
import sys
#from setFrequencyThroughDebugger import setFrequency

SCRIPTS_BASE="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/"
SET_FREQUENCY_BAT="RUN_DS5_changeFreq.bat"
SET_FREQUENCY_PY="changeFrequency.py"

#frequency=1284 #in MHZ
#frequency=1200
#frequency=1200
if len(sys.argv)!=4:
    print("enter vol com as arguments e.g. 0.8 COM7 deviceNumber(1 for A72 2 for A53)")
    sys.exit()

setVoltage(int(sys.argv[3]), float(sys.argv[1]), sys.argv[2])
#setFrequency(1200, portCOM="COM7", multiplier=20, supply=7)
#sendRebootCommand("COM7")
#setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)

