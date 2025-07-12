# 🚀 StackIt – AI-Powered Q\&A Platform

A modern Stack Overflow alternative built with **FastAPI**, **React 19**, and **Gemini AI** for smarter collaboration.

![StackIt Logo](https://via.placeholder.com/800x200/3B82F6/ffffff?text=StackIt+-+Q%26A+Platform)

---

## ✨ Key Features

### 🔐 Authentication

* JWT-based login with email verification
* Role-based access: Guest, User, Admin
* Secure sessions with token refresh

### 💬 Q\&A Engine

* Ask & answer with rich text support (React Quill)
* Upvote/downvote, accept answers, tag with auto-suggestions
* Nested comments, edit/delete support

### 🤖 AI Assistance (Gemini)

* Instant AI-generated answers
* Content enrichment & formatting help
* Smart suggestions to improve questions


### 🔔 Notifications

* Notification center + optional email alerts
* Real-time updates: mentions, replies, comments

### 🎨 UI/UX

* Responsive Tailwind CSS 4 design
* Dark/light mode
* Smooth transitions & WCAG-compliant components

---

## 💠 Tech Stack

| Backend                                                | Frontend                                                  |
| ------------------------------------------------------ | --------------------------------------------------------- |
| FastAPI, SQLAlchemy, JWT, Gemini AI, SQLite/PostgreSQL | React 19, Vite, Tailwind CSS 4, Axios, React Router Dom 7 |

---

## 🏗 Project Structure

```
backend/                  # FastAPI App
├── main.py               # Entry point
├── database.py           # DB config
├── models.py             # ORM models
├── routes/               # Auth, Q&A, AI, etc.
└── .env                  # Environment config

frontend/                 # React 19 + Vite
├── components/           # UI components (Navbar, Editor, etc.)
├── pages/                # Home, Ask, Login, Register, etc.
├── context/              # Auth context
└── main.jsx              # App entry
```

---

## ⚙️ Setup Guide

### ✅ Prerequisites

* Python 3.8+, Node.js 18+, npm/yarn
* Gemini API key (for AI features)

### 🔧 Backend

```bash
git clone https://github.com/Priyanshu-2811/StackIt-Odoo.git
cd StackIt-Odoo/backend

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # Edit credentials
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --reload
```

### 🔧 Frontend

```bash
cd ../frontend
npm install
npm run dev
```

### 🔗 Access

* Frontend: `http://localhost:5173`
* Backend: `http://localhost:8000`
* Docs: `http://localhost:8000/docs`

---

## 🔍 API Highlights

### Auth

* `POST /auth/register`
* `POST /auth/login`
* `GET /auth/me`

### Questions & Answers

* `GET /questions/`
* `POST /answers/`
* `POST /votes/`
* `POST /ai/answer/{question_id}`

See full docs at `/docs`.

---

## 🚢 Deployment

### Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Docker (optional)
docker build -t stackit-backend .
docker run -p 8000:8000 stackit-backend
```

### Frontend

```bash
npm run build
npm run preview
# Deploy to Vercel, Netlify, etc.
```

---

## 🧰 Testing

```bash
# Backend
cd backend
python ../test_api.py

# Frontend
cd frontend
npm run test
```

---

## 🤝 Contributing

```bash
# Fork & clone
git checkout -b feature/your-feature
# After changes
git commit -m "Add: new feature"
git push origin feature/your-feature
# Submit PR 🎉
```

---

## 🙏 Acknowledgments

Thanks to FastAPI, React, Tailwind, Google AI, and the open-source community. 💙
