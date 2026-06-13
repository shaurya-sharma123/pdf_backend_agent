# pdf_backend_agent

A production-ready Retrieval-Augmented Generation (RAG) backend built with **FastAPI** and powered completely by **Google Gemini** and **Chroma Cloud**. This system parses legal PDF documents, computes high-dimensional vector embeddings, indexes them remotely, and returns strictly validated structured data schemas.

## 🚀 Features

- **Gemini Embeddings:** Converts raw text segments into mathematical vectors using `gemini-embedding-2`.
- **Chroma Cloud Integration:** Scalable, hosted remote serverless cluster indexing using `chromadb.CloudClient`.
- **FastAPI Lifespan Management:** Uses modern asynchronous `lifespan` architecture to handle file extraction and database syncing seamlessly prior to server initialization.
- **Strict Schema Enforcement:** Forces Gemini to output formatted JSON matching specific Pydantic data blueprints (`AIFinalReport`).
- **Frontend Powered by Streamlit** A well organised user interface that is powered by streamlit.

---

## 📂 Project Architecture

The project runs on a flat, straightforward 3-file system for clean separation of responsibilities:

```text
pdf_backend_agent/
├── parser.py       # Handles local text extraction and chunk segmentation
├── database.py     # Connects to Chroma Cloud and manages Gemini embedding calls
└── main.py         # App entry-point containing schemas, routes, and lifespan logic
```

🛠️ Installation & Setup
1. Clone the Repository
```Bash
git clone [https://github.com/shaurya-sharma123/pdf_backend_agent.git](https://github.com/shaurya-sharma123/pdf_backend_agent.git)
cd pdf_backend_agent
```

2. Configure Environment Variables
Create a .env file in the root directory. Do not commit this file to Git. Add your private API tokens as follows:

```Plaintext
GEMINI_API_KEY="your_google_gemini_api_key"
CHROMA_API_KEY="your_chroma_cloud_api_key"
CHROMA_TENANT="your_chroma_tenant_id"
CHROMA_DATABASE="your_chroma_database_name"
```

3. Place Your Target PDF
Ensure your source document is placed in the root directory and named exactly:

```Plaintext
legal_document.pdf
```

⚡ Running the Application
Start the backend application server using Uvicorn:

```Bash
uvicorn main:app --reload
```
During the startup lifespan event, the system will automatically parse legal_document.pdf, generate embeddings via Google GenAI, and push or update them securely on your Chroma Cloud workspace.

🧪 Testing the API
Once the server is up and running:

Open your web browser and navigate to http://127.0.0.1:8000/docs to enter the interactive Swagger UI.

Click on the POST /chat endpoint.

Click "Try it out" and replace the default body payload with your custom question:

```JSON
{
  "question": "What is the governing law mentioned in this document?",
  "temperature": 0.2
}
```

Click "Execute" to view the structured JSON response containing your summary and detailed answer directly from Gemini.
