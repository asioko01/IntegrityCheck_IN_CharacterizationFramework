'''
Created on 12 Φεβ 2019

@author: admin
'''
from JSONoutputObjectDefinitions import pmd_error
from random import Random
from tkinter.constants import CURRENT
from serial.rfc2217 import ACTIVE

class Topology:
    
    def __init__(self,total_pmds,total_cores,coresPerPMD,fpmds,hpmds):
        self.total_pmds=total_pmds
        self.total_cores=total_cores
        self.coresPerPMD=coresPerPMD
        self.fpmds=fpmds
        self.hpmds=hpmds
        self.active_cores=self.activeCores() #to be used for sorted function
        
    @staticmethod
    def returnTopology(active_cores,total_pmds,total_cores,coresPerPMD):
        hpmds=0
        fpmds=0
        for coreID in range(0,total_cores,2):
            if (coreID in active_cores) and ((coreID+1) in active_cores): 
                fpmds=fpmds+1
            elif ((coreID in active_cores) or (coreID+1) in active_cores):
                hpmds=hpmds+1
        top = Topology(total_pmds,total_cores,coresPerPMD,fpmds,hpmds)
        return top

    @staticmethod
    def getAllInstancesStatic(total_cores,total_pmds,coresPerPMD): 
        instances=[]
        for active_cores in range(1,total_cores+1):
            currentCombination=[]
            Topology.__getAllInstancesHelper__(instances, currentCombination, 0, 0, None,total_cores,total_pmds,coresPerPMD,active_cores)
        return instances

    @staticmethod 
    def getOnlyCoreAndPMDs(total_cores):
        instances=[]
        for core in range(0,total_cores):
            currentInstance=[]
            currentInstance.append(core)
            instances.append(currentInstance)
            if (core % 2) == 0:
                currentInstance=[]
                currentInstance.append(core)        
                currentInstance.append(core+1)
                instances.append(currentInstance)            
        return instances
    
    def getAllInstances(self):
        instances=[]
        currentCombination=[]
        Topology.__getAllInstancesHelper__(instances, currentCombination, 0, 0, self,self.total_cores,self.total_pmds,self.coresPerPMD,self.activeCores())
        return instances
    
    @staticmethod    
    def __getAllInstancesHelper__(instances,currentCombination,iteration,depth,topologyToReturn,total_cores,total_pmds,coresPerPMD,activeCores):
        if depth==activeCores:
            newList = currentCombination.copy()
            newListTopology = Topology.returnTopology(newList,total_pmds,total_cores,coresPerPMD)
            if topologyToReturn is None : #check if instance of the current topology
                instances.append(newList)
            elif topologyToReturn is not None and topologyToReturn == newListTopology: 
                instances.append(newList)
            return
        else:
            i = iteration
            end = total_cores - (activeCores-depth) +1
            for i in range(i,end):
                currentCombination.append(i)
                Topology.__getAllInstancesHelper__(instances, currentCombination, i + 1, depth + 1,topologyToReturn,total_cores,total_pmds,coresPerPMD,activeCores)
                currentCombination.pop()
    
    def activeCores (self):
        return self.fpmds*2 +self.hpmds
    
    def getFps(self):
        return self.fpmds
    
    def getHps(self):
        return self.hpmds
    
    def randomPickCores(self,random=Random()):
        if self.fpmds==0 and self.hpmds==0 or (self.total_cores==0 or self.total_pmds==0 or self.coresPerPMD==0):
            import sys
            print("Error topology not initialized")
            sys.exit(1)
        #tmpList=[]
        #for coreID in range(0,self.total_cores):
        #    tmpList.append(coreID)
        
        fpmdsFilled=0
        pmdsToReturn=[]
        while fpmdsFilled < self.fpmds:
            pmdid = random.randint(1,self.total_pmds)
            if pmdid not in pmdsToReturn:
                pmdsToReturn.append(pmdid)
                fpmdsFilled=fpmdsFilled+1
        
        toReturn=[]  
        for pmdid in pmdsToReturn:
            tmp=pmdid*2
            firstCore=tmp-1
            secondCore=tmp-2
            toReturn.append(firstCore)
            toReturn.append(secondCore)
         
        hpmdsFilled=0
        while hpmdsFilled < self.hpmds:
            hpmdId= random.randint(0,self.total_cores-1)
            if hpmdId not in toReturn:
                toReturn.append(hpmdId)
                hpmdsFilled=hpmdsFilled+1
             
        toReturn.sort()
        if len(toReturn) != self.activeCores():
            import sys
            print("Assertion in RandomPickcores")
            sys.exit(1)
       
        return toReturn

    def __str__(self):
        return str(self.fpmds)+"fp"+str(self.hpmds)+"hp"
    
    def __hash__(self):
        return hash(self.fpmds+self.hpmds)
    
    def __eq__(self, other):    
        return (self.fpmds==other.fpmds
                and
                self.hpmds==other.hpmds
                and
                self.total_pmds==other.total_pmds
                and
                self.total_cores==other.total_cores
                and
                self.coresPerPMD==other.coresPerPMD)
    
   
    
    '''def doBelongToSamePMD(self,a,b): #assuming adjastent cores belong to the same pmd
        if (  ((a-b) == 1) and ((a%2)==1) and ((b%2)==0) ):
        
            return True
        
        elif (  ((b-a) == 1) and ((b%2)==1) and ((a%2)==0) ):
        
            return True
        
        return False
    '''
    