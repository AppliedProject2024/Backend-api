from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from pypdf import PdfReader
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
import hashlib
from config.chromadb_config import vector_store

#function to read PDF file
def extract_chunk(uploaded_file, doc_id, user_email):
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
                "chunk_index": index,
                "user_email": user_email
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

    #get user email
    user_email = get_jwt_identity()

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
    chunks = extract_chunk(pdf_file, doc_id, user_email)

    #add chunks to vector store
    vector_store.add_documents(chunks)

    return jsonify({"message": "File uploaded"}), 200
    
def get_user_documents():
    #get user email from request
    user_email = get_jwt_identity()
    print(f"user_email: {user_email}")

    #use search to get user documents
    results = vector_store.get(
        where={"user_email": user_email}
    )

    #assign results to set to remove duplicates
    filenames = set()
    for doc in results.get('metadatas', []):
        if doc and 'filename' in doc:
            filenames.add(doc['filename'])

    #return documents
    return jsonify({"filenames": list(filenames)}), 200

def delete_document():
    #get request data
    data = request.get_json()

    #check if data provided
    if not data or "filename" not in data:
        return jsonify({"error": "Filename required"}), 400
    
    #retrieve filename from request data
    filename = data["filename"]

    #get user email for token
    user_email = get_jwt_identity()

    #use search to get chunks related to filename
    results = vector_store.get(
        where={
            "$and": [
                {"user_email": user_email},
                {"filename": filename}
            ]
        }
    )

    #check if chunks exists
    if not results or not results.get('ids'):
        return jsonify({"error": "Document not found"}), 404
    
    #get ids of chunks to delete
    chunk_ids = results.get('ids', [])

    #delete chunks from vector store
    vector_store.delete(
        ids=chunk_ids
    )

    return jsonify({
        "message": f"Document '{filename}' deleted",
        "chunks_deleted": len(chunk_ids)
    }), 200