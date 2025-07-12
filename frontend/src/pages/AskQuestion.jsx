import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css";
import { useState } from "react";
import axios from "../api/api";
import { useNavigate } from "react-router-dom";
import { toast } from 'react-toastify';

export default function AskQuestion() {
  const [title, setTitle] = useState("");
  const [tags, setTags] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      toast.error('Please enter a title');
      return;
    }
    
    if (!description.trim()) {
      toast.error('Please enter a description');
      return;
    }

    setLoading(true);
    try {
      await axios.post("/questions/", {
        title: title.trim(),
        tags: tags.trim(),
        description: description.trim()
      });
      toast.success('Question posted successfully!');
      navigate("/");
    } catch (error) {
      toast.error('Failed to post question. Please try again.');
      console.error('Error posting question:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6">
      <h1 className="text-3xl font-bold mb-8">Ask a Question</h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Title
          </label>
          <input 
            type="text"
            placeholder="What's your programming question? Be specific." 
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tags
          </label>
          <input 
            type="text"
            placeholder="e.g. javascript, python, react (comma-separated)" 
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <ReactQuill 
            value={description} 
            onChange={setDescription}
            className="bg-white"
            modules={{
              toolbar: [
                [{ 'header': [1, 2, false] }],
                ['bold', 'italic', 'underline', 'strike'],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                ['link', 'code'],
                ['clean']
              ],
            }}
            placeholder="Describe your problem in detail. Include any error messages, code snippets, or what you've tried so far."
          />
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Posting...' : 'Post Question'}
        </button>
      </form>
    </div>
  );
}
