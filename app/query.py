from flask import jsonify, request
from config.chromadb_config import vector_store
from config.ai_api_config import Ai_call_api
from flask_jwt_extended import get_jwt_identity

def askAI(query_text, prompt_template, word_num, question_count, complexity, language="English"):
    #retrieve vector store
    db = vector_store

    #get user email from JWT token
    user_email = get_jwt_identity()

    #perform similarity search based on query text get 3 chunks for now
    results = db.similarity_search(
        query_text,
        filter={"user_email": user_email},
        k=20,)
    
    #combine text from all results
    combine_text = "\n\n- -\n\n".join([doc.page_content for doc in results])

    #combine text and query text into prompt
    prompt = prompt_template.format(
        context=combine_text, 
        question=query_text, 
        word_num=word_num, 
        question_count=question_count, 
        complexity=complexity,
        language=language
    )    

    #get response from model
    response = Ai_call_api(prompt)

    #return response and context
    return response, combine_text


def query():
    #get query text from request
    query_text = request.json["query_text"]
    language = request.json["language"]
    #set parameters to null
    word_num = 0
    question_count = 0
    complexity = ""

    #template for prompt
    prompt_template = """"
    Answer the following question based on the following context from retrieved context: {context}

    Ensure the output is in the follwoing language: {language}

    If the context does not contain relevant information, ignore it.

    Question: {question}
    """

    #get response from model
    response, context = askAI(query_text, prompt_template, word_num, question_count, complexity, language)

    #return response and context
    return jsonify({"response": response, "context": context})


def summary():
    #get query text from request
    query_text = request.json["query_text"]
    #get parameters from request
    word_num = request.json["word_num"]
    complexity = request.json["complexity"]
    question_count = 0
    language = request.json["language"]


    #template for prompt
    prompt_template = """"
    Create a summary of the user query using the retrieved context:
    {context}

    Ensure the output is in the follwoing language: {language}

    Make the summary {word_num} words long.
    Ensure the complexity level is {complexity}

    Ignore unrelated information

    Query: {question}
    """
    
    #get response from model
    response, context = askAI(query_text, prompt_template, word_num, question_count, complexity, language)

    #return response
    return jsonify({"response": response, "context": context})


def mcq():
    #get query text from request
    query_text = request.json["query_text"]
    #get parameters from request
    question_count = request.json["question_count"]
    complexity = request.json["complexity"]
    word_num = 0
    language = request.json["language"]

    
    #template for prompt
    prompt_template = """"
    Create {question_count} multiple-choice questions (MCQs) based on the following context:
    {context}

    Ensure the output is in the follwoing language: {language}

    The question should have a complextity level of {complexity}

    Format them like this:

    (1) Question:
    A: Option 1
    B: Option 2
    C: Option 3
    D: Option 4
    Answer: 

    Ensure the correct answers are spread between the options.

    Query: {question}
    """

    #get response from model
    response, context = askAI(query_text, prompt_template, word_num, question_count, complexity, language)

    #return response
    return jsonify({"response": response, "context": context})