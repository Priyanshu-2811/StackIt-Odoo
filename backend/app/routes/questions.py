from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Question
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()

@router.post("/")
def create_question(title: str, description: str, tags: str, user_id: int, db: Session = Depends(get_db)):
    q = Question(title=title, description=description, tags=tags, user_id=user_id, created_at=datetime.utcnow())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q