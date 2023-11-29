import sys
sys.path.insert(0,'./Util')

from DbApi import DbApi

class UserDao():
    def __init__(self,db:DbApi,database_name,collection_name) -> None:
        self.db = db
        self.databasesName = database_name
        self.collection_name = collection_name

    def AddUser(self,login:str,password:str):
        """
        The function `AddUser` adds a new user to a database collection with the provided login and
        password.
        
        :param login: The login parameter is a string that represents the username or login name of the
        user you want to add to the database
        :type login: str
        :param password: The password parameter is a string that represents the password for the user
        :type password: str
        :return: the result of the `insert_one` operation, which is an instance of the `InsertOneResult`
        class.
        """
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
    
    def Is_user_exist(self,login:str,password:str = None):
        
        query = {"login":login,"password":password}
        
        self.db.Open_connection()
        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]

        user = col.find_one(query)

        if user != None:
            return True
        else:
            return False





        