import os
import glob
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LocalRAGPipeline:
    def __init__(self, db_dir="./chroma_db"):
        # Initialize Gemini and the local Chroma Vector Database
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.chroma_client = chromadb.PersistentClient(path=db_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="support_kb")

    def get_embedding(self, text: str) -> list:
        """Calls Gemini to convert text into a mathematical vector."""
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        return response.embeddings[0].values

    def ingest_document(self, doc_name: str, content: str):
        """Splits the document and saves the chunks to the database."""
        # We split text into 400-character chunks with a 40-character overlap
        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
        chunks = splitter.split_text(content)
        
        for idx, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)
            chunk_id = f"{doc_name}_chunk_{idx}"
            
            # Save to ChromaDB
            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                metadatas=[{"source": doc_name, "chunk_index": idx}],
                documents=[chunk]
            )

    def retrieve_context(self, query: str, top_k: int = 3) -> list:
        """Searches the database for the most relevant document chunks."""
        query_vector = self.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        
        retrieved_items = []
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                retrieved_items.append({
                    "text": results['documents'][0][i],
                    "source": results['metadatas'][0][i]['source'],
                    "score": 1.0 - (results['distances'][0][i] if results['distances'] else 0.0)
                })
                
        return retrieved_items

# --- Utility Function to Load the Data Folder ---
def build_database_from_folder(data_folder="data"):
    """Reads all compatible files in the data folder and ingests them."""
    rag = LocalRAGPipeline()
    print("Starting Knowledge Base Ingestion...")
    
    # Read text and markdown files
    for ext in ["*.txt", "*.md"]:
        for filepath in glob.glob(os.path.join(data_folder, ext)):
            filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                rag.ingest_document(filename, content)
                print(f"✅ Ingested: {filename}")
                
    # Read PDF files
    for filepath in glob.glob(os.path.join(data_folder, "*.pdf")):
        filename = os.path.basename(filepath)
        reader = PdfReader(filepath)
        pdf_text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                pdf_text += extracted + "\n"
        
        rag.ingest_document(filename, pdf_text)
        print(f"✅ Ingested PDF: {filename}")
        
    print("Database built successfully!")

# Run the ingestion process if we execute this file directly
if __name__ == "__main__":
    build_database_from_folder()