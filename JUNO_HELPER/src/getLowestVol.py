'''
Created on 14 Jun 2017

@author: zachad01
'''
import os
import fileinput

##if many reps specified returns an average value
def getLowestVol(scriptPath="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS",
                 scriptName="RUN_DS5_lowestVol.bat",lastMeasFile="C:/Users/admin/Desktop/liClipseWorkspace/JUNO_SW/DS5_SCRIPTS/tmp",reps=1):

    if os.path.exists(lastMeasFile):
        os.remove(lastMeasFile)
    
    #os.system("cd \"C:/Users/zachad01/My Documents/LiClipse Workspace/JUNO_SW/DS5_SCRIPTS\" && RUN_DS5_lowestVol.bat && exit")
    values=[]
    for rep in range(reps):
        while os.path.exists(lastMeasFile)==False:
            system_command="cd "+str("\"")+scriptPath+str("\"")+" && "+scriptName+" && exit"
            #print(system_command)
            os.system(system_command)
        
        for line in fileinput.input(lastMeasFile):
            values.append(int(line))
            break
        fileinput.close()
    
    avg=float(sum(values))/len(values)
    return avg

#getLowestVol()