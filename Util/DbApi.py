from pymongo import MongoClient

class DbApi():
    def __init__(self,hostname,port=27017,username="",password="") -> None:
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.dbClient = ""

    def Open_connection(self):
        self.dbClient = MongoClient(self.hostname,port=self.port)
        
    def Close_connection(self):
        self.dbClient.close()

    
    

        
    