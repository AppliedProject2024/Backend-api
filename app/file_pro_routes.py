from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from pypdf import PdfReader
import os
import chromadb
from flask import Flask, request, jsonify, Blueprint
from config.chromadb_config import collection

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

#route to handle pdf uploads
@file_bp.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    pdf_file = request.files["file"]

    if pdf_file.filename == "":
        return jsonify({"error": "No file seleced"}), 400
    
    chunks = ExtractAndChunk(pdf_file)

    for idx, chunk in enumerate(chunks):
        collection.add(
            ids = [f"doc_{pdf_file.filename}_{idx}"],
            documents = [chunk.page_content]
        )

    return jsonify({"message": "File uploaded"}), 200
    
    