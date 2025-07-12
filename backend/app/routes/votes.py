from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Vote, Answer, User, Notification
from ..schemas import VoteCreate, VoteResponse
from ..auth_utils import get_current_user
from .notifications import create_notification

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("/", response_model=VoteResponse)
async def create_vote(
    vote: VoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update a vote on an answer"""
    # Check if answer exists
    answer = db.query(Answer).filter(Answer.id == vote.answer_id).first()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    # Check if user is trying to vote on their own answer
    if answer.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot vote on your own answer"
        )
    
    # Check if user has already voted on this answer
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.answer_id == vote.answer_id
    ).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote.vote_type:
            # Remove vote if clicking the same vote type
            db.delete(existing_vote)
            db.commit()
            return {"message": "Vote removed", "vote_type": None}
        else:
            # Update vote type
            existing_vote.vote_type = vote.vote_type
            db.commit()
            
            # Create notification for vote change
            if vote.vote_type == "upvote":
                create_notification(
                    db=db,
                    user_id=answer.owner_id,
                    message=f"{current_user.username} upvoted your answer",
                    notification_type="vote",
                    related_answer_id=answer.id,
                    related_question_id=answer.question_id
                )
            
            return {"message": "Vote updated", "vote_type": vote.vote_type}
    
    # Create new vote
    new_vote = Vote(
        user_id=current_user.id,
        answer_id=vote.answer_id,
        vote_type=vote.vote_type
    )
    db.add(new_vote)
    db.commit()
    
    # Create notification for new upvote
    if vote.vote_type == "upvote":
        create_notification(
            db=db,
            user_id=answer.owner_id,
            message=f"{current_user.username} upvoted your answer",
            notification_type="vote",
            related_answer_id=answer.id,
            related_question_id=answer.question_id
        )
    
    return {"message": "Vote created", "vote_type": vote.vote_type}

@router.get("/answer/{answer_id}")
async def get_answer_votes(
    answer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get vote statistics for an answer"""
    # Check if answer exists
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    upvotes = db.query(Vote).filter(
        Vote.answer_id == answer_id,
        Vote.vote_type == "upvote"
    ).count()
    
    downvotes = db.query(Vote).filter(
        Vote.answer_id == answer_id,
        Vote.vote_type == "downvote"
    ).count()
    
    # Check user's vote
    user_vote = db.query(Vote).filter(
        Vote.answer_id == answer_id,
        Vote.user_id == current_user.id
    ).first()
    
    return {
        "upvotes": upvotes,
        "downvotes": downvotes,
        "net_votes": upvotes - downvotes,
        "user_vote": user_vote.vote_type if user_vote else None
    }
