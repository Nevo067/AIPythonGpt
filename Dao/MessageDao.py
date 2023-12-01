import sys
sys.path.insert(0,'./Util')
sys.path.insert(0,'./Dao')

import datetime

from DbApi import DbApi
from ConvDao import ConvDao

class MessageDao():
    def __init__(self,db:DbApi,database_name,collection_name) -> None:
        self.db = db
        self.databasesName = database_name
        self.collection_name = collection_name
    
    def add_message(self,idConv,convDao:ConvDao,userId,text):
        
       
        
        conv = convDao.get_conv_by_id(idConv=idConv)
        conv.Message.append(message)
