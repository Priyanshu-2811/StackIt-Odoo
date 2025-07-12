from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, models, database
from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/auth")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(form: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, form.email)
    if not user or not crud.verify_password(form.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}