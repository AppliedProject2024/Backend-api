from langchain_openai import OpenAIEmbeddings
from config.chromadb_config import CHROMA_PATH
from langchain_chroma import Chroma
from flask import jsonify
from config.chromadb_config import vector_store

def query(query_text):
    #retrieve vector store
    db = vector_store
    
    #perform similarity search based on query text get 3 chunks for now
    results = db.similarity_search(query_text, k=3)
    
    #combine text from all results
    combine_text = "\n\n- -\n\n".join([doc.page_content for doc in results])

    #return combined text
    return jsonify(combine_text)