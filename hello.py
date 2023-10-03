from flask import Flask

from flask import request

from flask_cors import CORS
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory

import httpx
import json


from CustomClassLang.CustomLlm import CustomLLM

app = Flask(__name__)
CORS(app)
url = "http://localhost:5000/api/v1/chat"


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
    llm = CustomLLM()

    conversation_with_summary = ConversationChain(
        llm=llm,
        memory=ConversationSummaryMemory(llm=llm,return_messages=True),
        verbose=True,
        
        )

    #text= llm(prompt= data["user_input"],history= data["history"])
    return  conversation_with_summary.predict(input=data["user_input"])



if __name__ == '__main__':
    app.run(debug=True, port=8001)
