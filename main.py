from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from git_service import clone_repository, count_python_files
from graph_builder import build_repo_graph
from vector_store import embed_and_store_repo, search_codebase
from chat_engine import generate_explanation
from diagram_generator import generate_mermaid_diagram

app = FastAPI(title="OpenSource Compass API")


class IngestRequest(BaseModel):
    github_url: str


class ChatRequest(BaseModel):
    query: str


@app.post("/ingest")
def ingest_repo(request: IngestRequest):
    try:
        # Clone the repository
        local_path = clone_repository(request.github_url)

        # Count files in the repository
        file_counts = count_python_files(local_path)

        return {
            "message": "Repository successfully cloned and analyzed.",
            "local_path": local_path,
            "file_counts": file_counts
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/graph/{repo_name}")
def get_dependency_graph(repo_name: str):
    # Construct the local path
    local_path = os.path.join("temp_repos", repo_name)

    # Verify the folder exists
    if not os.path.exists(local_path) or not os.path.isdir(local_path):
        raise HTTPException(
            status_code=404, detail=f"Repository '{repo_name}' not found locally. Please ingest it first.")

    try:
        # Build the graph
        graph_data = build_repo_graph(local_path)
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "OpenSource Compass API is running"}


@app.post("/embed/{repo_name}")
def embed_repo(repo_name: str):
    # Construct the local path
    local_path = os.path.join("temp_repos", repo_name)

    # Verify the folder exists
    if not os.path.exists(local_path) or not os.path.isdir(local_path):
        raise HTTPException(
            status_code=404, detail=f"Repository '{repo_name}' not found locally. Please ingest it first.")

    try:
        # Generate embeddings and store in Supabase
        chunks_processed = embed_and_store_repo(repo_name, local_path)

        return {
            "message": "Repository successfully chunked and embedded.",
            "chunks_processed": chunks_processed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
def search(query: str):
    try:
        results = search_codebase(query)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        raw_chunks = search_codebase(request.query)
        english_answer = generate_explanation(request.query, raw_chunks)
        return {"answer": english_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/diagram/{repo_name}")
def get_diagram(repo_name: str):
    # Construct the local path
    local_path = os.path.join("temp_repos", repo_name)

    # Verify the folder exists
    if not os.path.exists(local_path) or not os.path.isdir(local_path):
        raise HTTPException(
            status_code=404, detail=f"Repository '{repo_name}' not found locally. Please ingest it first.")

    try:
        # Build the graph data
        graph_data = build_repo_graph(local_path)

        # Pass to Gemini to convert into Mermaid syntax
        mermaid_syntax = generate_mermaid_diagram(graph_data)

        return {"mermaid_syntax": mermaid_syntax}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
