from flask import jsonify, request
from config.chromadb_config import vector_store
from langchain.chat_models import ChatOpenAI

def query():
    #get query text from request
    query_text = request.json["query_text"]
    #retrieve vector store
    db = vector_store
    
    #perform similarity search based on query text get 3 chunks for now
    results = db.similarity_search(query_text, k=3)
    
    #combine text from all results
    combine_text = "\n\n- -\n\n".join([doc.page_content for doc in results])

    #template for prompt
    prompt_template = """"
    Answer the following question solely based on the following context from retrieved documents: {context}
    If a piece of information from context is not related to the question, please ignore it.
    Question: {question}
    """

    #combine text and query text into prompt
    prompt = prompt_template.format(context=combine_text, question=query_text)

    #initialise model
    model = ChatOpenAI()

    #get response from model
    response = model.predict(prompt)

    #return response
    return jsonify({"response": response})

