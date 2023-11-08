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
