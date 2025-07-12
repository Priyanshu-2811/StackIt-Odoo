# StackIt Frontend

A modern React frontend for the StackIt Q&A platform, built with Vite, Tailwind CSS, and React Router.

## 🚀 Features

### ✅ Completed Features

- **User Authentication**

  - User registration and login
  - JWT token management
  - Protected routes
  - Automatic logout on token expiry

- **Question Management**

  - Browse all questions
  - Ask new questions with rich text editor
  - View question details
  - Tag-based categorization

- **Answer System**

  - Post answers to questions
  - Rich text editor for formatting
  - Answer acceptance system
  - Owner-based permissions

- **Comment System**

  - Add comments to answers
  - View all comments
  - Real-time updates

- **User Interface**
  - Responsive design with Tailwind CSS
  - Clean, modern interface
  - Toast notifications for feedback
  - Loading states and error handling

## 🛠️ Tech Stack

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **React Router Dom 7** - Client-side routing
- **Tailwind CSS 4** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Quill** - Rich text editor
- **React Toastify** - Toast notifications
- **Date-fns** - Date formatting

## 📁 Project Structure

```
src/
├── api/
│   └── api.js              # Axios configuration and interceptors
├── components/
│   ├── AnswerCard.jsx      # Individual answer display
│   ├── Navbar.jsx          # Navigation component
│   ├── Notification.jsx    # Notification component
│   └── QuestionCard.jsx    # Individual question display
├── pages/
│   ├── AskQuestion.jsx     # Question creation form
│   ├── Home.jsx            # Homepage with question list
│   ├── Login.jsx           # Login form
│   ├── QuestionDetail.jsx  # Question detail with answers
│   └── Register.jsx        # Registration form
├── App.jsx                 # Main app component
├── main.jsx                # React entry point
└── index.css               # Global styles
```

## 🏃‍♂️ Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start development server**

   ```bash
   npm run dev
   ```

4. **Open browser**
   - Visit `http://localhost:5173`
   - Make sure the backend is running on `http://127.0.0.1:8000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔗 API Integration

The frontend communicates with the StackIt backend API:

- **Base URL**: `http://127.0.0.1:8000`
- **Authentication**: JWT Bearer tokens
- **Error Handling**: Automatic token refresh and error notifications

### Key API Endpoints Used

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /questions/` - Get all questions
- `POST /questions/` - Create question
- `GET /questions/{id}` - Get question details
- `POST /answers/question/{id}` - Create answer
- `POST /comments/answer/{id}` - Create comment
- `POST /answers/{id}/accept` - Accept answer

## 🎨 UI Components

### QuestionCard

- Displays question title, description, tags
- Shows creation date
- Links to question details

### AnswerCard

- Rich text answer display
- Accept answer functionality
- Comment system
- User permissions

### Navbar

- Authentication state management
- Navigation links
- Responsive design

## 🔐 Authentication Flow

1. User registers/logs in
2. JWT token stored in localStorage
3. Token included in all API requests
4. Automatic redirect on authentication failure
5. Logout clears token and redirects

## 📱 Responsive Design

- Mobile-first approach
- Tailwind CSS breakpoints
- Optimized for all screen sizes
- Touch-friendly interface

## 🚧 Future Enhancements

### Planned Features

- User profiles and avatars
- Question voting system
- Search and filtering
- Real-time notifications
- Draft saving
- Image upload support
- Dark mode
- Question categories
- User reputation system

### Technical Improvements

- State management with Redux/Zustand
- React Query for better data fetching
- Progressive Web App (PWA)
- Code splitting and lazy loading
- Error boundaries
- Unit and integration tests

## 🔧 Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://127.0.0.1:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is part of the StackIt platform and follows the same licensing terms.

## 🐛 Known Issues

- Rich text editor may need styling adjustments
- Date formatting could be improved
- Need to handle offline scenarios
- File upload not yet implemented

## 📞 Support

For questions or issues, please refer to the main StackIt repository or create an issue in the project repository.

---

Built with ❤️ using React and modern web technologies.
