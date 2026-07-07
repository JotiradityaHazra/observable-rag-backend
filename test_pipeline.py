import requests

# 2. Test Ingestion (Semantic Chunking)
print("1. Uploading Kubernetes.pdf to /ingest endpoint (Semantic Chunking)...")
with open("Kubernetes.pdf", "rb") as f:
    files = {"file": ("Kubernetes.pdf", f, "application/pdf")}
    data = {"chunk_strategy": "semantic"}
    response = requests.post("http://localhost:8000/ingest", files=files, data=data)
    
print(f"   Status Code: {response.status_code}")
try:
    print(f"   Response: {response.json()}\n")
except:
    print(f"   Response: {response.text}\n")

# 3. Test Retrieval & Reranking via /chat
print("2. Querying /chat endpoint (Testing Reranker)...")
# Note: This will likely return 500 because your Gemini key is invalid, 
# but it WILL trigger the local Reranker before it crashes!
payload = {
    "query": "What is Kubernetes?",
    "chunk_strat": "semantic"
}
chat_response = requests.post("http://localhost:8000/chat", json=payload)
print(f"   Status Code: {chat_response.status_code}")
try:
    print(f"   Response: {chat_response.json()}\n")
except:
    print(f"   Response: {chat_response.text}\n")
