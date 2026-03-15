import ast
import os


def get_python_imports(file_path: str) -> list[str]:
    """Reads a Python file, parses it using AST, and extracts module names."""
    imports = []

    # Use utf-8 and ignore errors to prevent crashes on non-standard encodings
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return imports

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError:
        # Skip files with syntax errors that ast cannot parse
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # alias.name contains the imported module name
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    # Remove duplicates and return
    return list(set(imports))
