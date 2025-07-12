from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import bcrypt

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = bcrypt.hash(user.password)
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        password=hashed_pw,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def verify_password(plain, hashed):
    return bcrypt.verify(plain, hashed)

# Question CRUD
def create_question(db: Session, question: schemas.QuestionCreate, user_id: int):
    db_question = models.Question(**question.dict(), owner_id=user_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    # Get the question owner
    question_owner = get_user_by_id(db, user_id)
    
    # Send notifications to all other users (not the question owner)
    all_users = db.query(models.User).filter(models.User.id != user_id).all()
    for user in all_users:
        message = f"New question posted: '{db_question.title}' by {question_owner.username}"
        create_notification(
            db=db,
            user_id=user.id,
            message=message,
            notification_type="new_question",
            related_question_id=db_question.id
        )
    
    return db_question

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()

def get_question_by_id(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def get_questions_by_user(db: Session, user_id: int):
    return db.query(models.Question).filter(models.Question.owner_id == user_id).all()

def update_question(db: Session, question_id: int, question_data: schemas.QuestionCreate):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question:
        for key, value in question_data.dict().items():
            setattr(db_question, key, value)
        db.commit()
        db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
    return db_question

# Answer CRUD
def create_answer(db: Session, answer: schemas.AnswerCreate, question_id: int, user_id: int):
    db_answer = models.Answer(**answer.dict(), question_id=question_id, owner_id=user_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_answers_by_question(db: Session, question_id: int):
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()

def get_answer_by_id(db: Session, answer_id: int):
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

def update_answer(db: Session, answer_id: int, answer_data: schemas.AnswerCreate):
    db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if db_answer:
        for key, value in answer_data.dict().items():
            setattr(db_answer, key, value)
        db.commit()
        db.refresh(db_answer)
    return db_answer

def accept_answer(db: Session, answer_id: int):
    # First, unaccept all answers for this question
    db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if db_answer:
        # Unaccept all other answers for this question
        db.query(models.Answer).filter(
            models.Answer.question_id == db_answer.question_id
        ).update({"is_accepted": False})
        
        # Accept this answer
        db_answer.is_accepted = True
        db.commit()
        db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, answer_id: int):
    db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if db_answer:
        db.delete(db_answer)
        db.commit()
    return db_answer

# Comment CRUD
def create_comment(db: Session, comment: schemas.CommentCreate, answer_id: int, user_id: int):
    db_comment = models.Comment(content=comment.content, answer_id=answer_id, owner_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_answer(db: Session, answer_id: int):
    return db.query(models.Comment).filter(models.Comment.answer_id == answer_id).all()

def get_comment_by_id(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, content: str):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db_comment.content = content
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment

# Notification CRUD
def create_notification(db: Session, user_id: int, message: str, notification_type: str, 
                       related_question_id: int = None, related_answer_id: int = None):
    db_notification = models.Notification(
        user_id=user_id,
        message=message,
        type=notification_type,
        related_question_id=related_question_id,
        related_answer_id=related_answer_id
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notifications_by_user(db: Session, user_id: int):
    return db.query(models.Notification).filter(
        models.Notification.user_id == user_id
    ).order_by(models.Notification.created_at.desc()).all()

def mark_notification_read(db: Session, notification_id: int, user_id: int):
    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == user_id
    ).first()
    if db_notification:
        db_notification.is_read = True
        db.commit()
        db.refresh(db_notification)
    return db_notification

def mark_all_notifications_read(db: Session, user_id: int):
    db.query(models.Notification).filter(
        models.Notification.user_id == user_id,
        models.Notification.is_read == False
    ).update({"is_read": True})
    db.commit()

def delete_notification(db: Session, notification_id: int, user_id: int):
    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == user_id
    ).first()
    if db_notification:
        db.delete(db_notification)
        db.commit()
    return db_notification

# Vote CRUD
def create_or_update_vote(db: Session, user_id: int, answer_id: int, vote_type: str):
    # Check if vote already exists
    existing_vote = db.query(models.Vote).filter(
        models.Vote.user_id == user_id,
        models.Vote.answer_id == answer_id
    ).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote if same type
            db.delete(existing_vote)
            db.commit()
            return None, "removed"
        else:
            # Update vote type
            existing_vote.vote_type = vote_type
            db.commit()
            db.refresh(existing_vote)
            return existing_vote, "updated"
    else:
        # Create new vote
        new_vote = models.Vote(
            user_id=user_id,
            answer_id=answer_id,
            vote_type=vote_type
        )
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote, "created"

def get_vote_counts(db: Session, answer_id: int):
    upvotes = db.query(models.Vote).filter(
        models.Vote.answer_id == answer_id,
        models.Vote.vote_type == "upvote"
    ).count()
    
    downvotes = db.query(models.Vote).filter(
        models.Vote.answer_id == answer_id,
        models.Vote.vote_type == "downvote"
    ).count()
    
    return {"upvotes": upvotes, "downvotes": downvotes, "net_votes": upvotes - downvotes}

def get_user_vote(db: Session, user_id: int, answer_id: int):
    vote = db.query(models.Vote).filter(
        models.Vote.user_id == user_id,
        models.Vote.answer_id == answer_id
    ).first()
    return vote.vote_type if vote else None

# Authentication helper
def get_current_user(db: Session, token: str):
    """Get current user from JWT token"""
    from .auth_utils import verify_token
    try:
        payload = verify_token(token)
        if payload is None:
            return None
        user_id = payload.get("sub")
        if user_id is None:
            return None
        user = get_user_by_id(db, user_id=int(user_id))
        return user
    except Exception:
        return None
