'''
Created on 21 Μαρ 2018

@author: admin
'''
from fft import getFFTPeakFreqAmp
from fft import getFFTfreqAmpPairs
from fft import fftwrapper
from getVoltagesTriggerOnLow import getMvFromSRAMtriggerOnLow
from fft import triggerOnLowFFTreturnTok

topK=1
'''
values=getMvFromSRAMtriggerOnLow()
freqAmpPairs=getFFTfreqAmpPairs(values, timestep=1/1600, endSample= 200)
topKPairs=getFFTPeakFreqAmp(freqAmpPairs,topK)'''
topKPairs=triggerOnLowFFTreturnTok(topK=topK)
print(str(topKPairs[topK-1][0])+" "+str(topKPairs[topK-1][1]))