from pymongo import MongoClient

class DbApi():
    def __init__(self,hostname,port=27017,username="",password="") -> None:
        """
        The function initializes a class instance with hostname, port, username, password, and dbClient
        attributes.
        
        :param hostname: The hostname parameter is used to specify the address of the MongoDB server
        where the database is hosted. It should be a string representing the IP address or domain name
        of the server
        :param port: The `port` parameter is an optional parameter that specifies the port number to
        connect to the MongoDB server. If no port number is provided, it defaults to 27017, which is the
        default port for MongoDB, defaults to 27017 (optional)
        :param username: The `username` parameter is used to specify the username for authentication
        when connecting to a MongoDB database. If no username is provided, it will default to an empty
        string
        :param password: The `password` parameter is used to specify the password for the database
        connection. It is an optional parameter and if not provided, it will default to an empty string
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.dbClient = ""

    def Open_connection(self):
        """
        The function opens a connection to a MongoDB database using the specified hostname and port.
        """
        self.dbClient = MongoClient(self.hostname,port=self.port)
        
    def Close_connection(self):
        """
        The Close_connection function closes the connection to the database.
        """
        self.dbClient.close()

    
    

        
    