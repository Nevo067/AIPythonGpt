import json
class HistoryManager:
    def __init__(self,ai_prefix,humain_prefix,count_limit) -> None:
        self.history = [];
        self.ai_prefix = ai_prefix;
        self.humain_prefix = humain_prefix;
        self.count_limit = count_limit
        self.count = count_limit;

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
        """
        The function `transform_text_to_dict` takes in three parameters (ai, humain, message), splits
        the message into separate lines, splits each line into key-value pairs, converts each pair into
        a dictionary, and appends the dictionaries to a list before returning the list.
        
        :param ai: The "ai" parameter represents the AI component or entity
        :param humain: The `humain` parameter is a string that represents the name or identifier of a
        human
        :param message: The `message` parameter is a string that contains multiple lines of text. Each
        line represents a key-value pair separated by a colon (:). The key and value are separated by a
        colon (:)
        :return: a list of dictionaries.
        """
        new_dict = [];
        newText = message.split("\n")
        
        for textMessage in newText :
            text_message_part= textMessage.split(":")
            if len(text_message_part) == 2:
                new_str_message = '{"' +text_message_part[0] +'":"'+ text_message_part[1] + '"}'
                dict_message = json.loads(new_str_message)
                new_dict.append(dict_message)
        print(new_dict)
        return new_dict
    
    def is_count_equals_0(self):
        """
        The function checks if the count limit is equal to 0 and returns True if it is, otherwise it
        returns False.
        :return: a boolean value. If the count_limit is less than or equal to 0, it will return True.
        Otherwise, it will return False.
        """
        if self.count <= 0:
            return True 
        else:
            return False
    
    def counting(self,nb_count):
        """
        The function "counting" takes a number as input and subtracts it from the count variable,
        returning False if the count is not equal to 0, and True if it is.
        
        :param nb_count: The parameter `nb_count` represents the number by which the count should be
        decreased
        :return: a boolean value. If the condition `self.is_count_equals_0()` is true, then the function
        returns `True`. Otherwise, it returns `False`.
        """
        print(self.count)
        if self.is_count_equals_0():
            self.count = self.count_limit
            return True
        else:
            self.count -= nb_count
            return False
        
    def get_number_message(self,nb_messages):
        """
        The function `get_number_message` returns a string containing the last `nb_messages` messages
        from a history list.
        
        :param nb_messages: The parameter "nb_messages" represents the number of messages you want to
        retrieve from the chat history
        :return: a string that contains the last `nb_messages` messages from the `self.history` list.
        Each message is converted to a string using the `get_string_message` method and concatenated
        with a newline character.
        """
        historyLength = len(self.history)
        text =""
        for i in range(historyLength-(nb_messages + 1),historyLength):
            message = self.history[i]
            text += self.get_string_message(message=message) +"\n"
        
        return text
         
 

            
