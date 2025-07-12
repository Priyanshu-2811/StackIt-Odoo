import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "../api/api";
import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css";
import { toast } from 'react-toastify';
import AnswerCard from "../components/AnswerCard";

export default function QuestionDetail() {
  const { id } = useParams();
  const [question, setQuestion] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
    
    // Fetch question details
    axios.get(`/questions/${id}`)
      .then((res) => {
        setQuestion(res.data);
        setAnswers(res.data.answers || []);
      })
      .catch((error) => {
        console.error('Error fetching question:', error);
        toast.error('Failed to load question');
      });
  }, [id]);

  const submitAnswer = async (e) => {
    e.preventDefault();
    
    if (!answer.trim()) {
      toast.error('Please enter an answer');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`/answers/question/${id}`, {
        content: answer.trim()
      });
      
      setAnswers([...answers, response.data]);
      setAnswer("");
      toast.success('Answer submitted successfully!');
    } catch (error) {
      console.error('Error submitting answer:', error);
      toast.error('Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatTags = (tags) => {
    if (!tags) return [];
    return tags.split(',').map(tag => tag.trim()).filter(tag => tag);
  };

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Recently';
    }
  };

  if (!question) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-lg">Loading question...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6">
      {/* Question Section */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <h1 className="text-3xl font-bold mb-4">{question.title}</h1>
        
        <div className="flex items-center mb-4 text-sm text-gray-600">
          <span>Asked {formatDate(question.created_at)}</span>
        </div>

        <div 
          className="prose max-w-none mb-6" 
          dangerouslySetInnerHTML={{ __html: question.description }} 
        />
        
        <div className="flex flex-wrap gap-2">
          {formatTags(question.tags).map((tag, index) => (
            <span 
              key={index}
              className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* Answers Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">
          {answers.length} {answers.length === 1 ? 'Answer' : 'Answers'}
        </h2>
        
        {answers.length > 0 ? (
          <div className="space-y-6">
            {answers.map((ans) => (
              <AnswerCard 
                key={ans.id} 
                answer={ans} 
                questionOwnerId={question.owner_id}
                onAnswerUpdate={(updatedAnswer) => {
                  setAnswers(answers.map(a => a.id === updatedAnswer.id ? updatedAnswer : a));
                }}
              />
            ))}
          </div>
        ) : (
          <p className="text-gray-600 text-center py-8">
            No answers yet. Be the first to help!
          </p>
        )}
      </div>

      {/* Answer Form */}
      {isLoggedIn ? (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">Your Answer</h3>
          
          <form onSubmit={submitAnswer}>
            <ReactQuill 
              value={answer} 
              onChange={setAnswer}
              className="mb-4"
              modules={{
                toolbar: [
                  [{ 'header': [1, 2, false] }],
                  ['bold', 'italic', 'underline', 'strike'],
                  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                  ['link', 'code'],
                  ['clean']
                ],
              }}
              placeholder="Write your answer here. Include code examples, explanations, and be as helpful as possible."
            />
            
            <button 
              type="submit" 
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Submitting...' : 'Submit Answer'}
            </button>
          </form>
        </div>
      ) : (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
          <p className="text-gray-600 mb-4">Please log in to post an answer.</p>
          <a 
            href="/login" 
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors inline-block"
          >
            Log In
          </a>
        </div>
      )}
    </div>
  );
}