from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services import note_service
from app.models.user import User

# Initialize router
router = APIRouter()

# Create note
@router.post("/", response_model=NoteResponse)
def create_note_api(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.create_note(db, current_user, note)

# Get all notes
@router.get("/", response_model=List[NoteResponse])
def get_notes_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = (page - 1) * limit
    return note_service.get_notes(db, current_user, skip, limit)

# Get Note by ID
@router.get("/{note_id}", response_model=NoteResponse)
def get_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.get_note_by_id(db, current_user, note_id)

# Update note
@router.put("/{note_id}", response_model=NoteResponse)
def update_note_api(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.update_note(db, current_user, note_id, note_data)

# Delete note
@router.delete("/{note_id}")
def delete_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.delete_note(db, current_user, note_id)


