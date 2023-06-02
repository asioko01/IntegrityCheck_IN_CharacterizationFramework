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
commandToExecute="cd /home/zhadji01/ga; taskset -c 4 ./individual &>/dev/null &  taskset -c 5 ./individual &>/dev/null & exit"
timestep=1/float(1600)
commandToKill="pkill individual; exit"
##eo inputs

executeCommand(command=commandToExecute)
values=getMvFromSRAM()
fftwrapper(values, timestep)
executeCommand(command=commandToKill)
