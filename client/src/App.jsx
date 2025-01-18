import React, { useState } from 'react';
import { Book, Users, ChevronRight, ChevronDown, MessageSquare } from 'lucide-react';

const App = () => {
  const [isChapterOpen, setIsChapterOpen] = useState(false);
  const [isCharacterOpen, setIsCharacterOpen] = useState(false);
  const [selectedChapter, setSelectedChapter] = useState(null);
  const [selectedCharacter, setSelectedCharacter] = useState(null);

  // Sample data
  const chapters = [
    { id: 1, title: "Chapter 1: The Beginning", content: "Lorem ipsum..." },
    { id: 2, title: "Chapter 2: The Journey", content: "Dolor sit amet..." },
    { id: 3, title: "Chapter 3: The Climax", content: "Consectetur adipiscing..." }
  ];

  const characters = [
    { id: 1, name: "Alice", description: "The protagonist" },
    { id: 2, name: "Bob", description: "The antagonist" },
    { id: 3, name: "Charlie", description: "The mentor" }
  ];

  // Modal component
  const Modal = ({ isOpen, onClose, children, size = "md" }) => {
    if (!isOpen) return null;

    const sizeClasses = {
      sm: "max-w-lg",
      md: "max-w-2xl",
    };

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className={`bg-stone-800 rounded-lg ${sizeClasses[size]} w-full`}>
          <div className="p-6 text-amber-50">
            {children}
            <button
              onClick={onClose}
              className="mt-4 px-4 py-2 bg-stone-700 rounded-lg hover:bg-stone-600 text-amber-50"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex h-screen w-full bg-stone-900">
      {/* Sidebar */}
      <div className="w-64 min-w-64 bg-stone-800 border-r border-stone-700">
        {/* Title Section */}
        <div className="flex items-center gap-2 p-4 border-b border-stone-700">
          <Book className="w-6 h-6 text-amber-400" />
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
                    key={chapter.id}
                    onClick={() => setSelectedChapter(chapter)}
                    className="w-full p-2 text-sm text-left text-amber-50 hover:bg-stone-700 rounded-lg pl-8"
                  >
                    {chapter.title}
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
                    key={character.id}
                    onClick={() => setSelectedCharacter(character)}
                    className="w-full p-2 text-sm text-left text-amber-50 hover:bg-stone-700 rounded-lg pl-8"
                  >
                    {character.name}
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
          {/* Chat messages would go here */}
          <div className="flex items-center justify-center h-full text-amber-200/60">
            <div className="flex flex-col items-center gap-2">
              <MessageSquare className="w-12 h-12" />
              <p>Start a new conversation</p>
            </div>
          </div>
        </div>
        {/* Chat input */}
        <div className="p-4 border-t border-stone-700 bg-stone-800">
          <input
            type="text"
            placeholder="Type your message..."
            className="w-full p-2 bg-stone-700 border-none rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-400 text-amber-50 placeholder-amber-200/30"
          />
        </div>
      </div>

      {/* Chapter Modal */}
      <Modal
        isOpen={!!selectedChapter}
        onClose={() => setSelectedChapter(null)}
        size="md"
      >
        <h2 className="text-xl font-bold mb-4">{selectedChapter?.title}</h2>
        <p>{selectedChapter?.content}</p>
      </Modal>

      {/* Character Modal */}
      <Modal
        isOpen={!!selectedCharacter}
        onClose={() => setSelectedCharacter(null)}
        size="sm"
      >
        <h2 className="text-xl font-bold mb-4">{selectedCharacter?.name}</h2>
        <p>{selectedCharacter?.description}</p>
      </Modal>
    </div>
  );
};

export default App;