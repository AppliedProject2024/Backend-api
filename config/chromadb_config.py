from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os

#initialise Chroma with OpenAI embeddings
embeddings = OpenAIEmbeddings()

#set path to persist data
CHROMA_PATH = os.getenv('CHROMA_PATH', './chromadb')

#check if path exists and create it if not
if not os.path.exists(CHROMA_PATH):
    os.makedirs(CHROMA_PATH)

#initialise Chroma vector store
vector_store = Chroma(
    #set collection name
    collection_name="pdf_chunks",
    #set embedding function to openai embeddings
    embedding_function=embeddings,
    #set directory to persist data
    persist_directory=CHROMA_PATH
)