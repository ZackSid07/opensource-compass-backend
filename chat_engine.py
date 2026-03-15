import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-3-flash-preview')



def generate_explanation(query: str, search_results: list) -> str:
    # Combine search results into a single context string
    context_chunks = []
    for result in search_results:
        # result is likely a dict from Supabase RPC containing file_path and content
        file_path = result.get('file_path', 'Unknown file')
        content = result.get('content', '')
        context_chunks.append(f"--- File: {file_path} ---\n{content}\n")

    context = "\n".join(context_chunks)

    prompt = f"""You are OpenSource Compass, an AI mentor for junior developers. Use the following code snippets to answer the user's question clearly and simply. If the answer is not in the context, say you don't know based on the current codebase.

Context:
{context}


Question: {query}"""

    response = model.generate_content(prompt)
    return response.text
