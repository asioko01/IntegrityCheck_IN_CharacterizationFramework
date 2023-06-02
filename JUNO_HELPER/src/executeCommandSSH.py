'''
Created on 20 Ιουν 2017

@author: admin
'''
from paramiko import SSHClient, client
from pip._vendor.colorama.ansi import Back

def executeCommand(hostname="juno_uni.in.cs.ucy.ac.cy",username="root",password="UniServer",command="ls",background=False,timeout=None):
    sshCommand=command
    if background==True:
        sshCommand=sshCommand+" &"
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
    ssh.connect(hostname, username=username, password=password,timeout=timeout)
    #print ("sshcommand "+str(sshCommand))
    stdin,stdout,stderr=ssh.exec_command(command=sshCommand,timeout=timeout)
    dummy=stdout.readlines() #just do this to make exec blocking call
    #return stdout.readlines()
    ssh.close()

UNKNOWN_PID=-1
def executeCommandAndReturnPID(hostname="juno_uni.in.cs.ucy.ac.cy",username="root",password="UniServer",command="ls"):
    sshCommand=command
    #background=True
    #if background==True:
    sshCommand=sshCommand+" &>/dev/null & echo PIDIS $!; exit"
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
    ssh.connect(hostname, username=username, password=password)
    stdin,stdout,stderr=ssh.exec_command(command=sshCommand)
    dummy=stdout.readlines() #just do this to make exec blocking call
    pidToReturn=UNKNOWN_PID
    try:
        for line in dummy:
            tokens = line.split(" ")
            if "PIDIS" in str(tokens[0]):
                pidToReturn=int(tokens[1])
                #print ("PID to return "+str(pidToReturn))
                break
    except:
        print("COULD NOT RETRIEVE PID")
    ssh.close()
    return pidToReturn