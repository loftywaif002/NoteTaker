from pydantic import BaseModel
from typing import List, Optional


class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    tags: List[str]

class IndexRequest(BaseModel):
    id: str
    text: str
    metadata: Optional[dict] = {}

class DeleteRequest(BaseModel):
    id: str

class SearchRequest(BaseModel):
    query: str
    k: int = 10

class SearchResult(BaseModel):
    id: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]