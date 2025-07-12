import { useEffect, useState } from "react";
import axios from "../api/api";
import QuestionCard from "../components/QuestionCard";
import { toast } from 'react-toastify';

export default function Home() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get("/questions/");
        setQuestions(response.data);
      } catch (error) {
        console.error('Error fetching questions:', error);
        toast.error('Failed to load questions');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-lg">Loading questions...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Recent Questions</h1>
        <a 
          href="/ask" 
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Ask Question
        </a>
      </div>
      
      {questions.length > 0 ? (
        <div className="space-y-6">
          {questions.map((question) => (
            <QuestionCard key={question.id} question={question} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold text-gray-600 mb-4">
            No questions yet
          </h2>
          <p className="text-gray-500 mb-6">
            Be the first to ask a question and start the discussion!
          </p>
          <a 
            href="/ask" 
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors inline-block"
          >
            Ask the First Question
          </a>
        </div>
      )}
    </div>
  );
}