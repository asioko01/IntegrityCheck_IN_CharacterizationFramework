'''
Created on 14 Jun 2017

@author: zachad01
'''
from paramiko import SSHClient, client
import time

def waitTillSSHworks(targetHostname,targetSSHusername,targetSSHpassword,timeOut=210):
    count=0
    while True:
        try:    
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
            ssh.connect(targetHostname, username=targetSSHusername, password=targetSSHpassword,timeout=15)
            ssh.close()
            break
        except(Exception):
            time.sleep(1)
            count=count+16
            if(count>=timeOut):
                return 1
            continue
    return 0