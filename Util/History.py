class HistoryManager:
    def __init__(self,ai_prefix,humain_prefix) -> None:
        self.history = [];
        self.ai_prefix = ai_prefix;
        self.humain_prefix = humain_prefix;

    def add_humain_message(self,message:str):
        self.history.append({self.humain_prefix : message})

    def add_ai_message(self,message:str):
        self.history.append({self.ai_prefix : message})

    def get_history(self):
        return self.history;

    def get_string_message(self,message):
        strs = ""

        if(message[self.ai_prefix] is None):
            strs = self.humain_prefix +" : "+message[self.humain_prefix]
        else:
            strs = self.ai_prefix +" : "+message[self.ai_prefix]
        
        return strs

        

    def get_two_last_String(self):
        nb = len(self.history)
        message = self.get_history()[nb-1];
        message1 = self.get_history()[nb-2];

        messageText = ', '.join([str(dic) for dic in message]) 
        messageText1 = ', '.join([str(dic) for dic in message1])

        newText = messageText+" /n "+messageText1

        return newText
 

            
