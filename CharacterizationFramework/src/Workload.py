'''
Created on May 4, 2017

@author: zhadji01
'''

class Workload(object): # Describing the workload that will be run
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #self.id=None
        self.work_dir=None
        self.cmd_line=None
        self.toKillName=None
        self.conventionName=None
        self.cores=None
        self.originalOutput=None
        self.runOutput=None
        self.type=None
        self.inputs=None
        self.VM=None
        self.exitCode=None
        self.sdc=None
        self.crash=None
        self.executionTime=None
        self.stdin=None
        self.qos=None
        
    @staticmethod    
    def workloadGenerator(work_dir,cmd_line,toKillName,conventionName,cores,originalOutput,runOutput,workloadtype,inputs,VM):
        workload = Workload()
        workload.work_dir=work_dir
        workload.cmd_line=cmd_line
        workload.toKillName=toKillName
        workload.conventionName=conventionName
        workload.cores=cores
        workload.originalOutput=originalOutput
        workload.runOutput=runOutput
        workload.type=workloadtype
        workload.inputs=inputs
        workload.VM=VM
        return workload
       
    
    @staticmethod
    def NASworkloadGenerator(toKillName,conventionName,cores,runOutput,inputs,VM):
        return Workload.workloadGenerator(".", "/home/zhadji01/scripts/run_NPB.sh "+ "/home/zhadji01/NPB3.3/NPB3.3-OMP/bin "+ toKillName +" " +str(len(cores)), toKillName, conventionName, cores, None,runOutput, "Multithreaded", inputs, VM)
    
    @staticmethod
    def SPEC2017rateWorkloadGenerator(toKillName,conventionName,cores,runOutput,inputs,VM):
        return Workload.workloadGenerator(".","/home/zhadji01/scripts/run_spec2017.sh /home/zhadji01/cpu2017 "+ toKillName+" "+str(len(cores)), toKillName,conventionName,cores, None, runOutput, "SingleThread", inputs, VM )
    
    @staticmethod
    def NASworkloadGeneratorXG3(toKillName,conventionName,cores,runOutput,inputs,VM):
        return Workload.workloadGenerator("/home/root_desktop", "/home/root_desktop/run_NPB.sh "+ "/home/root_desktop/NPB3.3/NPB3.3-OMP/bin "+ toKillName +" " +str(len(cores)), toKillName, conventionName, cores, None,runOutput, "Multithreaded", inputs, VM)
    
    @staticmethod
    def SPEC2017rateWorkloadGeneratorXG3(toKillName,conventionName,cores,runOutput,inputs,VM):
        return Workload.workloadGenerator("/home/root_desktop","/home/root_desktop/run_spec2017.sh /home/root_desktop/cpu2017 "+ toKillName+" "+str(len(cores)), toKillName,conventionName,cores, None, runOutput, "SingleThread", inputs, VM )
    
    @staticmethod
    def dIdTvirusWorkloadGeneratorXG3(cores):
        work_dir="/home/root_desktop/xg3tests/"
        toKillName="theVirus"
        
        originalOutput=None
        runOutput="/home/root_desktop/chf_scripts/chf_tmp/0_out"
        coreList=""
        inputs=None
        VM=False
        for core in cores:
            coreList=coreList+str(core)+","
        coreList=coreList[:-1]
        cmd_line="./tester.sh ./theVirus theVirus 300 "+coreList
        conventionName="theVirus"+"_"+coreList.replace(',', '')
        return Workload.workloadGenerator(work_dir, cmd_line, toKillName, conventionName, cores, originalOutput, runOutput, "singleThread", inputs, VM)
    
    @staticmethod
    def dIdTvirusWorkloadGenerator(cores):
        work_dir="/home/zhadji01/xg2DiDtViruses/"
        toKillName="theVirus"
        
        originalOutput=None
        runOutput="/ssd/zhadji01/chf_tmp/0_out"
        coreList=""
        inputs=None
        VM=False
        for core in cores:
            coreList=coreList+str(core)+","
        coreList=coreList[:-1]
        cmd_line="./tester.sh ./64multiplyStack/theVirus theVirus 300 "+coreList
        conventionName="theVirus"+"_"+coreList.replace(',', '')
        return Workload.workloadGenerator(work_dir, cmd_line, toKillName, conventionName, cores, originalOutput, runOutput, "singleThread", inputs, VM)
    
    def toHelperScript(self):
        command=""
        coresStr=""
        for core in self.cores:
            coresStr=coresStr+str(core)+","
        
        tmp=list(coresStr)
        tmp.pop()
        coresStr=''.join(tmp)
        
        #work_dir cmd_line (please without stdout stder redirections) toKillName conventionName cores originalOutputPath runOutputPath type
        command=command+self.work_dir+" "
        command=command+str("\"")+self.cmd_line+str("\"")+" "
        command=command+self.toKillName+" "
        command=command+self.conventionName+" "
        command=command+coresStr+" "
        command=command+str(self.originalOutput)+" "
        command=command+str(self.runOutput)+" "
        command=command+str(self.type)+" "
        if self.stdin==None:
            command=command+"null"
        else:
            command=command+str(self.stdin)
        return command
