import sys
sys.path.insert(0,'./Util')

from DbApi import DbApi

class UserDao():
    def __init__(self,db:DbApi,database_name,collection_name) -> None:
        self.db = db
        self.databasesName = database_name
        self.collection_name = collection_name

    def AddUser(self,login:str,password:str):
        self.db.Open_connection()

        user = {
            "login":login,
            "password":password
        }

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]
        newUser = col.insert_one(user)

        self.db.Close_connection()

        return newUser


        