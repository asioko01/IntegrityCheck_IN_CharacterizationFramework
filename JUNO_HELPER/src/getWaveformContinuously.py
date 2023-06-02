from getVoltageFromSram import getMvFromSRAM
import time
from fft import fftwrapper, fftwrapperAproxe
reps=1
timestep=1/float(1600)
values=[]
for rep in range(reps):
    values.append(getMvFromSRAM())
    time.sleep(1)
'''
for val in values:
    for i in val:
        print(i,end=' ')
    print()
'''
for val in values:
    temp=fftwrapperAproxe(val,timestep)
    for i in temp:
        print(i[0],i[1])
    #print(max(temp))
    #print()
 
    