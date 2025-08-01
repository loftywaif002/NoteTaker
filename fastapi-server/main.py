from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers.notes import router as notes_router
from config import settings

app = FastAPI(title="Smart Notes API", version="0.1.0")


# CORS for your Next.js UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create tables on startup (simple dev path; for prod, use Alembic)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}
app.include_router(notes_router, prefix="/api", tags=["notes"])