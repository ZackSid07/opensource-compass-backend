from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_file_content(content: str) -> list[str]:
    """Splits a string of code into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return splitter.split_text(content)
