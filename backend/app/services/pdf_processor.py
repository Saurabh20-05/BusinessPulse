from io import BytesIO

from pypdf import PdfReader


# Keep chunks small enough for embedding and retrieval
CHUNK_SIZE = 1200

# Keep some previous text so important context is not lost between chunks
CHUNK_OVERLAP = 200


def extract_pdf_text(file_data: bytes) -> str:
    # Read the PDF directly from the bytes stored in GridFS
    reader = PdfReader(BytesIO(file_data))

    pages = []

    # Extract text from every page
    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text.strip())

    # Combine all extracted pages into one text block
    return "\n\n".join(pages)


def split_text_into_chunks(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    # Remove unnecessary whitespace before splitting the text
    text = " ".join(text.split())

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    chunks = []
    start = 0

    # Split the document into overlapping sections
    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def process_pdf(file_data: bytes) -> dict:
    # Extract readable text from the PDF
    text = extract_pdf_text(file_data)

    if not text:
        raise ValueError(
            "No readable text was found in the PDF."
        )

    # Split the extracted text into smaller sections for later retrieval
    chunks = split_text_into_chunks(text)

    if not chunks:
        raise ValueError(
            "The PDF could not be split into text chunks."
        )

    return {
        "text": text,
        "chunks": chunks,
        "page_count": len(
            PdfReader(BytesIO(file_data)).pages
        ),
        "chunk_count": len(chunks),
    }