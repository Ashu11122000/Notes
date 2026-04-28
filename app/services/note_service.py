from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.models.user import User

# Create Note
def create_note(db: Session, user: User, note_data: NoteCreate):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        user_id=user.id  # ownership enforced here
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note

# Get all notes

def create_note(db: Session, user: User, note_data: NoteCreate):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        user_id=user.id  # ownership enforced here
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note

# Get Note by id
def get_note_by_id(db: Session, user: User, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    # Ownership check
    if user.role != "admin" and note.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this note"
        )

    return note

# Update Note
def update_note(
    db: Session,
    user: User,
    note_id: int,
    note_data: NoteUpdate
):
    note = get_note_by_id(db, user, note_id)

    # Partial update
    if note_data.title is not None:
        note.title = note_data.title

    if note_data.content is not None:
        note.content = note_data.content

    db.commit()
    db.refresh(note)

    return note

# Delete note
def delete_note(db: Session, user: User, note_id: int):
    note = get_note_by_id(db, user, note_id)

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}

