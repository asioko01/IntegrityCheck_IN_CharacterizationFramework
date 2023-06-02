'''
Created on 15 Jun 2017

@author: zachad01
'''

###EXAMPLE COMMAND FOR
##CORTEX-A72 setFrequencyTo1200 1200 20 7 COM7 
####CORTEX-A53 setFrequencyTo600 600 16 6 COM7
####SYS_REF_CLK setFrequencyTo1600 1600 32 0 COM7

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
if len(sys.argv)!=5:
    print("enter frequency multiplier supply com as arguments e.g. 1200 20 7 COM7")
    sys.exit()
#setVoltage(1, float(sys.argv[1]), sys.argv[2])
freq=int(sys.argv[1])
multiplier=int(sys.argv[2])
supply=int(sys.argv[3])
com=sys.argv[4]
print(str(freq)+" "+str(com)+" "+str(multiplier)+" "+str(supply))
setFrequency(freq, portCOM=com, multiplier=multiplier, supply=supply)
#sendRebootCommand("COM7")
#setFrequency(frequency,SCRIPTS_BASE+SET_FREQUENCY_PY,SCRIPTS_BASE+SET_FREQUENCY_BAT)

