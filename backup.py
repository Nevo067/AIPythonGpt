from flask import Flask

from flask import request

from flask_cors import CORS
import langchain
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationSummaryMemory,ConversationSummaryBufferMemory,ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms import TextGen


import httpx
import json


from CustomClassLang.CustomLlm import CustomLLM

app = Flask(__name__)
CORS(app)

url = "http://localhost:5000"
llm = TextGen(model_url=url)
memory = ConversationBufferMemory(llm=llm,human_prefix="USER",ai_prefix="ATOM")

template = """ 
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

prompt = PromptTemplate(template=template,input_variables=["history","input"])

conversation_with_summary = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True,
        )
