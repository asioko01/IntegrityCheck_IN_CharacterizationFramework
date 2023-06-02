'''
Created on 20 Ιουν 2017

@author: admin
'''
import os
import fileinput

##if many reps specified returns an average value
def getMvFromSRAMtriggerOnLow(scriptPath="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS",
                 scriptName="RUN_DS5_measMVtriggerLowValue.bat",lastMeasFile="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/tmp"):

    if os.path.exists(lastMeasFile):
        os.remove(lastMeasFile)
    
    #os.system("cd \"C:/Users/zachad01/My Documents/LiClipse Workspace/JUNO_SW/DS5_SCRIPTS\" && RUN_DS5_lowestVol.bat && exit")
    values=[]

    while os.path.exists(lastMeasFile)==False:
        system_command="cd "+str("\"")+scriptPath+str("\"")+" && "+str("\"")+scriptName+str("\"")+" && exit"
        os.system(system_command)
        
    for line in fileinput.input(lastMeasFile):
        values.append(int(line))
        
    fileinput.close()
    
    return values

#getMvFromSRAM()
#getLowestVol()
    
