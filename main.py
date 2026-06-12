from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types 
from database import collection, load_pdf_to_vector_store, ai_client

class AIFinalReport(BaseModel):
    summary: str = Field(description="A brief 1-sentence summary of the answer.")
    detailed_answer: str = Field(description="The complete, detailed answer based on the PDF.")

class AgentQueryRequest(BaseModel):
    question: str
    temperature: float = 0.2

class AgentQueryResponse(BaseModel):
    question: str
    agent_final_report: AIFinalReport

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        load_pdf_to_vector_store("legal_document.pdf")
    
    except Exception as e:
        print(f"Could not load the PDF to cloud on startup: {e}")

    yield

app = FastAPI(lifespan=lifespan)

@app.post("/chat", response_model=AgentQueryResponse)
async def chat_endpoint(agent_request: AgentQueryRequest):
    query_vector_response = ai_client.models.embed_content(
        model="gemini-embedding-2",
        contents=agent_request.question
    )

    query_vector = query_vector_response.embeddings[0].values
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=2
    )

    retrieved_chunks = results['documents'][0] if results["documents"] else[]
    context = "\n---\n".join(retrieved_chunks)

    prompt = (
        "You are an AI assistant. Answer the user's question using ONLY the context provided below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {agent_request.question}"
    )

    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=agent_request.temperature,
            response_mime_type="application/json",
            response_schema=AIFinalReport
        )
    )
    
    structured_data = response.parsed
    
    if not structured_data:
        raise HTTPException(status_code=500, detail="Gemini output response parsing check failed.")
    
    return AgentQueryResponse(
        question=agent_request.question,
        agent_final_report=structured_data
    )