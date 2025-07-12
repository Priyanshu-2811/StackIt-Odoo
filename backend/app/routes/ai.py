from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Question, User
from ..auth_utils import get_current_user
from ..crud import create_answer
from .. import schemas
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ai", tags=["ai"])

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@router.post("/answer/{question_id}")
async def generate_ai_answer(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate an AI answer for a question using Gemini"""
    
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured"
        )
    
    # Get the question
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare prompt for the question
        prompt = f"""
        You are a helpful programming assistant. Please provide a detailed and accurate answer to the following question:
        
        Title: {question.title}
        Description: {question.description}
        Tags: {question.tags}
        
        Please provide:
        1. A clear explanation of the problem
        2. A step-by-step solution
        3. Code examples if applicable
        4. Best practices and recommendations
        
        Format your response in a clear, structured way that would be helpful for a developer.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        ai_answer = response.text
        
        # Create the answer in the database
        answer_data = schemas.AnswerCreate(
            content=ai_answer,
            question_id=question_id
        )
        
        # Create a special AI user or use current user with AI tag
        created_answer = create_answer(db=db, answer=answer_data, user_id=current_user.id)
        
        return {
            "success": True,
            "answer_id": created_answer.id,
            "content": ai_answer,
            "message": "AI answer generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating AI answer: {str(e)}"
        )

@router.post("/suggest/{question_id}")
async def suggest_ai_improvement(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Suggest improvements to make the question clearer"""
    
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured"
        )
    
    # Get the question
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare prompt for suggestions
        prompt = f"""
        Please analyze this programming question and suggest improvements to make it clearer and more likely to get good answers:
        
        Title: {question.title}
        Description: {question.description}
        Tags: {question.tags}
        
        Please provide:
        1. Assessment of the question clarity
        2. Suggestions for improving the title
        3. Suggestions for improving the description
        4. Recommended additional information to include
        5. Better tag suggestions if applicable
        
        Be constructive and helpful.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        suggestions = response.text
        
        return {
            "success": True,
            "suggestions": suggestions,
            "message": "AI suggestions generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating suggestions: {str(e)}"
        )
