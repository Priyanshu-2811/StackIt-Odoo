from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth, questions, answers, comments, notifications, votes, ai
from .routes import auth, questions, answers, comments


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StackIt API",
    description="A Stack Overflow-like Q&A platform API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(comments.router)
app.include_router(notifications.router)
app.include_router(votes.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"msg": "StackIt API Running!"}

@app.get("/")
def root():
    return {"msg": "StackIt API Running! 🚀", "docs": "/docs", "redoc": "/redoc"}

