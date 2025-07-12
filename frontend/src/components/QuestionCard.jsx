import { Link } from 'react-router-dom';

export default function QuestionCard({ question }) {
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) return '1 day ago';
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
      if (diffDays < 365) return `${Math.ceil(diffDays / 30)} months ago`;
      return `${Math.ceil(diffDays / 365)} years ago`;
    } catch {
      return 'recently';
    }
  };

  const formatTags = (tags) => {
    if (!tags) return [];
    return tags.split(',').map(tag => tag.trim()).filter(tag => tag);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
      <Link to={`/questions/${question.id}`} className="block">
        <h2 className="text-xl font-semibold text-gray-900 hover:text-blue-600 mb-2">
          {question.title}
        </h2>
        <p className="text-gray-600 mb-4 line-clamp-3">
          {question.description}
        </p>
      </Link>
      
      <div className="flex items-center justify-between">
        <div className="flex flex-wrap gap-2">
          {formatTags(question.tags).map((tag, index) => (
            <span 
              key={index}
              className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
        
        <div className="text-sm text-gray-500">
          asked {formatDate(question.created_at)}
        </div>
      </div>
    </div>
  );
}
