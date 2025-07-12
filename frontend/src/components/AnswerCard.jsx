import { useState } from 'react';
import axios from '../api/api';
import { toast } from 'react-toastify';

export default function AnswerCard({ answer, questionOwnerId, onAnswerUpdate }) {
  const [loading, setLoading] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const [comments, setComments] = useState(answer.comments || []);
  const [newComment, setNewComment] = useState('');
  const [commentLoading, setCommentLoading] = useState(false);

  const currentUserId = localStorage.getItem('userId'); // You'd need to store this during login
  const isLoggedIn = !!localStorage.getItem('token');
  const isQuestionOwner = currentUserId && parseInt(currentUserId) === questionOwnerId;

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Recently';
    }
  };

  const handleAcceptAnswer = async () => {
    if (!isQuestionOwner) {
      toast.error('Only the question owner can accept answers');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`/answers/${answer.id}/accept`);
      onAnswerUpdate(response.data);
      toast.success('Answer accepted!');
    } catch (error) {
      console.error('Error accepting answer:', error);
      toast.error('Failed to accept answer');
    } finally {
      setLoading(false);
    }
  };

  const loadComments = async () => {
    try {
      const response = await axios.get(`/comments/answer/${answer.id}`);
      setComments(response.data);
    } catch (error) {
      console.error('Error loading comments:', error);
      toast.error('Failed to load comments');
    }
  };

  const handleToggleComments = () => {
    if (!showComments && comments.length === 0) {
      loadComments();
    }
    setShowComments(!showComments);
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    
    if (!newComment.trim()) {
      toast.error('Please enter a comment');
      return;
    }

    setCommentLoading(true);
    try {
      const response = await axios.post(`/comments/answer/${answer.id}`, {
        content: newComment.trim()
      });
      
      setComments([...comments, response.data]);
      setNewComment('');
      toast.success('Comment added!');
    } catch (error) {
      console.error('Error adding comment:', error);
      toast.error('Failed to add comment');
    } finally {
      setCommentLoading(false);
    }
  };

  return (
    <div className={`bg-white border rounded-lg p-6 ${answer.is_accepted ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}>
      {answer.is_accepted && (
        <div className="flex items-center mb-4 text-green-600">
          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <span className="font-medium">Accepted Answer</span>
        </div>
      )}

      <div 
        className="prose max-w-none mb-4" 
        dangerouslySetInnerHTML={{ __html: answer.content }} 
      />

      <div className="flex items-center justify-between border-t pt-4">
        <div className="flex items-center space-x-4">
          <button
            onClick={handleToggleComments}
            className="text-blue-600 hover:text-blue-800 text-sm"
          >
            {showComments ? 'Hide' : 'Show'} Comments ({comments.length})
          </button>
          
          {isQuestionOwner && !answer.is_accepted && (
            <button
              onClick={handleAcceptAnswer}
              disabled={loading}
              className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Accepting...' : 'Accept Answer'}
            </button>
          )}
        </div>

        <div className="text-sm text-gray-600">
          answered {formatDate(answer.created_at)}
        </div>
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="mt-4 pt-4 border-t">
          <h4 className="font-medium mb-3">Comments</h4>
          
          {comments.length > 0 ? (
            <div className="space-y-2 mb-4">
              {comments.map((comment) => (
                <div key={comment.id} className="bg-gray-50 p-3 rounded text-sm">
                  <p className="mb-1">{comment.content}</p>
                  <span className="text-gray-500 text-xs">
                    {formatDate(comment.created_at)}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm mb-4">No comments yet.</p>
          )}

          {/* Add Comment Form */}
          {isLoggedIn ? (
            <form onSubmit={handleAddComment} className="flex gap-2">
              <input
                type="text"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Add a comment..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="submit"
                disabled={commentLoading}
                className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
              >
                {commentLoading ? 'Adding...' : 'Add'}
              </button>
            </form>
          ) : (
            <p className="text-gray-500 text-sm">
              <a href="/login" className="text-blue-600 hover:underline">Log in</a> to add a comment.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
