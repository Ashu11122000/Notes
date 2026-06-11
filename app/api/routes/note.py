from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Query  # type: ignore[import]
from sqlalchemy.orm import Session # type: ignore

from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services import note_service

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


# Create Note
@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED
)
def create_note_api(
    note: NoteCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    return note_service.create_note(
        db=db,
        user_id=user_id,
        note=note
    )


# Get All Notes
@router.get(
    "",
    response_model=List[NoteResponse]
)
def get_notes_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    offset = (page - 1) * limit

    return note_service.get_notes(
        db=db,
        user_id=user_id,
        skip=offset,
        limit=limit
    )


# Get Note By ID
@router.get(
    "/{note_id}",
    response_model=NoteResponse
)
def get_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    note = note_service.get_note_by_id(
        db=db,
        user_id=user_id,
        note_id=note_id
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return note


# Update Note
@router.put(
    "/{note_id}",
    response_model=NoteResponse
)
def update_note_api(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    note = note_service.update_note(
        db=db,
        user_id=user_id,
        note_id=note_id,
        note_data=note_data
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return note


# Delete Note
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    deleted = note_service.delete_note(
        db=db,
        user_id=user_id,
        note_id=note_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return None