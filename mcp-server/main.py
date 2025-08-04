from fastapi import FastAPI
from schemas import *
from summarizer import summarize_and_tag
from vectorstore import index_note, delete_note, search

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    result = summarize_and_tag(req.text)
    return SummarizeResponse(**result)

@app.post("/index")
def index(req: IndexRequest):
    index_note(id=req.id, text=req.text, metadata=req.metadata or {})
    return {"ok": True}

@app.post("/delete")
def delete(req: DeleteRequest):
    delete_note(req.id)
    return {"ok": True}

@app.post("/search", response_model=SearchResponse)
def search_notes(req: SearchRequest):
    results = search(req.query, k=req.k)
    return SearchResponse(results=[SearchResult(**r) for r in results])