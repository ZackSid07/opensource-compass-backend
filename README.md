# OpenSource Compass (Backend API)

## 1. What is it?
**OpenSource Compass** is an AI-powered mentor designed to help junior developers understand and contribute to massive open-source projects. 

Instead of forcing new contributors to blindly read thousands of lines of code, this backend system automatically ingests GitHub repositories, mathematically maps their architecture, and acts as an interactive teacher. 

**Key Features:**
* **Automated Ingestion:** Clones GitHub repositories and analyzes Python files using Abstract Syntax Trees (AST).
* **Dependency Mapping:** Uses NetworkX to map out how files and modules connect to each other.
* **Vector Memory (RAG):** Chunks code and stores it as mathematical embeddings in a Supabase PostgreSQL database using `pgvector` and local HuggingFace models.
* **AI Chat Engine:** Powered by Google's Gemini LLM, it retrieves relevant code chunks and explains complex software logic in plain English.
* **Architecture Visualization:** Automatically converts raw codebase graphs into valid Mermaid.js flowcharts for frontend rendering.

## 2. How to install / setup
To run this project locally, you will need Python 3.10+ and Git installed on your machine.

**Step 1: Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/opensource-compass-backend.git
cd opensource-compass-backend
```

**Step 2: Set up a Virtual Environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Environment Variables**
Create a `.env` file in the root directory and add your API keys:
```env
SUPABASE_URL="your_supabase_project_url"
SUPABASE_KEY="your_supabase_anon_public_key"
GEMINI_API_KEY="your_google_ai_studio_key"
```

**Step 5: Run the Server**
```bash
uvicorn main:app --reload
```
The API will be live at `http://127.0.0.1:8000`.

## 3. Links to hosted version
* **Local Interactive API Docs (Swagger UI):** `http://127.0.0.1:8000/docs`
* **Production API:** *(Coming soon - Will be deployed to Render/Railway)*
* **Frontend Application:** *(Coming soon)*

## 4. Examples / Screenshots
*(Note: Add frontend UI screenshots here once the React application is built.)*

**Core API Flow Example:**
* **`POST /ingest`**: Send `{"github_url": "..."}` to download the repository.
* **`POST /embed/{repo_name}`**: Slices the code into chunks and saves them to the Supabase vector database.
* **`POST /chat`**: Send `{"query": "How does the database login work?"}`. The backend uses Semantic Search to find the exact Python files and Gemini AI returns a plain-English explanation of the authentication flow.
* **`GET /diagram/{repo_name}`**: Returns a raw Mermaid.js string (e.g., `graph TD; main.py --> auth.py;`) to draw the system architecture.

## 5. Contributing Instructions
We welcome contributions to make open-source more accessible!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
