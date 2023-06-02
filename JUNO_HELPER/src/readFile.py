'''
Created on 20 Ιουν 2017

@author: admin
'''

def readFile(filePath):
    values = []
    with open(filePath) as file:
        for line in file: #low memory consumption iterator. even TB files can be read on a standard laptop.
            line = line.strip() #or some other preprocessing
            values.append(float(line))