class HistoryManager:
    def __init__(self,ai_prefix,humain_prefix) -> None:
        self.history = [];
        self.ai_prefix = ai_prefix;
        self.humain_prefix = humain_prefix;

    def add_humain_message(self,message:str):
        """
        The function adds a human message to a history list.
        
        :param message: The parameter "message" is a string that represents the human message that you
        want to add to the history
        :type message: str
        """
        self.history.append({self.humain_prefix : message})

    def add_ai_message(self,message:str):
        """
        The function adds an AI-generated message to a chat history.
        
        :param message: The parameter "message" is a string that represents the message to be added to
        the AI's history
        :type message: str
        """
        self.history.append({self.ai_prefix : message})

    def get_history(self):
        """
        The function returns the history of an object.
        :return: The method `get_history` is returning the value of the `history` attribute.
        """
        return self.history;

    def get_string_message(self,message):
        """
        The function `get_string_message` takes a message dictionary as input and returns a string
        representation of the message.
        
        :param message: The "message" parameter is a dictionary that contains two keys: "ai_prefix" and
        "humain_prefix". The values associated with these keys are strings
        :return: a string message.
        """
        strs = ""

        if(message[self.ai_prefix] in message):
            strs = self.humain_prefix +" : "+message[self.humain_prefix]
        else:
            strs = self.ai_prefix +" : "+message[self.ai_prefix]
        
        return strs

        

    def get_two_last_String(self):
        nb = len(self.history)
        message = self.get_history()[nb-2];
        message1 = self.get_history()[nb-1];
        
        self.get_string_message()

        newText = messageText+" /n "+messageText1

        return newText
 

            
