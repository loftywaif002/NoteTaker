from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Note
from schemas import NoteCreate, NoteOut, NoteUpdate
from database import get_db
from mcp_client import summarize_and_tag, index_note, delete_note_index, semantic_search
from config import settings
import json


router = APIRouter()

def _tags_to_json(tags: List[str]) -> str:
    try:
        return json.dumps(tags or [])
    except Exception:
        return "[]"
def _json_to_tags(tags_json: Optional[str]) -> List[str]:
    if not tags_json:
        return []
    try:
        val = json.loads(tags_json)
        return val if isinstance(val, list) else []
    except Exception:
        return []
def _note_to_out(note: Note) -> NoteOut:
    return NoteOut(
        id=note.id,
        title=note.title,
        content=note.content,
        tags=_json_to_tags(note.tags_json),
        summary=note.summary,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )

@router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)

def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    summary = None
    tags = payload.tags or []
    if settings.AUTOSUMMARIZE_ON_CREATE and payload.auto_summarize:
        result = summarize_and_tag(f"{payload.title}\n\n{payload.content}")
        if result.get("summary"):
            summary = result["summary"]
        if result.get("tags"):
            tags = list({*tags, *result["tags"]})
    note = Note(
        title=payload.title,
        content=payload.content,
        tags_json=_tags_to_json(tags),
        summary=summary,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    index_note(
        note_id=note.id,
        text=f"{note.title}\n\n{note.content}",
        metadata={"tags": tags}
    )
    return _note_to_out(note)

@router.get("/notes", response_model=List[NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Simple title/content substring search"),
    skip: int = 0,
    limit: int = Query(50, le=200)
):
    query = db.query(Note)
    if q:
        like = f"%{q}%"
        query = query.filter((Note.title.ilike(like)) | (Note.content.ilike(like)))
    notes = query.order_by(Note.created_at.desc()).offset(skip).limit(limit).all()
    return [_note_to_out(n) for n in notes]

@router.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: str, db: Session = Depends(get_db)):
    note = db.query(Note).get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return _note_to_out(note)

@router.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: str, payload: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    if payload.tags is not None:
        note.tags_json = _tags_to_json(payload.tags)
    if settings.AUTOSUMMARIZE_ON_UPDATE and payload.auto_summarize and (payload.title is not None or payload.content is not None):
        result = summarize_and_tag(f"{note.title}\n\n{note.content}")
        if result.get("summary"):
            note.summary = result["summary"]
        if result.get("tags"):
            existing = set(_json_to_tags(note.tags_json))
            merged = list(existing.union(set(result["tags"])))
            note.tags_json = _tags_to_json(merged)
    db.commit()
    db.refresh(note)
    index_note(
        note_id=note.id,
        text=f"{note.title}\n\n{note.content}",
        metadata={"tags": _json_to_tags(note.tags_json)}
    )
    return _note_to_out(note)

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_endpoint(note_id: str, db: Session = Depends(get_db)):
    note = db.query(Note).get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note)
    db.commit()
    delete_note_index(note_id)
    return

@router.post("/notes/search", response_model=List[NoteOut])
def semantic_search_notes(
    query: str = Query(..., description="Natural language query"),
    k: int = Query(10, le=50, description="Max results"),
    db: Session = Depends(get_db),
):
    results = semantic_search(query, k=k)
    if not results:
        return []
    ids = [r.get("id") for r in results if r.get("id")]
    if not ids:
        return []
    notes = db.query(Note).filter(Note.id.in_(ids)).all()
    order = {nid: i for i, nid in enumerate(ids)}
    notes.sort(key=lambda n: order.get(n.id, 10_000))
    return [_note_to_out(n) for n in notes]



