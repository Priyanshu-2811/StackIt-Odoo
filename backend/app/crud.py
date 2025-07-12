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
