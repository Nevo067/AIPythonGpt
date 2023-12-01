import sys
sys.path.insert(0,'./Util')
from pymongo import MongoClient
from bson.objectid import ObjectId


from DbApi import DbApi
import datetime

class ConvDao():
    def __init__(self,db:DbApi,database_name,collection_name) -> None:
        self.db = db
        self.databasesName = database_name
        self.collection_name = collection_name

    def add_conv(self,nom):
        """
        The function `add_conv` adds a conversation to a database and returns the ID of the inserted
        document.
        
        :param nom: The parameter "nom" is a string that represents the name of the conversation
        :return: the string representation of the inserted ID.
        """
        conv = {
            "Nom":nom,
            "Message":[],
            "Surnom":[]
            }
        
        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]
        idConv = col.insert_one(conv)

        print(idConv.inserted_id)

        self.db.Close_connection()

        return str(idConv.inserted_id)

    def get_conv_by_id(self,idConv):
        """
        The function `get_conv_by_id` retrieves a conversation from a MongoDB collection based on its ID.
        
        :param idConv: The parameter "idConv" is the ID of the conversation that you want to retrieve
        from the database
        :return: the result of the `find_one` method, which is a single document that matches the given
        query.
        """
        query = {"_id":ObjectId(idConv)} 
        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]

        return col.find_one(query)
    
    def add_message(self,idConv,message,idUser):
        """
        The function `add_message` adds a new message to a conversation in a MongoDB database.
        
        :param idConv: The parameter "idConv" is the ID of the conversation or chat where the message
        will be added
        :param message: The "message" parameter is the text of the message that you want to add to the
        conversation
        :param idUser: The `idUser` parameter is the ID of the user who is sending the message
        :return: a boolean value of True.
        """
        date = datetime.datetime.now()
        query = {"_id": ObjectId(idConv)}
        message = {
            "Text":message,
            "UserId":idUser,
            "Date": date
        }

        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]
        print(col.find_one(query))
        col.find_one_and_update(query,{'$push':{"Message":message}})

        self.db.Close_connection()

        return True