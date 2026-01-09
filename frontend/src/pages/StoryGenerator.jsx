import { useState } from 'react';
import axios from 'axios';

const StoryGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  //updated link
const API_URL = 'https://folkloregpt-production.up.railway.app/api/generate';

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt first');
      return;
    }

    setLoading(true);
    setError('');
    setStory('');
    
    try {
      const response = await axios.post(API_URL, {
        prompt: prompt,
        max_length: 150
      });
      
      // Extract the story from response
      setStory(response.data.generated_story || response.data.story);
    } catch (err) {
      console.error('API Error:', err);
      setError('Could not generate story. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-amber-50 to-orange-100">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-bold text-amber-900 mb-3">
            ✨ FolkloreGPT Storyteller
          </h1>
          <p className="text-lg text-amber-700">
            Generate unique folklore stories powered by AI
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left Column: Input */}
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-2xl font-semibold text-amber-800 mb-4">
              Your Story Prompt
            </h2>
            
            <div className="mb-6">
              <label className="block text-amber-700 font-medium mb-3">
                What kind of story would you like?
              </label>
              <textarea
                className="w-full h-40 p-4 border-2 border-amber-300 rounded-xl focus:border-amber-500 focus:ring-2 focus:ring-amber-200 resize-none"
                placeholder="Example: A story about a clever fox who outwits a tiger in the Himalayan mountains..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
              <p className="text-sm text-gray-500 mt-2">
                Be specific! Mention characters, places, or themes.
              </p>
            </div>

            <button
              onClick={handleGenerate}
              disabled={loading}
              className={`w-full py-3 px-6 rounded-xl font-bold text-lg transition-all duration-300 ${
                loading 
                  ? 'bg-amber-400 cursor-not-allowed' 
                  : 'bg-amber-600 hover:bg-amber-700 hover:shadow-lg'
              } text-white`}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-3 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Weaving your tale...
                </span>
              ) : '✨ Generate Story'}
            </button>

            {/* Error Message */}
            {error && (
              <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded">
                <p className="text-red-700 font-medium">{error}</p>
              </div>
            )}
          </div>

          {/* Right Column: Output */}
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-2xl font-semibold text-amber-800 mb-4">
              Your Generated Story
            </h2>
            
            {story ? (
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 min-h-[300px]">
                <div className="prose prose-lg max-w-none">
                  <p className="text-gray-800 leading-relaxed whitespace-pre-line">
                    {story}
                  </p>
                </div>
                
                <div className="mt-6 pt-6 border-t border-amber-200">
                  <button
                    onClick={() => navigator.clipboard.writeText(story)}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-amber-100 hover:bg-amber-200 text-amber-800 rounded-lg transition"
                  >
                    📋 Copy Story
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center min-h-[300px] bg-amber-50 rounded-xl border-2 border-dashed border-amber-300">
                <div className="text-amber-400 mb-4">
                  <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                  </svg>
                </div>
                <p className="text-amber-700 text-center px-6">
                  {loading 
                    ? "The AI is weaving your story... Patience, great tales take a moment!" 
                    : "Your story will appear here. Enter a prompt and click Generate!"}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-10 bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 className="font-semibold text-blue-800 mb-2">💡 How it works:</h3>
          <ul className="text-blue-700 list-disc pl-5 space-y-1">
            <li>Type a story prompt above (in any language)</li>
            <li>Our AI model generates a unique folklore story</li>
            <li>Stories are inspired by indigenous narrative traditions</li>
            <li>You can copy, share, or save your generated stories</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default StoryGenerator;
