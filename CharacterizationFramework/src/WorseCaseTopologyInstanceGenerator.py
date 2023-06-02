'''
Created on 17 Μαΐ 2019

@author: admin
'''
import operator
from Topology import Topology

class WorseCaseTopologyInstanceGenerator(object):
    
    def __init__(self,pmd_vmin,core_vmin): #tuples of (coreIds,vmin)
        self.pmd_vmin=pmd_vmin
        self.core_vmin=core_vmin
        self.pmdsCoresSorted=[]
        for pv in self.pmd_vmin:
            self.pmdsCoresSorted.append(pv)
        for cv in self.core_vmin:
            self.pmdsCoresSorted.append(cv)
        self.pmdsCoresSorted.sort(key=operator.itemgetter(1),reverse=True)
    
    def findWorseCaseTopologyInstance(self,topology):
        fullPmdSpots=topology.getFps()
        halfPmdSpots=topology.getHps()
        filledFullPmdSpots=0
        filledHalfPmdSpots=0
        worseMapping=[]
        curIndex=0
        
        while filledFullPmdSpots<fullPmdSpots or filledHalfPmdSpots<halfPmdSpots:
            if curIndex>=len(self.pmdsCoresSorted):
                return None
            coreIds=self.pmdsCoresSorted[curIndex][0]
            curIndex=curIndex+1
            toAddFlag=True
            if len(coreIds)==1: #single core
                coreId=coreIds[0]
                if coreId in worseMapping:
                    toAddFlag=False
                if coreId % 2 ==0:
                    if (coreId+1) in worseMapping:
                        toAddFlag=False
                else:
                    if (coreId-1) in worseMapping:
                        toAddFlag=False
                if toAddFlag == True and (filledHalfPmdSpots<halfPmdSpots):
                    filledHalfPmdSpots=filledHalfPmdSpots+1
                    worseMapping.append(coreId)
            else: #pmd
                for coreId in coreIds:
                    if coreId in worseMapping:
                        toAddFlag=False
                        break
                if toAddFlag == True and (filledFullPmdSpots<fullPmdSpots):
                    filledFullPmdSpots=filledFullPmdSpots+1
                    worseMapping.extend(coreIds)
        worseMapping.sort()
        return worseMapping
             
                
                 
                