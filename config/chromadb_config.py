import chromadb 

#initialise the database
chromadb_client = chromadb.PersistentClient(path="./chroma.db")
collection = chromadb_client.get_or_create_collection(name="pdf_chunks")
