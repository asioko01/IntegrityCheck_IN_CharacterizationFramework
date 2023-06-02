'''
Created on Mar 2, 2017

@author: zhadji01
'''
from xml.dom import minidom
import traceback
from json_helper import *
from JSONoutputObjectDefinitions import *
from email.policy import default
import JSONoutputObjectDefinitions
from Workload import Workload
import json_helper

class Experiment:
    
    ##default values
    DEF_CMD_LINE="ls"
    DEF_START_VOL=980
    DEF_END_VOL=0
    DEF_VOL_INC=-10

    DEF_REP=1
    DEF_INC_WAIT=10
    DEF_TYPE="all"
    DEF_WORK_TYPE="singleThread"
    #DEF_INPUT_DEFAULT_FILE="C:/Users/Sugar/workspace_python/characterization_framework/inputs/xg2_normal_1dim.json"
    DEF_INPUT_DEFAULT_FILE="C:/Users/zhadji01/workspace/CharacterizationFramework/inputs/exampleInput.json"
    DEF_VM_FLAG=False
    ##end of default values
    
    ##static/global
    MAX_CORES=8
    
    RUN_TYPE_CRASH="crash"
    RUN_TYPE_ALL="all"

    def __init__(self,workloads,start_voltage,end_voltage,vol_inc,core_to_frequencies,repetitions,run_type,inc_wait_time=DEF_INC_WAIT,platform=None,core_vol=None,uncore_vol=None,vmin_component=None,run_timeout=None,reboot_on_emer=False,sets=1,onlineOfflineCores=[]):
        self.workloads=[]
        for workload in workloads:
            newWorkloadObject= Workload()
            newWorkloadObject.work_dir=workload["work_dir"]
            newWorkloadObject.cmd_line=workload["cmd_line"]
            newWorkloadObject.toKillName=workload["toKillName"]
            newWorkloadObject.conventionName=workload["conventionName"]
            newWorkloadObject.cores=workload["cores"]
            newWorkloadObject.originalOutput=workload["originalOutput"]
            newWorkloadObject.runOutput=workload["runOutput"]
            newWorkloadObject.type=workload["type"]
            newWorkloadObject.inputs=workload["inputs"]
            newWorkloadObject.VM=workload["VM"]
            newWorkloadObject.stdin=workload["stdin"]
            ##important assumption here.. reliability information if not measured is considered unknown..
            #for instance is a system crash prevented from reading sdc app crash etc then this infomration is considere unknown
            ##only mark something as sdc or crash if you are sure
            newWorkloadObject.sdc=None
            newWorkloadObject.crash=None
            newWorkloadObject.exitCode=None
            newWorkloadObject.executionTime=None
            self.workloads.append(newWorkloadObject)
        
        self.start_voltage=start_voltage
        self.end_voltage=end_voltage
        self.vol_inc=vol_inc
        self.core_to_frequencies=core_to_frequencies
        self.repetitions=repetitions
        self.run_type=run_type
        self.inc_wait_time=inc_wait_time
        ###stable factors
        self.platform=platform
        self.slimpro_version=None
        self.os_version=None
        self.tianocore_version=None
        self.dramVol=[]
        self.dramRefresh=None
        self.dramFrequency=None
        self.uncoreVol=uncore_vol
        self.uncoreFreq=None
        self.coreVol=core_vol
        self.vminComponent=vmin_component
        
        self.measuredCoreVol=None
        self.measuredUncoreVol=None
        ##end of stable factors
        
        self.tmpJsonOutput=None #for supporting warmup run
        
        self.run_timeout=run_timeout
        self.reboot_on_emer=reboot_on_emer
        # alex
        self.sets=sets
        # end of alex
        
        if str(platform) == "juno":
            Experiment.MAX_CORES=2
        elif str(platform) =="juno_a53":
            Experiment.MAX_CORES=4
        elif int(platform)==4:
            Experiment.MAX_CORES=32
        else:
            Experiment.MAX_CORES=8
        
        ##calculate idle cores ## the cores that will run the background and system jobs on safe frequency
        self.idle_cores=[]
        self.active_cores=[]
        for i in range(Experiment.MAX_CORES):
            self.idle_cores.append(i)
        
        for workload in self.workloads:
            for core in workload.cores:
                if int(core) in self.idle_cores:
                    self.idle_cores.remove(int(core))
                if core not in self.active_cores:
                    self.active_cores.append(core)
                    
        ###TODO FOR HANDLING PMDs. do not consider the brother of active core as idle.. TODO for different core layout different handling is needed            
        for core in self.active_cores:
            mod=core%2
            if(mod==0):
                core=core+1
            else:
                core=core-1
            if(core in self.idle_cores):
                self.idle_cores.remove(core)
        
        if len(self.idle_cores)==0: ##all cores active
            self.idle_cores=self.active_cores     ##in that case idle and active cores are one!!    
        ##end of calculate idle cores
        
        #self.cores=len(active_cores.split(","))
        #calculate irq affinity
        bitstring=""
        for i in range(self.MAX_CORES):
            bitstring+='0'
        for idle_core in self.idle_cores:
            new=list(bitstring);
            new[int(self.MAX_CORES-int(idle_core)-1)]='1';
            bitstring=''.join(new)
        self.smp_affinity='%08X' % int(bitstring,2)
        self.smp_affinity=str(self.smp_affinity).lstrip("0")
        #print(str(self.smp_affinity))
        ##end of calculate irq affinity
        
        #cmd
        self.prettyName=[]
        for workload in self.workloads:
            command_line=workload.cmd_line
            tmp=str(command_line.split("/")[-1])
            prettyName=tmp#process to pkill up to 15 chars
            if len(tmp)>15:
                prettyName=tmp[0:14]
            self.prettyName.append(prettyName)
        #end of cmd
        
        self.onlineOfflineCores=onlineOfflineCores
        self.customChar=False

    
    def jsonExpOutInit(self,jsonOutput):

        
        json_helper.__assignDefaultInputs__(jsonOutput) #TODO fix default inputs.. I mean do something that does not require change of source code
        
        ##calculate core_to_freq
        jsonOutput.core_to_freq=self.core_to_frequencies
        
        #intialize json output related to workload
        jsonOutput.workloads=[]
        jsonOutput.workload_num=len(self.workloads)
        for index in range(jsonOutput.workload_num):
            workload_json =  JSONoutputObjectDefinitions.workload()
            workload_json.cores=self.workloads[index].cores
            workload_json.name=self.workloads[index].conventionName
            workload_json.type=self.workloads[index].type
            workload_json.inputs=self.workloads[index].inputs
            workload_json.VM=self.workloads[index].VM
                     
            jsonOutput.workloads.append(workload_json)
    
    def __str__(self):
        return str(self.prettyName)+"_"+str(self.active_cores)+"_"+str(self.frequency)
    
    
    @staticmethod
    def covertJSONtoObject(data): ##expects json dictionary        

        #workloads,start_voltage,end_voltage,vol_inc,core_to_frequencies,repetitions,run_type,inc_wait_time=DEF_INC_WAIT
        try:
            start_voltage=data["start_voltage"];
            end_voltage=data["end_voltage"];
            vol_inc=data["vol_inc"]
            core_to_frequencies=data["core_to_freq"]
            repetitions=data["repetitions"]
            run_type=data["run_type"]
            workloads=data["workloads"]
        except (KeyError)as err:
            print(str(err))
            traceback.print_exc()
            exit()
        
        try:
            inc_wait_time=data["inc_wait_time"]
          
        except(KeyError):
            inc_wait_time=Experiment.DEF_INC_WAIT
        
        try:
            platform=data["platform"]
        except(KeyError):
            platform=None #we can live without platform input
        
        core_vol=None
        uncore_vol=None
        vmin_component=None
        try:
            core_vol=data["core_vol"]
        except(KeyError):        
            pass
        
        try:
            uncore_vol=data["uncore_vol"]
        except(KeyError):        
            pass
        
        try:
            vmin_component=data["vmin_component"]
            if vmin_component != "CORE" and vmin_component!="UNCORE":
                print("Please specify vmin_component. CORE or UNCORE.. Exitting")
                import sys
                sys.exit(1)
        except(KeyError):        
            print("Please specify vmin_component. CORE or UNCORE.. Exitting")
            import sys
            sys.exit(1)
            #pass
            
        run_timeout=None
        try:
            run_timeout=data["run_timeout"]
        except(KeyError):
            pass

        reboot_on_emer=False
        try:
            reboot_on_emer=data["reboot_on_emer"]
        except(KeyError):
            pass
        
        # alex
        sets=1
        try:
            sets=data["sets"]
        except(KeyError):
            pass
        # end of alex
        
        onlineOfflineCores=[]
        
        try:
            onlineOfflineCores=data["online_offline_cores"]
        except(KeyError):
            pass
        
        customCharFlag=False
        try:
            customCharFlag=data["custom_char"]
        except(KeyError):
            pass
        
        newRun=Experiment(workloads,start_voltage,end_voltage,vol_inc,core_to_frequencies,repetitions,run_type,inc_wait_time,platform=platform,core_vol=core_vol,uncore_vol=uncore_vol,vmin_component=vmin_component,run_timeout=run_timeout,reboot_on_emer=reboot_on_emer,sets=sets,onlineOfflineCores=onlineOfflineCores)
        
        if customCharFlag==True: #for specCharacterization
            newRun.setCustomChar()
        
        return newRun
    
    def setCustomChar(self): #for speCharacterization
        self.customChar=True
  
        