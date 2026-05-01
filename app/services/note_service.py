from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate


# Helper: get user from email
def get_user(db: Session, user_email: str) -> User:
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# Create Note
def create_note(db: Session, user_email: str, note_data: NoteCreate):
    user = get_user(db, user_email)

    note = Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=user.id  
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


# Get all notes
def get_notes(db: Session, user_email: str):
    user = get_user(db, user_email)

    return db.query(Note).filter(Note.owner_id == user.id).all()


# Get note by ID
def get_note_by_id(db: Session, user_email: str, note_id: int):
    user = get_user(db, user_email)

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    # Ownership check
    if user.role != "admin" and note.owner_id != user.id: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this note"
        )

    return note


# Update note
def update_note(db: Session, user_email: str, note_id: int, note_data: NoteUpdate):
    note = get_note_by_id(db, user_email, note_id)

    if note_data.title is not None:
        note.title = note_data.title

    if note_data.content is not None:
        note.content = note_data.content

    db.commit()
    db.refresh(note)

    return note


# Delete note
def delete_note(db: Session, user_email: str, note_id: int):
    note = get_note_by_id(db, user_email, note_id)

    db.delete(note)
    db.commit()

    return True