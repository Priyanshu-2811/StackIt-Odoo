from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models, database
from ..auth_utils import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/answer/{answer_id}", response_model=schemas.CommentOut)
def create_comment(
    answer_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new comment for an answer"""
    # Check if answer exists
    answer = crud.get_answer_by_id(db=db, answer_id=answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    return crud.create_comment(db=db, comment=comment, answer_id=answer_id, user_id=current_user.id)

@router.get("/answer/{answer_id}", response_model=List[schemas.CommentOut])
def get_comments_for_answer(
    answer_id: int,
    db: Session = Depends(database.get_db)
):
    """Get all comments for a specific answer"""
    answer = crud.get_answer_by_id(db=db, answer_id=answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    return crud.get_comments_by_answer(db=db, answer_id=answer_id)

@router.get("/{comment_id}", response_model=schemas.CommentOut)
def get_comment(
    comment_id: int,
    db: Session = Depends(database.get_db)
):
    """Get a specific comment"""
    comment = crud.get_comment_by_id(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return comment

@router.put("/{comment_id}", response_model=schemas.CommentOut)
def update_comment(
    comment_id: int,
    comment_data: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a comment (only by owner or admin)"""
    comment = crud.get_comment_by_id(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this comment"
        )
    
    updated_comment = crud.update_comment(db=db, comment_id=comment_id, content=comment_data.content)
    return updated_comment

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a comment (only by owner or admin)"""
    comment = crud.get_comment_by_id(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this comment"
        )
    
    crud.delete_comment(db=db, comment_id=comment_id)
    return {"message": "Comment deleted successfully"}
