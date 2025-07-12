from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Comment
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()

@router.post("/")
def create_comment(answer_id: int, content: str, is_from_ai: bool = False, db: Session = Depends(get_db)):
    c = Comment(answer_id=answer_id, content=content, is_from_ai=is_from_ai, created_at=datetime.utcnow())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c