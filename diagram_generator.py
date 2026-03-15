import os
import json
import google.generativeai as genai

# Use the working alias you successfully tested in chat_engine
model = genai.GenerativeModel('gemini-3-flash-preview')


def generate_mermaid_diagram(graph_data: dict) -> str:
    system_prompt = """You are an expert software architect. Convert the following JSON dictionary of file dependencies (nodes and edges) into a Mermaid.js flowchart. Use 'graph TD'. Use valid Mermaid syntax. Return ONLY the raw Mermaid code. Do not include markdown formatting like ```mermaid, do not include explanations, and do not include the word 'mermaid' at the beginning. Just the raw syntax."""

    # Convert the Python dictionary to a formatted JSON string
    graph_json = json.dumps(graph_data, indent=2)

    prompt = f"{system_prompt}\nGraph Data:\n{graph_json}"

    response = model.generate_content(prompt)

    # Clean up the response in case the LLM still returns markdown formatting
    return response.text.strip().replace('```mermaid', '').replace('```', '').strip()
