from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models, database
from ..auth_utils import get_current_user

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/", response_model=schemas.QuestionOut)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new question"""
    return crud.create_question(db=db, question=question, user_id=current_user.id)

@router.get("/", response_model=List[schemas.QuestionOut])
def get_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """Get all questions with pagination"""
    return crud.get_questions(db=db, skip=skip, limit=limit)

@router.get("/{question_id}", response_model=schemas.QuestionWithAnswers)
def get_question(
    question_id: int,
    db: Session = Depends(database.get_db)
):
    """Get a specific question with its answers"""
    question = crud.get_question_by_id(db=db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return question

@router.put("/{question_id}", response_model=schemas.QuestionOut)
def update_question(
    question_id: int,
    question_data: schemas.QuestionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a question (only by owner or admin)"""
    question = crud.get_question_by_id(db=db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this question"
        )
    
    updated_question = crud.update_question(db=db, question_id=question_id, question_data=question_data)
    return updated_question

@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a question (only by owner or admin)"""
    question = crud.get_question_by_id(db=db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this question"
        )
    
    crud.delete_question(db=db, question_id=question_id)
    return {"message": "Question deleted successfully"}

@router.get("/user/{user_id}", response_model=List[schemas.QuestionOut])
def get_user_questions(
    user_id: int,
    db: Session = Depends(database.get_db)
):
    """Get all questions by a specific user"""
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return crud.get_questions_by_user(db=db, user_id=user_id)
