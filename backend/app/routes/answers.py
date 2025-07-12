from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models, database
from ..auth_utils import get_current_user

router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/question/{question_id}", response_model=schemas.AnswerOut)
def create_answer(
    question_id: int,
    answer: schemas.AnswerCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new answer for a question"""
    # Check if question exists
    question = crud.get_question_by_id(db=db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return crud.create_answer(db=db, answer=answer, question_id=question_id, user_id=current_user.id)

@router.get("/question/{question_id}", response_model=List[schemas.AnswerWithComments])
def get_answers_for_question(
    question_id: int,
    db: Session = Depends(database.get_db)
):
    """Get all answers for a specific question"""
    question = crud.get_question_by_id(db=db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return crud.get_answers_by_question(db=db, question_id=question_id)

@router.get("/{answer_id}", response_model=schemas.AnswerWithComments)
def get_answer(
    answer_id: int,
    db: Session = Depends(database.get_db)
):
    """Get a specific answer with its comments"""
    answer = crud.get_answer_by_id(db=db, answer_id=answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    return answer

@router.put("/{answer_id}", response_model=schemas.AnswerOut)
def update_answer(
    answer_id: int,
    answer_data: schemas.AnswerCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update an answer (only by owner or admin)"""
    answer = crud.get_answer_by_id(db=db, answer_id=answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    if answer.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this answer"
        )
    
    updated_answer = crud.update_answer(db=db, answer_id=answer_id, answer_data=answer_data)
    return updated_answer

@router.post("/{answer_id}/accept", response_model=schemas.AnswerOut)
def accept_answer(
    answer_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Accept an answer (only by question owner or admin)"""
    answer = crud.get_answer_by_id(db=db, answer_id=answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    question = crud.get_question_by_id(db=db, question_id=answer.question_id)
    if question.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the question owner can accept answers"
        )
    
    accepted_answer = crud.accept_answer(db=db, answer_id=answer_id)
    return accepted_answer

@router.delete("/{answer_id}")
def delete_answer(
    answer_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete an answer (only by owner or admin)"""
    answer = crud.get_answer_by_id(db=db, answer_id=answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    if answer.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this answer"
        )
    
    crud.delete_answer(db=db, answer_id=answer_id)
    return {"message": "Answer deleted successfully"}
