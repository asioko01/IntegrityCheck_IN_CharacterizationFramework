'''
Created on 12 Φεβ 2019

@author: admin
'''
import jsonpickle
from InputTop import InputTop
from GeneralInput import GeneralInput
from ExperimentInput import ExperimentInput
from Workload import Workload
from Topology import Topology
from random import Random
from InputGenerator import activeCoresToTopology
from WorseCaseTopologyInstanceGenerator import WorseCaseTopologyInstanceGenerator


def getAllpossibleTopologies(totalPmds,totalCores,coresPerPMD):
    topologies=[]
    for activeCores in range(1,totalCores+1):
            maxfpmds=activeCores//coresPerPMD
            for fpmds in range(0,maxfpmds+1):
                hpmds=activeCores-(coresPerPMD*fpmds)
                if((hpmds+fpmds)>totalPmds):
                    continue
                else: 
                    topologies.append(Topology(totalPmds,totalCores,coresPerPMD,fpmds,hpmds))
    return topologies
            
                

def generateAllInstances(total_cores,total_pmds,coresPerPMD):
    activeCoresToTopology=[]
    instances=Topology.getAllInstancesStatic(total_cores, total_pmds, coresPerPMD)
    for instance in instances:
        topology = Topology.returnTopology(instance, total_pmds, total_cores, coresPerPMD)
        toAdd = (instance,topology)
        activeCoresToTopology.append(toAdd)
    return activeCoresToTopology


##VARIABLES
targetHostName="10.16.20.162"
targetSSHusername="root"
targetSSHpassword="root"
    
sysLogParsingScript="/home/root_desktop/chf_scripts/printErrorsWithinTimestamps"
helperScriptSetup="/home/root_desktop/chf_scripts/chf_helper_freq_taskset.sh"

workloadStatusOutput="/home/root_desktop/chf_scripts/chf_tmp/workload_status"
serialPort="COM12"
mongoDB="longTests"
mongoCol="xg3EmvirusCharWorstCaseTopologyInstances"
measurePowerScript = "/home/root_desktop/chf_scripts/chf_measure_power.sh"
platform=4
online_offline_cores=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
repetitions=1
run_type="all"
vol_inc=10
inc_wait_time=10
vmin_component="CORE"
nominalVol=820



totalPmds=16
totalCores=32
coresPerPMD=2


core_vmin=[]
with open('./core_vmin.txt') as f:
    lines = f.readlines()
index=0
for line in lines:
    vmin=int(line)
    core=index
    core_vmin.append(([core],vmin))
    index=index+1

pmd_vmin=[]
with open('./pmds_vmin.txt') as f:
    lines = f.readlines()
index=0
for line in lines:
    vmin=int(line)
    core1=index
    core2=index+1
    pmd_vmin.append(([core1,core2],vmin))
    index=index+2

knownTopologies = getAllpossibleTopologies(totalPmds, totalCores, coresPerPMD)
worstCaseGenerator = WorseCaseTopologyInstanceGenerator(pmd_vmin,core_vmin)

topologyToActiveCores={}


for knownTopology in knownTopologies:
    worseMapping=worstCaseGenerator.findWorseCaseTopologyInstance(knownTopology)
    topologyToActiveCores[knownTopology]=worseMapping


run_timeout=500
helperScriptWorkload="/home/root_desktop/chf_scripts/chf_helper_virus.sh"


jsonFileName="xg3WorstCaseTopology.json"
#END OF VARIABLES

generalInput = GeneralInput(targetHostName,targetSSHusername,targetSSHpassword,sysLogParsingScript,helperScriptSetup,helperScriptWorkload,workloadStatusOutput,serialPort,mongoDB,mongoCol,measurePowerScript)
experiments=[]

for knownTopology in knownTopologies :
    
    activeCores=topologyToActiveCores[knownTopology]
   
    #set frequencies
    core_to_freq=[]
    for core in range(totalCores):
        core_to_freq.append(375)
        
    for core in activeCores:
        core_to_freq[core]=3000
        if core % 2 == 0:
            core_to_freq[core+1]=3000
        else:
            core_to_freq[core-1]=3000
    
    workloads=[]
    workloads.append(Workload.dIdTvirusWorkloadGeneratorXG3(activeCores))
                         
    startVol = nominalVol
    endVol=750
    experiment = ExperimentInput(workloads,platform,online_offline_cores,core_to_freq,repetitions,run_type,startVol,endVol,vol_inc,inc_wait_time,vmin_component,run_timeout)
    experiments.append(experiment)
    
out_file = open(jsonFileName,'w')    
inputTop = InputTop(generalInput,experiments)
frozen = jsonpickle.encode(inputTop,unpicklable=False)
out_file.write(frozen)
