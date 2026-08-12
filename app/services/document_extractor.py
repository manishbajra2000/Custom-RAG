from pathlib import Path
import pymupdf
from fastapi import UploadFile

SUPPORTED_EXTENSIONS = {".pdf", ".txt"}

async def extract_text(file: UploadFile) -> str:
    if not file.filename:
        raise ValueError("Filename is missing.")

    suffix = Path(file.filename).suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {suffix}. Only PDF and TXT files are supported.")

    content = await file.read()

    if not content:
        raise ValueError("File is empty.")

    if suffix == ".txt":
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode TXT file. Ensure it is UTF-8 encoded.") from exc

    try:
        document = pymupdf.open(stream=content, filetype="pdf")

        text = "\n".join(page.get_text() for page in document)

        document.close()
        return text
    except Exception as exc:
        raise ValueError("Could not read the PDF file.") from exc
        