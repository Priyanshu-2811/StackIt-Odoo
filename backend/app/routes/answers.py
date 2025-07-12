from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Answer
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_answers(db: Session = Depends(get_db)):
    return db.query(Answer).all()

@router.post("/")
def create_answer(question_id: int, content: str, user_id: int, db: Session = Depends(get_db)):
    a = Answer(question_id=question_id, content=content, user_id=user_id, created_at=datetime.utcnow())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a