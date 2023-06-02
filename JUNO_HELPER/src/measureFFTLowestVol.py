'''    
Created on 20 Ιουν 2017

@author: admin
'''

from fft import  fftwrapper
from readFile import readFile
from executeCommandSSH import executeCommand
from getVoltageFromSram import getMvFromSRAM
from getLowestVol import getLowestVol
import sys
import time
import argparse

file=str(time.strftime("%Y%m%d-%H%M%S"))
endSample=None
printFrequencies=True

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file",help="give output file")
parser.add_argument("-e","--endSample",type=int,help="give end fft sample")
parser.add_argument("-o","--omitFrequencies",type=int,choices=[0,1],help="choose if want to omit frequencies from fft")

args=parser.parse_args()
if args.file:
    file=args.file
if args.endSample:
    endSample=args.endSample
if args.omitFrequencies:
    if args.omitFrequencies==1:
        printFrequencies=False

fout=open(file,'w')

##inputs
#commandToExecute="taskset -c 4 /media/oldDisk1/root/benchmarks/em@72MHz/em72MHz &> /dev/null & exit"
timestep=1/float(1600)
#commandToKill="pkill em72MHz; exit"
##eo inputs

#executeCommand(command=commandToExecute)
lowestVol=getLowestVol()
values=getMvFromSRAM()
freqToAmp=fftwrapper(values, timestep,endSample=endSample,printFrequencies=printFrequencies)
#executeCommand(command=commandToKill)

print(freqToAmp)
print("\n")
print(str(lowestVol)+"\n\n")
print(str(values))


fout.write(freqToAmp)
fout.write("\n")
fout.write(str(lowestVol)+"\n\n")
#fout.write(str(values))
for value in values:
    fout.write(str(value)+"\n")
fout.write("\n")
fout.close()
