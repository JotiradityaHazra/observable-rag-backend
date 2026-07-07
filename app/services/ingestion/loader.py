import logging
import time
# pyrefly: ignore [missing-import]
from pypdf import PdfReader
# pyrefly: ignore [missing-import]
from google import genai
from app.core.config import GEMINI_API_KEY

import os

logger = logging.getLogger(__name__)

def load_pdf_with_gemini(file_path: str) -> str:
    """Uses Gemini 1.5 Flash/Pro to extract text and describe images from a PDF."""
    if not GEMINI_API_KEY:
        raise ValueError("No Gemini API key configured.")

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )
    
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    logger.info(f"Uploading {file_path} to Gemini for OCR extraction...")
    uploaded_file = client.files.upload(file=file_path)
    
    logger.info("PDF processed. Generating multi-modal transcription...")
    prompt = (
        "You are an advanced document parser. Read this entire document and extract all the text. "
        "Maintain the original structure and formatting (use Markdown). "
        "CRITICAL: If you encounter any images, charts, diagrams, or screenshots, write a detailed description "
        "of what the image contains so that it can be indexed and searched by text later. "
        "Do not leave out any details."
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_file, prompt]
    )
    
    # Clean up the file from Google's servers
    client.files.delete(name=uploaded_file.name)
    
    return response.text

def load_pdf(file_path: str):
    try:
        # Attempt advanced Vision OCR extraction
        text = load_pdf_with_gemini(file_path)
        logger.info("Successfully extracted PDF using Gemini Vision.")
        return text
    except Exception as e:
        logger.warning(f"Gemini Vision extraction failed ({e}). Falling back to pypdf...")
        
        file_path = os.path.abspath(file_path)
        # Fallback to standard digital text extraction
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
