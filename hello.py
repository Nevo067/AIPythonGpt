from flask import Flask

from flask import request

from flask_cors import CORS
import langchain
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import PromptTemplate
from langchain.llms import TextGen


import httpx
import json


from CustomClassLang.CustomLlm import CustomLLM

app = Flask(__name__)
CORS(app)
url = "http://localhost:5000"


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
    langchain.debug = True

    template = """Question: {question} 
    Answer : Let's think step by step"""

    prompt = PromptTemplate(template=template,input_variables=["question"])
    llm = TextGen(model_url=url)
    chain = LLMChain(prompt=prompt,llm=llm)
    data = request.get_json()
    
    ''' 
    conversation_with_summary = ConversationChain(
        llm=llm,
        memory=ConversationSummaryMemory(llm=llm,return_messages=True),
        verbose=True,
        
        )
    '''  
    #text= llm(prompt= data["user_input"],history= data["history"])
    return  chain.run(data["user_input"])



if __name__ == '__main__':
    app.run(debug=True, port=8001)
