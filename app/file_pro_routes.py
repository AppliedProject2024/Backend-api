from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from pypdf import PdfReader
import os
import chromadb
from flask import Flask, request, jsonify, Blueprint
from config.chromadb_config import collection
import hashlib

#feedback blueprint
file_bp = Blueprint("file_bp", __name__)

#function to read PDF file
def ExtractAndChunk(uploaded_file):
    #extract pdf text
    pdf_reader = PdfReader(uploaded_file)
    full_text = ""
    #extract text from each page
    for page in pdf_reader.pages:
        full_text += page.extract_text()
    
    #chunk text using langchain TextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n", #split by newline
        chunk_size=1000, #maximun chunk size
        chunk_overlap=100 #overlap between chunks preserves context
    )
    #split text into chunks
    chunks = text_splitter.split_text(full_text)
    #return chunks as list of Documents
    return [Document(page_content=chunk) for chunk in chunks]

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

#route to handle pdf uploads
@file_bp.route("/upload", methods=["POST"])
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

    #get existing documents id
    existing_docs = collection.get(
        where={"doc_id": doc_id},
        include=["metadatas"]
    )
    #check if file is already uploaded
    if existing_docs['ids']:
        return jsonify({"error": "File already uploaded"}), 409

    #extract and chunk pdf file
    chunks = ExtractAndChunk(pdf_file)

    #add chunks to collection
    for idx, chunk in enumerate(chunks):
        #generate id for chunk wiht doc id and index
        chunk_id = f"{doc_id}_{idx}"
        collection.add(
            ids = [chunk_id],
            documents = [chunk.page_content],
            #add metadata for chunk with doc id and filename
            metadatas=[{"doc_id": doc_id, "filename": pdf_file.filename}]
        )

    return jsonify({"message": "File uploaded"}), 200
    
    