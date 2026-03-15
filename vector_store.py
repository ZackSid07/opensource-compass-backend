import os
from database import supabase
from sentence_transformers import SentenceTransformer
from chunker import chunk_file_content

# Initialize the model at the top of the file so it loads once on startup
model = SentenceTransformer('all-MiniLM-L6-v2')


def embed_and_store_repo(repo_name: str, repo_path: str) -> int:
    """
    Reads all .py files in the repo, chunks them, generates embeddings,
    and stores them in the Supabase code_chunks table.
    Returns the total number of chunks processed.
    """
    total_chunks = 0
    if not supabase:
        print("Supabase client is not initialized. Please check your .env variables.")
        return 0

    for root, _, files in os.walk(repo_path):
        # Skip .git directory and virtual environment
        if '.git' in root or 'venv' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                # Make the node name relative to the repo path for cleaner db records
                rel_path = os.path.relpath(file_path, repo_path)
                # Replace backslashes with forward slashes for cross-platform consistency
                rel_path = rel_path.replace('\\', '/')

                # Read content safely
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue

                # Chunk content
                chunks = chunk_file_content(content)

                for chunk in chunks:
                    # Generate embedding (tolist required as supabase expects a standard python list of floats)
                    embedding = model.encode(chunk).tolist()

                    # Insert into Supabase
                    try:
                        record = {
                            "repo_name": repo_name,
                            "file_path": rel_path,
                            "content": chunk,
                            "embedding": embedding
                        }

                        # Note: supabase-py requires execution of the query builder to perform the insert
                        supabase.table("code_chunks").insert(record).execute()
                        total_chunks += 1
                    except Exception as e:
                        print(f"Error inserting chunk for {rel_path}: {e}")

    return total_chunks


def search_codebase(query: str, match_count: int = 3):
    """Encodes the query and searches the Supabase code_chunks table."""
    if not supabase:
        print("Supabase client is not initialized.")
        return []

    query_embedding = model.encode(query).tolist()

    response = supabase.rpc(
        "match_code_chunks",
        {
            "query_embedding": query_embedding,
            "match_threshold": 0.3,
            "match_count": match_count
        }
    ).execute()

    return response.data
