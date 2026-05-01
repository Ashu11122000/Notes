from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services import note_service

router = APIRouter(prefix="/notes", tags=["Notes"])


# Create note
@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note_api(
    note: NoteCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    return note_service.create_note(db, user_id, note)


# Get all notes (WITH pagination)
@router.get("", response_model=List[NoteResponse])
def get_notes_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    notes = note_service.get_notes(db, user_id)

    # Apply pagination safely
    start = (page - 1) * limit
    end = start + limit

    return notes[start:end]


# Get note by ID
@router.get("/{note_id}", response_model=NoteResponse)
def get_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    note = note_service.get_note_by_id(db, user_id, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# Update note
@router.put("/{note_id}", response_model=NoteResponse)
def update_note_api(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    note = note_service.update_note(db, user_id, note_id, note_data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# Delete note
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    success = note_service.delete_note(db, user_id, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return None