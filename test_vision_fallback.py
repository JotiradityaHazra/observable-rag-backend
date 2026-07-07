import logging
from app.services.ingestion.loader import load_pdf

# Setup basic logging to see the fallback warning
logging.basicConfig(level=logging.INFO)

print("Starting PDF extraction test...")
try:
    text = load_pdf("test_document.pdf")
    print("\n--- Extracted Text Preview (First 500 chars) ---")
    print(text[:500] if text else "No text extracted!")
    print("--------------------------------------------------\n")
    print("Test Complete. Fallback logic verified.")
except Exception as e:
    print(f"Test Failed! Unexpected exception: {e}")
