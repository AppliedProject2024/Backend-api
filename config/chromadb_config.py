from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

#initialise Chroma with OpenAI embeddings
embeddings = OpenAIEmbeddings()

#initialise Chroma vector store
vector_store = Chroma(
    #set collection name
    collection_name="pdf_chunks",
    #set embedding function to openai embeddings
    embedding_function=embeddings,
    #set directory to persist data
    persist_directory="./chromadb"
)