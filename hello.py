import sys
sys.path.insert(0,'./Util')
sys.path.insert(0,'./Dao')

from flask import Flask

from flask import request

from flask_cors import CORS

import chromadb
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.schema import Document,BaseMessage


import langchain
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationSummaryMemory,ConversationSummaryBufferMemory,ConversationBufferMemory,ChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain.llms import TextGen


import httpx
import json

from History import HistoryManager
from DbApi import DbApi
from UserDao import UserDao
from ConvDao import ConvDao

from bson.json_util import dumps




from CustomClassLang.CustomLlm import CustomLLM




#MongoDb

mgdb_host_name = "localhost"
mgdb_port =""
mgdb_databases_name = "" 


mongo_db = DbApi(mgdb_host_name)



prefix_humain = "YOU";
prefix_AI = "ATOM";
history_manager = HistoryManager(prefix_AI,prefix_humain,4);
persit_directory = "./DatabaseChroma/chroma_db"

## Init Langchain
app = Flask(__name__)
CORS(app)

#DB
loader = TextLoader("./DatabaseChroma/test.txt")
document = loader.load();

#print(document);

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(document)



embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db_chroma = Chroma(embedding_function=embedding_function,persist_directory=persit_directory)
db_chroma = db_chroma.as_retriever(search_type = "mmr")



url = "http://localhost:5000"
llm = TextGen(model_url=url)
memory = ConversationBufferMemory(human_prefix=prefix_humain,ai_prefix=prefix_AI,memory_key="history",input_key="humain_input")
# summure Conversation's History
history = ChatMessageHistory()
memory1 = ConversationSummaryMemory(llm=llm,human_prefix="YOU",ai_prefix="ATOM",chat_memory=history)




## Template 

template = """ 
Atom's Persona: You are a chatbot having a conversation with a human
<START>
[DIALOGUE HISTORY]

{tests}


{history}

YOU: {humain_input}
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

prompt = PromptTemplate(template=template,input_variables=["history","humain_input","tests"])



conversation_with_summary = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True    
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
    """
    The `testL` function takes in a JSON object, adds the user input to a history manager, retrieves
    relevant documents from a database, concatenates the page content of the documents into a single
    string, transforms the text into a dictionary, uses a conversation model to generate a response,
    adds the AI response to the history manager, retrieves the last two messages from the history
    manager, and returns the AI response.
    :return: The function `testL()` returns the variable `rep`.
    """
    
    data = request.get_json()
    history_manager.add_humain_message(data["user_input"])
    
    #Get text
    text_doc =""
    
    docsQuery = db_chroma.get_relevant_documents(data["user_input"])
    print(docsQuery)
    
    for page_content in docsQuery:
        text_doc += (page_content.page_content+"\n")
    
    #Add document to text
    doc_dict= history_manager.transform_text_to_dict("YOU","AI",text_doc)

    rep = conversation_with_summary.predict(humain_input= data["user_input"],tests=text_doc)

    history_manager.add_ai_message(rep)

    newMessage = history_manager.get_two_last_String()
    #print(updateDoc)

    print(newMessage)
    
    
    #print(testH)
    
    # update 

    
    if history_manager.counting(1):
        text = history_manager.get_number_message(4)
        doc = Document(page_content=text,
            metadata={
                "source": "test ai",
                }
            )
        doc_list = []
        doc_list.append(doc)
        db_chroma.add_documents(documents=doc_list)
        #print(db_chroma.get())
    

    return rep


@app.route("/testC", methods=['POST'])
def testC():
    
    data = request.get_json()
    history_manager.add_humain_message(data["Text"])
    
    #Get text
    text_doc =""
    
    docsQuery = db_chroma.get_relevant_documents(data["Text"])
    print(docsQuery)
    
    for page_content in docsQuery:
        text_doc += (page_content.page_content+"\n")
    
    #Add document to text
    doc_dict= history_manager.transform_text_to_dict("YOU","AI",text_doc)

    rep = conversation_with_summary.predict(humain_input= data["Text"],tests=text_doc)

    history_manager.add_ai_message(rep)

    newMessage = history_manager.get_two_last_String()
    #print(updateDoc)

    print(newMessage)
    
    
    #print(testH)
    
    # update 

    
    if history_manager.counting(1):
        text = history_manager.get_number_message(4)
        doc = Document(page_content=text,
            metadata={
                "source": "test ai",
                }
            )
        doc_list = []
        doc_list.append(doc)
        db_chroma.add_documents(documents=doc_list)
        #print(db_chroma.get())
    

    Dao= ConvDao(mongo_db,"TestAi","Conversation")
    input_user= request.get_json()
    if Dao.add_message(input_user["id"],input_user["Text"],input_user["UserId"]) :
        Dao.add_message(input_user["id"],rep,input_user["aiId"])
    
    jsonText = json.dumps({"text":rep})
    
    return jsonText

#User Routes

@app.route("/User",methods=['POST'])
def userPost():
    Dao= UserDao(mongo_db,"TestAi","User")
    input_user= request.get_json()
    newUser =Dao.AddUser(input_user["login"],input_user["password"])
    print(newUser)
    return "bip"

@app.route("/Connexion",methods=['POST'])
def Connexion():
    Dao= UserDao(mongo_db,"TestAi","User")
    input_user= request.get_json()
    is_connect = Dao.Is_user_exist(input_user["login"],input_user["password"])
    
    if is_connect:
        return "Connecté"
    else:
        return "Non Connecté"
    
@app.route("/Conv",methods=['POST'])
def addConv():
    Dao= ConvDao(mongo_db,"TestAi","Conversation")
    input_user= request.get_json()
    return Dao.add_conv(input_user["Nom"])

@app.route("/testMessage",methods=["POST"])
def testMessage():
    Dao= ConvDao(mongo_db,"TestAi","Conversation")
    input_user= request.get_json()
    message =Dao.get_message_by_idConv(input_user["id"],10)

    tab = []
    for x in message:
        print(x)
        tab.append(x)
    
    return dumps(tab)

    return "Ajouter"

@app.route("/Messages",methods=["POST"])
def testMessages():
    Dao= ConvDao(mongo_db,"TestAi","Conversation")
    input_user= request.get_json()
    messages =Dao.get_message_by_idConv_nb(input_user["id"],input_user["indexStart"],input_user["indexEnd"])

    tab = []
    for x in messages:
        print(x)
        tab.append(x)
    
    return dumps(tab)

    return "Ajouter"


if __name__ == '__main__':
    app.run(debug=True, port=8001)

@app.route("/message",methods=["POST"])
def addMessage():
    Dao= ConvDao(mongo_db,"TestAi","Conversation")
    input_user= request.get_json()
    if Dao.add_message(input_user["id"],input_user["Text"],input_user["UserId"]) :
        return "Update"
    else:
        return "No-Update"

