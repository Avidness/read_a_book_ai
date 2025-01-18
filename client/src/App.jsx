import React, { useState } from 'react';
import { Book, Users, ChevronRight, ChevronDown, MessageSquare, Send } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { useStreamFetcher } from "./hooks/useStreamFetcher";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from './components/Dialog';
import BookIcon from './components/BookIcon';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const App = () => {
  // Sidebar state
  const [isChapterOpen, setIsChapterOpen] = useState(false);
  const [isCharacterOpen, setIsCharacterOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  
  // Content state
  const [chapters, setChapters] = useState([]);
  const [characters, setCharacters] = useState([]);

  // Chat state
  const { streamData, isStreaming, fetchStream } = useStreamFetcher(apiUrl);
  const [inputValue, setInputValue] = useState('');

  // Process stream data for both chat and content objects
  React.useEffect(() => {
    streamData.forEach(chunk => {
      try {
        const data = JSON.parse(chunk);
        setChapters(data["chapters"]);
        setCharacters(data["characters"]);
      } catch (error) {
        console.error(error)
      }
    });
  }, [streamData]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!inputValue.trim() || isStreaming) return;
    
    fetchStream('send_input', { 'user_input': inputValue });
    setInputValue('');
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
    setIsDialogOpen(true);
  };

  const ChapterDialog = ({ chapter }) => (
    <DialogContent className="bg-stone-800 text-amber-50 border-stone-700">
      <DialogHeader>
        <DialogTitle className="text-xl font-bold">
          Chapter {chapter["chapter_id"]}: {chapter["chapter_name"]}
        </DialogTitle>
      </DialogHeader>
      <div className="space-y-4">
        <p className="mt-2">{chapter[["chapter_summary"]]}</p>
      </div>
    </DialogContent>
  );

  const CharacterDialog = ({ character }) => (
    <DialogContent className="bg-stone-800 text-amber-50 border-stone-700">
      <DialogHeader>
        <DialogTitle className="text-xl font-bold">{character["character_name"]}</DialogTitle>
      </DialogHeader>
      <div className="space-y-4">
        <div>
          <h4 className="font-semibold">Character Arc</h4>
          <p className="mt-2">{character["arc"]}</p>
        </div>
        <div>
          <h4 className="font-semibold">Physical Description</h4>
          <p className="mt-2">{character["physical_desc"]}</p>
        </div>
        <div>
          <h4 className="font-semibold">Psychological Profile</h4>
          <p className="mt-2">{character["psychological_desc"]}</p>
        </div>
      </div>
    </DialogContent>
  );

  return (
    <div className="flex h-screen w-full bg-stone-900">
      {/* Sidebar */}
      <div className="w-64 min-w-64 bg-stone-800 border-r border-stone-700">
        {/* Title Section */}
        <div className="flex items-center gap-2 p-4 border-b border-stone-700">
          <BookIcon className="w-9 h-9"/>
          <h1 className="text-xl font-bold text-amber-50">CorpusAI</h1>
        </div>

        {/* Collapsible Sections */}
        <div className="p-2">
          {/* Chapters Section */}
          <div className="space-y-2">
            <button
              onClick={() => setIsChapterOpen(!isChapterOpen)}
              className="flex items-center justify-between w-full p-2 text-sm font-medium text-left text-amber-50 hover:bg-stone-700 rounded-lg"
            >
              <div className="flex items-center gap-2">
                <Book className="w-4 h-4" />
                <span>Chapters</span>
              </div>
              {isChapterOpen ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </button>
            {isChapterOpen && (
              <div className="space-y-1">
                {chapters.map((chapter) => (
                  <button
                    key={chapter["chapter_id"]}
                    onClick={() => handleItemClick(chapter)}
                    className="w-full p-2 text-sm text-left text-amber-50 hover:bg-stone-700 rounded-lg pl-8"
                  >
                    Chapter {chapter["chapter_id"]}: {chapter["chapter_name"]}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Characters Section */}
          <div className="space-y-2 mt-4">
            <button
              onClick={() => setIsCharacterOpen(!isCharacterOpen)}
              className="flex items-center justify-between w-full p-2 text-sm font-medium text-left text-amber-50 hover:bg-stone-700 rounded-lg"
            >
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                <span>Characters</span>
              </div>
              {isCharacterOpen ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </button>
            {isCharacterOpen && (
              <div className="space-y-1">
                {characters.map((character) => (
                  <button
                    key={character["character_name"]}
                    onClick={() => handleItemClick(character)}
                    className="w-full p-2 text-sm text-left text-amber-50 hover:bg-stone-700 rounded-lg pl-8"
                  >
                    {character["character_name"]}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Chat Window */}
      <div className="flex-1 flex flex-col min-w-0">
        <div className="flex-1 p-4 overflow-auto">
          {streamData.length === 0 ? (
            <div className="flex items-center justify-center h-full text-amber-200/60">
              <div className="flex flex-col items-center gap-2">
                <MessageSquare className="w-12 h-12" />
                <p>Start a new conversation</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {streamData.map((chunk, index) => (
                <div key={index} className="text-amber-50 prose prose-invert max-w-none">
                  <ReactMarkdown>{chunk}</ReactMarkdown>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Chat input */}
        <div className="p-4 border-t border-stone-700 bg-stone-800">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 p-2 bg-stone-700 border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-400 text-amber-50 placeholder-amber-200/30"
              disabled={isStreaming}
            />
            <button
              type="submit"
              disabled={isStreaming || !inputValue.trim()}
              className="px-4 py-2 bg-amber-600 text-amber-50 rounded-lg hover:bg-amber-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>

      {/* Dialog for both Chapter and Character details */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        {selectedItem?.type === 'chapter' && <ChapterDialog chapter={selectedItem} />}
        {selectedItem?.type === 'character' && <CharacterDialog character={selectedItem} />}
      </Dialog>
    </div>
  );
};

export default App;