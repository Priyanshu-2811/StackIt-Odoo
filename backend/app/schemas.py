from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: Optional[bool] = False

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Question schemas
class QuestionCreate(BaseModel):
    title: str
    description: str
    tags: str
    image_url: Optional[str] = None

class QuestionOut(BaseModel):
    id: int
    title: str
    description: str
    tags: str
    image_url: Optional[str] = None
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionWithAnswers(QuestionOut):
    answers: List["AnswerOut"] = []

# Answer schemas
class AnswerCreate(BaseModel):
    content: str
    image_url: Optional[str] = None

class AnswerOut(BaseModel):
    id: int
    content: str
    image_url: Optional[str] = None
    question_id: int
    owner_id: int
    is_accepted: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnswerWithComments(AnswerOut):
    comments: List["CommentOut"] = []

# Comment schemas
class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    answer_id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Notification schemas
class NotificationResponse(BaseModel):
    id: int
    message: str
    type: str
    is_read: bool
    related_question_id: Optional[int] = None
    related_answer_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Vote schemas
class VoteCreate(BaseModel):
    answer_id: int
    vote_type: str  # 'upvote' or 'downvote'

class VoteResponse(BaseModel):
    message: str
    vote_type: Optional[str] = None

# Update forward references
QuestionWithAnswers.model_rebuild()
AnswerWithComments.model_rebuild()