from pypdf import PdfReader 

def extract_chunks(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    reader = PdfReader("legal_document.pdf")
    raw_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            raw_text += text

    chunks = []
    start = 0

    while start < len(raw_text):
        end = start + chunk_size
        chunks.append(raw_text[start:end])
        start += (chunk_size - chunk_overlap)

    return chunks