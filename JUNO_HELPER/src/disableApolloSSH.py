'''
Created on 14 Jun 2017

@author: zachad01
'''
from paramiko import SSHClient, client

def disableApollo(targetHostname,targetSSHusername,targetSSHpassword):
    while True:
        try:    
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(client.AutoAddPolicy()) 
            ssh.connect(targetHostname, username=targetSSHusername, password=targetSSHpassword)
            stdin,stdout,stderr=ssh.exec_command(command="/media/oldDisk1/root/disableApollo &>/dev/null;")
            dummy=stdout.readlines()
            ssh.close()
            break
        except(Exception):
            continue



