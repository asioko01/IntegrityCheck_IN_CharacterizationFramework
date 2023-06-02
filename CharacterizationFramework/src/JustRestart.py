'''
Created on Mar 2, 2017

@author: zhadji01
'''
from Experiment import Experiment
import traceback
from paramiko import SSHClient, client
import paramiko
import socket
from threading import Timer
from threading import Thread
import time
import os
import subprocess
import sys
from json_helper import *
import math
from random import Random
from SerialHandler  import SerialHandler
import serial
import Utilites
import datetime
from Utilites import getTimestampInSecs, getNextOf, getBinaryStringOfInt

os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
#time.sleep(6)
#os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 on\"")
#command = "C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 check | C:/cygwin64/bin/grep -o 'ON\|OFF' \""
#result = subprocess.check_output(command, shell=True)
#print(result)