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
            "_id": ObjectId(),
            "Text":message,
            "UserId":idUser,
            "Date": date,
            
        }

        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]
        print(col.find_one(query))
        col.find_one_and_update(query,{'$push':{"Message":message}})

        self.db.Close_connection()

        return True
    def get_message_by_idConv(self,id_conv,nb):
        """
        The function retrieves a specified number of messages from a conversation based on its ID.
        
        :param id_conv: The `id_conv` parameter is the ID of the conversation for which you want to
        retrieve the messages
        :param nb: The parameter "nb" is used to specify the number of messages to retrieve from the
        conversation. It is used in the query to limit the number of messages returned
        """

        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]

        query = {"_id": ObjectId(id_conv)}
        project={'Message': {'$slice': nb}}

        return col.find(query,project)
    
    def get_message_by_idConv_nb(self,id_conv,nb_start,nb_get):
        """
        The function retrieves a specific range of messages from a conversation based on the
        conversation ID.
        
        :param id_conv: The `id_conv` parameter is the unique identifier of the conversation for which
        you want to retrieve messages
        :param nb_start: The `nb_start` parameter is the starting index of the messages you want to
        retrieve. It specifies the position of the first message you want to retrieve in the list of
        messages for the given conversation
        :param nb_end: The `nb_end` parameter is used to specify the ending index of the range of
        messages you want to retrieve
        :return: the result of the find query on the specified collection in the database. The query is
        searching for a document with the specified `_id` value and then using the `` operator to
        return a subset of the `Message` array field, starting from `nb_start` and ending at `nb_end`.
        """

        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]

        query = {"_id": ObjectId(id_conv)}
        project={'Message': {'$slice': [nb_start, nb_get]}}

        return col.find(query,project)
    
    def get_nb_message_by_id(self,id_conv):
        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]

        query = {"_id": ObjectId(id_conv)}
        project={ {'$size': "Message"}}
    
    def count_nb_message(self,id_conv):
        final_result = ""

        self.db.Open_connection()

        dbN = self.db.dbClient[self.databasesName]
        col = dbN[self.collection_name]

        query = {"_id": ObjectId(id_conv)}
        result = col.aggregate(
            [
                {
                    '$unwind': '$Message'
                }, {
                    '$group': {
                        '_id': 1111, 
                        'count': {
                            '$sum': 1
                        }
                    }
                }
            ]
        )
        for count in result:
            final_result = count

        self.db.Close_connection()

        return final_result


    


        