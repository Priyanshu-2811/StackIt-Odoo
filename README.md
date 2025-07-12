# 🚀 StackIt - Q&A Platform

A modern, full-stack Q&A platform built with FastAPI, React 19, and AI-powered assistance. Think Stack Overflow but with integrated AI help and modern UI/UX.

![StackIt Logo](https://via.placeholder.com/800x200/3B82F6/ffffff?text=StackIt+-+Q%26A+Platform)

## ✨ Features

### 🔐 Authentication & User Management
- **JWT-based authentication** with secure token handling
- **User registration and login** with email validation
- **Role-based access control** (Guest, User, Admin)
- **Password hashing** with bcrypt for security
- **Session management** with automatic token refresh

### 💬 Q&A System
- **Rich text editor** with React Quill for formatted questions and answers
- **Tagging system** with hashtag support and suggestions
- **Question management** (create, edit, delete, view)
- **Answer system** with acceptance mechanism
- **Comment threads** on answers
- **Voting system** for questions and answers

### 🤖 AI-Powered Assistance
- **Gemini AI integration** for automated question answering
- **Question improvement suggestions** from AI
- **Smart content generation** for comprehensive answers
- **AI-powered recommendations** for better question formatting

### 🔔 Real-time Notifications
- **Instant notifications** for new questions, answers, and comments
- **User mention system** with @username tagging
- **Notification center** with read/unread status
- **Email notifications** (configurable)

### 🎨 Modern UI/UX
- **Responsive design** with Tailwind CSS 4
- **Dark/light theme** support
- **Mobile-first approach** for all devices
- **Smooth animations** and transitions
- **Accessible components** following WCAG guidelines

### 🛠 Technical Features
- **RESTful API** with comprehensive documentation
- **Real-time updates** with optimistic UI
- **File upload support** with Cloudinary integration
- **Search functionality** with filters
- **Pagination** for performance
- **Error handling** with user-friendly messages

## 🏗 Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration & connection
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # Database operations
│   ├── auth_utils.py        # Authentication utilities
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── questions.py     # Question CRUD operations
│   │   ├── answers.py       # Answer management
│   │   ├── comments.py      # Comment system
│   │   ├── notifications.py # Notification system
│   │   ├── votes.py         # Voting system
│   │   └── ai.py            # AI integration endpoints
│   └── .env                 # Environment variables
├── requirements.txt         # Python dependencies
└── stackit.db              # SQLite database
```

### Frontend (React 19 + Vite)
```
frontend/
├── src/
│   ├── api/
│   │   └── api.js           # Axios configuration & interceptors
│   ├── components/
│   │   ├── AuthLayout.jsx   # Authentication page layout
│   │   ├── Navbar.jsx       # Navigation component
│   │   ├── QuestionCard.jsx # Question display card
│   │   ├── AnswerCard.jsx   # Answer display component
│   │   ├── RichTextEditor.jsx # Rich text editing
│   │   ├── TagInput.jsx     # Tag input with suggestions
│   │   ├── VotingComponent.jsx # Upvote/downvote system
│   │   ├── AIAssistant.jsx  # AI-powered assistance
│   │   └── Notification.jsx # Notification dropdown
│   ├── context/
│   │   └── AuthContext.jsx  # Global authentication state
│   ├── pages/
│   │   ├── Home.jsx         # Question listing page
│   │   ├── QuestionDetail.jsx # Question view with answers
│   │   ├── AskQuestion.jsx  # Question creation form
│   │   ├── Login.jsx        # Login form
│   │   └── Register.jsx     # Registration form
│   ├── App.jsx              # Main application component
│   └── main.jsx             # React application entry point
├── package.json             # Node.js dependencies
├── vite.config.js           # Vite configuration
└── tailwind.config.js       # Tailwind CSS configuration
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** for backend
- **Node.js 18+** for frontend
- **npm or yarn** package manager
- **Gemini API key** (optional, for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Priyanshu-2811/StackIt-Odoo.git
   cd StackIt-Odoo
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   .\venv\Scripts\Activate.ps1
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   
   # Run database migrations (creates tables)
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   
   # Start the server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Setup**
   ```bash
   # In a new terminal
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

4. **Access the application**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./stackit.db

# Security
SECRET_KEY=your_super_secret_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Integration (Optional)
GEMINI_API_KEY=your_gemini_api_key_here

# File Upload (Optional)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Email Configuration (Future)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Frontend Configuration

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=StackIt
```

## � API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user profile

### Questions
- `GET /questions/` - List all questions (with pagination)
- `POST /questions/` - Create new question
- `GET /questions/{id}` - Get question details with answers
- `PUT /questions/{id}` - Update question (owner/admin only)
- `DELETE /questions/{id}` - Delete question (owner/admin only)

### Answers
- `POST /answers/` - Create answer for question
- `GET /answers/{id}` - Get specific answer
- `PUT /answers/{id}` - Update answer (owner/admin only)
- `POST /answers/{id}/accept` - Accept answer (question owner only)
- `DELETE /answers/{id}` - Delete answer (owner/admin only)

### Comments
- `POST /comments/` - Create comment on answer
- `GET /comments/answer/{answer_id}` - Get comments for answer
- `PUT /comments/{id}` - Update comment (owner/admin only)
- `DELETE /comments/{id}` - Delete comment (owner/admin only)

### Notifications
- `GET /notifications/` - Get user notifications
- `PUT /notifications/{id}/read` - Mark notification as read
- `PUT /notifications/mark-all-read` - Mark all notifications as read

### Voting
- `POST /votes/` - Vote on answer (upvote/downvote)
- `DELETE /votes/{id}` - Remove vote

### AI Features
- `POST /ai/answer/{question_id}` - Generate AI answer
- `POST /ai/suggest/{question_id}` - Get question improvement suggestions

## 🧪 Testing

### API Testing
```bash
# Run the comprehensive test suite
cd backend
python ../test_api.py
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 🔨 Development

### Backend Development
- **FastAPI** with automatic OpenAPI documentation
- **SQLAlchemy** ORM for database operations
- **Pydantic** for data validation
- **JWT** authentication with python-jose
- **bcrypt** for password hashing

### Frontend Development
- **React 19** with latest features
- **Vite** for fast development and building
- **Tailwind CSS 4** for styling
- **React Router Dom 7** for navigation
- **Axios** for API communication
- **React Quill** for rich text editing

### Code Quality
- **ESLint** for JavaScript linting
- **Black** for Python code formatting
- **Type hints** in Python code
- **Responsive design** principles

## 🚢 Deployment

### Backend Deployment
```bash
# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# With Docker
docker build -t stackit-backend .
docker run -p 8000:8000 stackit-backend
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Deploy to static hosting (Vercel, Netlify, etc.)
```

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite/PostgreSQL** - Database options
- **Pydantic** - Data validation using Python type hints
- **JWT** - JSON Web Tokens for authentication
- **Google Generative AI** - AI-powered features
- **Cloudinary** - Image upload and management

### Frontend
- **React 19** - Latest React with concurrent features
- **Vite** - Next generation frontend tooling
- **Tailwind CSS 4** - Utility-first CSS framework
- **React Router Dom 7** - Declarative routing
- **Axios** - Promise-based HTTP client
- **React Quill** - Rich text editor
- **Lucide React** - Beautiful icon library
- **React Toastify** - Toast notifications

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** team for the amazing framework
- **React** team for the powerful frontend library
- **Tailwind CSS** for the utility-first CSS framework
- **Google** for the Generative AI API
- **Open source community** for all the amazing libraries

## � Support

- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Issues**: [GitHub Issues](https://github.com/Priyanshu-2811/StackIt-Odoo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Priyanshu-2811/StackIt-Odoo/discussions)

---

⭐ **Star this repository if you find it helpful!**

Built with ❤️ by [Priyanshu](https://github.com/Priyanshu-2811)
