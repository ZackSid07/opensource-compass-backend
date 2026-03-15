import os
import networkx as nx
from parser import get_python_imports


def build_repo_graph(repo_path: str) -> dict:
    """Builds a dependency graph of Python files in the given repository path."""
    G = nx.DiGraph()

    # First pass: collect all python files and add them as nodes
    for root, _, files in os.walk(repo_path):
        # Skip .git directory or venv to avoid noise
        if '.git' in root or 'venv' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                # Make the node name relative to the repo path for cleaner output
                rel_path = os.path.relpath(file_path, repo_path)
                # Replace backslashes with forward slashes for cross-platform consistency
                file_name = rel_path.replace('\\', '/')

                G.add_node(file_name)

                # Get the imports for this file
                imports = get_python_imports(file_path)

                # Add edges from this file to the imported modules
                for imp in imports:
                    G.add_edge(file_name, imp)

    # Format the graph data as requested
    return {
        "nodes": list(G.nodes),
        "edges": list(G.edges)
    }
