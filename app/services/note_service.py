from fastapi import HTTPException, status # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate


# Create Note
def create_note(
    db: Session,
    user_id: int,
    note: NoteCreate
):
    db_note = Note(
        title=note.title,
        content=note.content,
        owner_id=user_id
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


# Get Notes (Paginated)
def get_notes(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Note)
        .filter(Note.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# Get Note By ID
def get_note_by_id(
    db: Session,
    current_user: User,
    note_id: int
):
    query = db.query(Note).filter(Note.id == note_id)

    note = query.first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    if (
        current_user.role != "admin"
        and note.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this note"
        )

    return note


# Update Note
def update_note(
    db: Session,
    current_user: User,
    note_id: int,
    note_data: NoteUpdate
):
    note = get_note_by_id(
        db,
        current_user,
        note_id
    )

    update_data = note_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    return note


# Delete Note
def delete_note(
    db: Session,
    current_user: User,
    note_id: int
):
    note = get_note_by_id(
        db,
        current_user,
        note_id
    )

    db.delete(note)
    db.commit()

    return True