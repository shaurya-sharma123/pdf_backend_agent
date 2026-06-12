from parser import extract_chunks
import chromadb
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

chroma_client = chromadb.CloudClient(
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE"),
    api_key=os.getenv("CHROMA_API_KEY")
)

collection = chroma_client.get_or_create_collection(name="gemini_cloud_collection")
ai_client = genai.Client()

def load_pdf_to_vector_store(file_path: str):
    chunks = extract_chunks(file_path)
    ids = [f"chunk_id{i}" for i in range(len(chunks))]
    embeddings_list = []

    for chunk in chunks:
        response = ai_client.models.embed_content(
            model="gemini-embedding-2",
            contents=chunk
        )

        embeddings_list.append(response.embeddings[0].values)

    collection.upsert(
        embeddings=embeddings_list,
        ids=ids,
        documents=chunks
    )
