import langchain
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationSummaryMemory,ConversationSummaryBufferMemory,ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms import TextGen

class SimpleChatbot:
    def __init__(self) ->None:
        self.template = """ 
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
        
        self.memory = ConversationBufferMemory(llm=llm,human_prefix="USER",ai_prefix="ATOM")
        self.prompt = PromptTemplate(template=template,input_variables=["history","input"])
    
    def __init__(self,template) -> None:
        self.template = template
        self.memory = ConversationBufferMemory(llm=llm,human_prefix="USER",ai_prefix="ATOM")
        self.prompt = PromptTemplate(template=template,input_variables=["history","input"])