def DefaultTemplate():
    templateString = """ 
        Atom's Persona: You are a chatbot having a conversation with a human
        <START>
        [DIALOGUE HISTORY]

        USER: Salut
        ATOM: Bonjour comment puis-je vous aider ?
        USER: J'aimerais connaitre ton zelda préferé
        ATOM: J'adore Skyward sword. 
        {history}

        You: {input}
        Atom:
        """
    return templateString
def SummaryTemplate():
    templateSummury ="""
        Atom's Persona: You are a chatbot having a conversation with a human.
        {history}
        <START>
        [DIALOGUE HISTORY]

        YOU: Salut
        ATOM: Bonjour comment puis-je vous aider ?
        YOU: J'aimerais connaitre ton zelda préferé
        ATOM: J'adore Skyward sword. 


        YOU: {input}
        ATOM: 
        """

    
    

    