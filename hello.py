import sys
sys.path.insert(0, './Util')

from flask import Flask

from flask import request

from flask_cors import CORS
import langchain
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationSummaryMemory,ConversationSummaryBufferMemory,ConversationBufferMemory,ChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain.llms import TextGen


import httpx
import json

from History import HistoryManager


from CustomClassLang.CustomLlm import CustomLLM

prefix_humain = "YOU";
prefix_AI = "AI";
history_manager = HistoryManager(prefix_AI,prefix_humain);

## Init Langchain
app = Flask(__name__)
CORS(app)

#DB


url = "http://localhost:5000"
llm = TextGen(model_url=url)
memory = ConversationBufferMemory(llm=llm,human_prefix=prefix_humain,ai_prefix=prefix_AI)
# summure Conversation's History
history = ChatMessageHistory()
memory1 = ConversationSummaryMemory(llm=llm,human_prefix="YOU",ai_prefix="ATOM",chat_memory=history)


## Template 

template = """ 
Atom's Persona: You are a chatbot having a conversation with a human
<START>
[DIALOGUE HISTORY]

YOU: Salut
ATOM: Bonjour comment puis-je vous aider ?
YOU: J'aimerais connaitre ton zelda préferé
ATOM: J'adore Skyward sword. 
{history}

YOU: {input}
ATOM:
"""

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

prompt = PromptTemplate(template=templateSummury,input_variables=["history","input"])

conversation_with_summary = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True,
        )




@app.route("/")
def hello_world():
    return "ppp"


@app.route("/test", methods=['POST'])
def test():
    data = request.get_json()

    history = data["history"]
    message = data["user_input"]
    body = {
        "user_input": message,
        "max_new_tokens": 250,
        "auto_max_new_tokens": False,
        "history": history,
        "mode": "chat",
        "character": "Example",
        "instruction_template": "Vicuna-v1.1",
        "your_name": "You",
        "regenerate": False,
        "_continue": False,
        "stop_at_newline": False,
        "chat_generation_attempts": 1,
        "chat_instruct_command": "Continue the chat dialogue below. Write a single reply for the character "
    }
    data = json.dumps(body)
    headers = {"Content-Type": "application/json"}

    res = httpx.post(url=url, data=data, headers=headers,timeout=10.0)
    print(res.text)
    return res.text

@app.route("/testL", methods=['POST'])
def testL():
    
    data = request.get_json()
    history_manager.add_humain_message(data["user_input"])
    
    #Langchain
    ''' V1
    langchain.debug = True

    template = """Question: {question} 
        Answer : Let's think step by step"""

    prompt = PromptTemplate(template=template,input_variables=["question"])
    llm = TextGen(model_url=url)
    chain = LLMChain(prompt=prompt,llm=llm)
    conversation_with_summary = ConversationChain(
        llm=llm,
        memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=128),
        verbose=True,
    )

    '''

    ''' 
    conversation_with_summary = ConversationChain(
        llm=llm,
        memory=ConversationSummaryMemory(llm=llm,return_messages=True),
        verbose=True,
        
        )
    '''  
    

    #text= llm(prompt= data["user_input"],history= data["history"])
    rep = conversation_with_summary.predict(input=data["user_input"])
    history_manager.add_ai_message(rep)
    print(history_manager.history)

    return rep



if __name__ == '__main__':
    app.run(debug=True, port=8001)
