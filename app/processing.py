from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from pypdf import PdfReader
from flask import request, jsonify
import hashlib
from config.chromadb_config import vector_store

#function to read PDF file
def extract_chunk(uploaded_file, doc_id):
    #extract pdf text
    pdf_reader = PdfReader(uploaded_file)
    full_text = ""
    #extract text from each page
    for page in pdf_reader.pages:
        full_text += page.extract_text()
    
    #chunk text using langchain TextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n", #split by newline
        chunk_size=300, #maximun chunk size
        chunk_overlap=100 #overlap between chunks preserves context
    )
    #split text into chunks
    chunks = text_splitter.split_text(full_text)
    
    #return chunks as list of Documents with metadata
    return[
        Document(
            page_content=chunk,
            metadata={
                "doc_id": doc_id,
                "filename": uploaded_file.filename,
                "chunk_index": index
            }
        )
        for index, chunk in enumerate(chunks)
    ]

#gernerate a unique id for file that will be assigned anytime uploaded
def generate_id(uploaded_file):
    #generate hash from file content
    pdf_reader = PdfReader(uploaded_file)
    full_text = ""
    #extract text from each page
    for page in pdf_reader.pages:
        #add page text to full text
        full_text += page.extract_text()

    uploaded_file.seek(0)
    #return md5 hash of full text
    return hashlib.md5(full_text.encode('utf-8')).hexdigest()

def upload_pdf():
    #check if file is in request
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    #get file from request
    pdf_file = request.files["file"]
    #check if file is empty
    if pdf_file.filename == "":
        return jsonify({"error": "No file seleced"}), 400
    
    #generate unique id for file
    doc_id = generate_id(pdf_file)

    #use search to check if document exists
    check_result = vector_store.similarity_search(
        "CHECK_DOCUMENT_EXISTS",
        filter={"doc_id": doc_id},
        k=1
    )

    #check if document exists
    if check_result:
        return jsonify({"error": "Document already exists"}), 409
    
    #extract and chunk pdf file
    chunks = extract_chunk(pdf_file, doc_id)

    #add chunks to vector store
    vector_store.add_documents(chunks)

    return jsonify({"message": "File uploaded"}), 200
    
