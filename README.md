# NoteTaker
Simple CRUD app using MCP, Langchain, FastApi

### Architecture

+--------------+      REST / JSON       +---------------+       LLM + VectorDB
|              |  <------------------>  |               | <-->  LangChain / Llama.cpp / ChromaDB
|  FastAPI API |                        |  MCP Server   |
|              |                        |  (Python SDK) |
+--------------+                        +---------------+
       ↑                                         ↑
       |                                         |
       |              HTTP (REST)               |
       +----------------------------------------+
                         ↓
                  +--------------+
                  |              |
                  | Next.js UI   |
                  | (Carbon DS)  |
                  +--------------+

#### Data model
```
{
  "id": "uuid",
  "title": "string",
  "content": "string",
  "tags": ["string"],
  "summary": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```
