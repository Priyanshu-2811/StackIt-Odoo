import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

export default function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    navigate('/');
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="text-xl font-bold">
            StackIt
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-4">
            <Link 
              to="/" 
              className="hover:bg-blue-700 px-3 py-2 rounded transition-colors"
            >
              Home
            </Link>
            
            {isLoggedIn ? (
              <>
                <Link 
                  to="/ask" 
                  className="bg-blue-500 hover:bg-blue-400 px-4 py-2 rounded font-medium transition-colors"
                >
                  Ask Question
                </Link>
                <button 
                  onClick={handleLogout}
                  className="hover:bg-blue-700 px-3 py-2 rounded transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link 
                  to="/login" 
                  className="hover:bg-blue-700 px-3 py-2 rounded transition-colors"
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="bg-green-500 hover:bg-green-400 px-4 py-2 rounded font-medium transition-colors"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
