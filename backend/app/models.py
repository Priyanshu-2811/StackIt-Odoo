from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    questions = relationship("Question", back_populates="owner")
    answers = relationship("Answer", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    tags = Column(String(255))
    image_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    image_url = Column(String, nullable=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    question = relationship("Question", back_populates="answers")
    owner = relationship("User", back_populates="answers")
    comments = relationship("Comment", back_populates="answer")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500))
    answer_id = Column(Integer, ForeignKey("answers.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    answer = relationship("Answer", back_populates="comments")
    owner = relationship("User", back_populates="comments")