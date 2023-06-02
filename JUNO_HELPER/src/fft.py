from numpy import fft
import numpy as np
from audioop import reverse


'''def fftwrapper(values,timestep):
    
    signal = np.array(values,dtype=float)
    fourier = fft.fft(signal)
    n = signal.size
    timestep = 1/float(1600)
    freqs = fft.fftfreq(n, d=timestep)
    samples=0
    for freq,coef in zip(freqs,fourier):
        samples=samples+1
        if samples > (len(values)/2): # dont plot the negative frequencies
            break
        print(str(freq)+" "+str(np.abs(coef)))'''

def fftwrapper(values,timestep=1/1600,endSample=None,printFrequencies=True):
    
    signal = np.array(values,dtype=float)
    fourier = fft.fft(signal)
    n = signal.size
    freqs = fft.fftfreq(n, d=timestep)
    samples=0
    toReturn=""
    for freq,coef in zip(freqs,fourier):
        samples=samples+1
        if samples > (len(values)/2): # dont plot the negative frequencies
            break
        if samples==1:
            continue
        if endSample is not None and samples>endSample:
            break
        if printFrequencies==True:
            toReturn+=(str(freq)+" "+str(np.abs(coef))+"\n")
            print(str(freq)+" "+str(np.abs(coef)))
        else:
            toReturn+=(str(np.abs(coef))+"\n")
            print(str(np.abs(coef)))
    return toReturn

def fftwrapperAproxe(values,timestep=1/1600,endSample=None,printFrequencies=True):
    signal = np.array(values,dtype=float)
    fourier = fft.fft(signal)
    n = signal.size
    freqs = fft.fftfreq(n, d=timestep)
    samples=0
    toReturn=""
    temp=[]
    for freq,coef in zip(freqs,fourier):
        
        samples=samples+1
        if samples > (len(values)/2): # dont plot the negative frequencies
            break
        if samples==1:
            continue
        if endSample is not None and samples>endSample:
            break
        if printFrequencies==True:
            #toReturn+=(str(freq)+" "+str(np.abs(coef))+"\n")
            if(freq>60 and freq<80):
                temp.append([freq,np.abs(coef)])
                #temp.append(str(np.abs(coef)))
            #print(str(freq)+" "+str(np.abs(coef)))
        else:
            toReturn+=(str(np.abs(coef))+"\n")
            print(str(np.abs(coef)))
    return temp

def getFFTfreqAmpPairs(values,timestep=1/1600,endSample=None): #returns an array of freq amp tuples
    
    signal = np.array(values,dtype=float)
    fourier = fft.fft(signal)
    n = signal.size
    freqs = fft.fftfreq(n, d=timestep)
    samples=0
    toReturn=[]
    for freq,coef in zip(freqs,fourier):
        samples=samples+1
        if samples > (len(values)/2): # dont plot the negative frequencies
            break
        if samples==1:
            continue
        if endSample is not None and samples>endSample:
            break 
        tup=(float(freq),np.abs(coef))
        toReturn.append(tup)
        #print(str(freq)+" "+str(np.abs(coef)))
  
    return toReturn

def getFFTPeakFreqAmp(values,topk=1): #expects an array of freq,amp tuples and returns the topK tuple with the highest amp
    from operator import itemgetter
    #valuesCopy=list(values) # to avoid mutating the caller's function values list
    valuesCopy=sorted(values,key=itemgetter(1),reverse=True)
    return valuesCopy[0:topk]

def triggerOnLowFFTreturnTok(topK=1,timestep=1/1600,endSample=200): # return topK frequencues amplitudes pairs    
    from getVoltagesTriggerOnLow import getMvFromSRAMtriggerOnLow
    topK=1
    values=getMvFromSRAMtriggerOnLow()
    freqAmpPairs=getFFTfreqAmpPairs(values, timestep=timestep, endSample= endSample)
    topKPairs=getFFTPeakFreqAmp(freqAmpPairs,topK)
    return topKPairs    