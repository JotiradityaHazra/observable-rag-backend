import logging
import sys
from app.services.ingestion.loader import load_pdf

# Setup logging
logging.basicConfig(level=logging.INFO)

print("Starting PDF extraction test on Kubernetes.pdf...")
try:
    text = load_pdf("Kubernetes.pdf")
    
    with open("test_output.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    print("\n--- Extracted Text Preview (First 1500 chars) ---")
    try:
        print(text[:1500] if text else "No text extracted!")
    except UnicodeEncodeError:
        print(text[:1500].encode('cp1252', errors='replace').decode('cp1252'))
    print("\n--------------------------------------------------")
    print(f"Total length extracted: {len(text)} characters.")
    print("Full output saved to test_output.txt")
except Exception as e:
    print(f"Test Failed! Unexpected exception: {e}")
