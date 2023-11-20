import chromadb
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.schema import Document,BaseMessage

persit_directory = "./DatabaseChroma/chroma_db"

loader = TextLoader("./DatabaseChroma/test.txt")
document = loader.load();

#print(document);

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(document)



embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db_chroma = Chroma(embedding_function=embedding_function,persist_directory=persit_directory)

db_chroma.delete("dee0665f-7e04-11ee-8c73-c87f54925d7e")