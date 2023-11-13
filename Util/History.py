import json
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
        The function `get_string_message` takes a message dictionary as input and returns a formatted
        string message based on the presence of a human or AI prefix in the message.
        
        :param message: The `message` parameter is a dictionary that contains two keys:
        `self.humain_prefix` and `self.ai_prefix`. The values associated with these keys are strings
        :return: a string message.
        """
        strs = ""

        if(self.humain_prefix in message):
            strs = self.humain_prefix +" : "+message[self.humain_prefix]
        else:
            strs = self.ai_prefix +" : "+message[self.ai_prefix]
        
        return strs

        

    def get_two_last_String(self):
        """
        The function `get_two_last_String` returns a concatenated string of the two most recent messages
        in the chat history.
        :return: a string that contains the text of the second to last message and the last message in
        the chat history.
        """
        nb = len(self.history)
        message = self.get_history()[nb-2];
        message1 = self.get_history()[nb-1];
        
        messageText = self.get_string_message(message=message)
        messageText1 = self.get_string_message(message=message1)
        

        newText = messageText+" \n"+messageText1

        return newText
    
    def transform_text_to_dict(self,ai, humain, message):
        new_dict = [];
        newText = message.split("\n")

        for textMessage in newText :
            text_message_part= textMessage.split(":")
            new_str_message = '{"' +text_message_part[0] +'":"'+ text_message_part[1] + '"}'
            dict_message = json.loads(new_str_message)
            new_dict.append(dict_message)
        print(new_dict)
        return new_dict
        
         
 

            
