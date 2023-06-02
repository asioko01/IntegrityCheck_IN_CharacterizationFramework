'''
Created on 12 Φεβ 2019

@author: admin
'''

class GeneralInput:
    '''def __init__(self):
        self.targetHostName=None
        self.targettSSHusername=None
        self.targetSSHpassword=None
        self.sysLogParsingScript=None
        self.helperScriptSetup=None
        self.helperScriptWorkload=None
        self.workloadStatusOutput=None
        self.serialPort=None
        self.mongoDB=None
        self.mongoCol=None
        self.measurePowerScript=None
        self.experiments=None'''
    
    def __init__(self,targetHostName,targetSSHusername,targetSSHpasword,sysLogParsingScript,helperScriptSetup,helperScriptWorkload,
                 workloadStatusOutput,serialPort,mongoDB,mongoCol,measurePowerScript):
        
        self.targetHostName=targetHostName
        self.targetSSHusername=targetSSHusername
        self.targetSSHpassword=targetSSHpasword
        self.sysLogParsingScript=sysLogParsingScript
        self.helperScriptSetup=helperScriptSetup
        self.helperScriptWorkload=helperScriptWorkload
        self.workloadStatusOutput=workloadStatusOutput
        self.serialPort=serialPort
        self.mongoDB=mongoDB
        self.mongoCol=mongoCol
        self.measurePowerScript=measurePowerScript
    
        
        