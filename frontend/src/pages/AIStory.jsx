import { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Loader2, Sparkles, BookOpen, Heart } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export default function AIStory() {
  const [prompt, setPrompt] = useState('');
  const [culture, setCulture] = useState('Indian');
  const [language, setLanguage] = useState('English');
  const [loading, setLoading] = useState(false);
  const [story, setStory] = useState(null);

  const cultures = ['Indian', 'African', 'Japanese', 'Chinese', 'Norse', 'Celtic', 'Native American', 'Arabic'];
  const languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Spanish', 'French'];

  const generateStory = async () => {
    if (!prompt.trim()) {
      alert('Please enter a story prompt!');
      return;
    }
    
    setLoading(true);
    
    // Demo mode - shows story even without backend
    setTimeout(() => {
      setStory({
        title: `The ${culture} Storyteller's Gift`,
        content: `In a small ${culture} village, there lived a young storyteller named Maya. ${prompt}. 

The villagers gathered around as Maya shared tales of bravery, kindness, and wisdom passed down through generations. 

Every word she spoke painted vivid pictures in their minds, and each story carried a lesson that touched their hearts. 

By the end, the entire village learned that stories are not just entertainment—they are the threads that weave communities together.`,
        moral: "Stories have the power to unite, teach, and preserve our cultural heritage for generations to come.",
        tags: [culture.toLowerCase(), "wisdom", "storytelling", "heritage"]
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-100 to-pink-100 px-4 py-2 rounded-full mb-4">
            <Sparkles className="w-5 h-5 text-purple-600" />
            <span className="text-purple-700 font-medium">AI-Powered Folklore Generation</span>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
            Create Your Folklore Story
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Generate authentic cultural stories with AI. Preserve and share the wisdom of generations.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Panel */}
          <Card className="shadow-xl">
            <CardHeader>
              <CardTitle className="text-2xl flex items-center gap-2">
                <BookOpen className="w-6 h-6 text-purple-600" />
                Story Parameters
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <label className="text-lg font-semibold mb-2 block">
                  Story Prompt or Theme
                </label>
                <Textarea
                  placeholder="Example: A brave young girl who saves her village from a drought using ancient wisdom passed down by her grandmother..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-[120px] resize-none"
                />
                <p className="text-sm text-gray-500 mt-2">
                  💡 Tip: Be specific about characters, setting, and moral lesson
                </p>
              </div>

              <div>
                <label className="text-lg font-semibold mb-2 block">
                  Culture / Region
                </label>
                <Select value={culture} onValueChange={setCulture}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {cultures.map(c => (
                      <SelectItem key={c} value={c}>{c}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-lg font-semibold mb-2 block">
                  Language
                </label>
                <Select value={language} onValueChange={setLanguage}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {languages.map(l => (
                      <SelectItem key={l} value={l}>{l}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Button
                onClick={generateStory}
                disabled={loading}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white text-lg py-6"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Weaving Your Story...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    Generate Folklore Story
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Output Panel */}
          <Card className="shadow-xl">
            <CardHeader>
              <CardTitle className="text-2xl flex items-center gap-2">
                <Heart className="w-6 h-6 text-purple-600" />
                Your Generated Story
              </CardTitle>
            </CardHeader>
            <CardContent>
              {story ? (
                <div className="space-y-6">
                  <div className="border-b pb-3">
                    <h2 className="text-2xl font-bold text-gray-800">{story.title}</h2>
                    <div className="flex flex-wrap gap-2 mt-2">
                      <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                        {culture}
                      </span>
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                        {language}
                      </span>
                      {story.tags?.map(tag => (
                        <span key={tag} className="px-2 py-1 bg-gray-100 rounded-full text-sm">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-lg">
                    <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
                      {story.content}
                    </p>
                  </div>

                  <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded">
                    <p className="font-semibold text-amber-800">📖 Moral of the Story</p>
                    <p className="text-amber-700">{story.moral}</p>
                  </div>

                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={() => {
                      navigator.clipboard.writeText(story.content);
                      alert('Story copied to clipboard!');
                    }}
                  >
                    Copy Story to Share
                  </Button>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-400">
                  <Sparkles className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>Enter a prompt and click generate</p>
                  <p className="text-sm mt-2">Your AI-generated folklore story will appear here</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}