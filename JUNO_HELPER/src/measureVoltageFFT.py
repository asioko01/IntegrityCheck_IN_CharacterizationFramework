'''
Created on 20 Ιουν 2017

@author: admin
'''

from fft import  fftwrapper
from readFile import readFile
from executeCommandSSH import executeCommand
from getVoltageFromSram import getMvFromSRAM

##inputs
#commandToExecute="taskset -c 4 /media/oldDisk1/root/benchmarks/em@72MHz/em72MHz &> /dev/null & exit"
timestep=1/float(1600)
#commandToKill="pkill em72MHz; exit"
##eo inputs

#executeCommand(command=commandToExecute)
values=getMvFromSRAM()
maximum=max(values)
minimum=min(values)
ptp=maximum-minimum
print(str(max)+" "+str(min)+str(ptp))

fftwrapper(values, timestep)
#executeCommand(command=commandToKill)
