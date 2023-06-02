'''
Created on 17 Μαΐ 2017

@author: admin
'''

from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder

class MongoDBhandler(object):
    '''
    classdocs
    '''
    
    Global=None
    
    
    def __init__(self, ip=None,port=None,user=None,password=None):
        self.server=None
        if ip==None:
            self._client = MongoClient() #connect to running instance with default ip port
        else:
            self.server = SSHTunnelForwarder(
                ip,
                ssh_username=user,
                ssh_password=password,
                remote_bind_address=('127.0.0.1', port)
            )
            self.server.start()
            self._client=MongoClient('127.0.0.1',self.server.local_bind_port)
        self._db=None
        self._coll=None
        
    def setDB(self,dbname): 
        self._db=self._client[dbname]
        
    def setColl(self,collname):
        if self._db==None:
            raise Exception("No db set... First call setDB method") 
        self._coll=self._db[collname]
    
    def insertDoc(self,record,dbname=None,dbcol=None):
        self.exceptionRaiser(dbname,dbcol)
        if  (dbname==None or dbcol==None ):
            self._coll.insert(record)
        else:
            self._client[dbname][dbcol].insert(record)  
    
    def setGlobal(self):
        MongoDBhandler.Global=self 
    
    def dropColl(self):
        if self._coll is not None:
            self._coll.drop()
        else:
            print("No coll set.. First call setColl method")
    
    def exceptionRaiser(self,dbname=None,dbcol=None):
        if (self._db==None or self._coll==None) and (dbname==None or dbcol==None ):
            raise Exception("No db or coll set... First call setDB, setCol methods or give dbname dbcol as parameter")
    
    def closeConnection(self):
        if self.server is not None:
            self.server.stop()
        