// components/Sidebar.jsx
import React, { useState } from 'react';
import BookIcon from './BookIcon';
import ChapterList from './ChapterList';
import CharacterList from './CharacterList';

const Sidebar = ({ chapters, characters, onItemClick }) => {
  const [isChapterOpen, setIsChapterOpen] = useState(false);
  const [isCharacterOpen, setIsCharacterOpen] = useState(false);

  const handleChapterClick = (chapter) => {
    onItemClick({ ...chapter, type: 'chapter' });
  };

  const handleCharacterClick = (character) => {
    onItemClick({ ...character, type: 'character' });
  };

  return (
    <div className="w-64 min-w-64 bg-stone-800 border-r border-stone-700 flex flex-col h-full">
      {/* Title Section */}
      <div className="flex items-center gap-2 p-4 border-b border-stone-700 shrink-0">
        <BookIcon className="w-9 h-9" />
        <h1 className="text-xl font-bold text-amber-50">CorpusAI</h1>
      </div>

      {/* Collapsible Sections */}
      <div className="p-2 overflow-y-auto flex-1">
        <ChapterList
          chapters={chapters}
          isOpen={isChapterOpen}
          onToggle={() => setIsChapterOpen(!isChapterOpen)}
          onChapterClick={handleChapterClick}
        />
        
        <div className="mt-4">
          <CharacterList
            characters={characters}
            isOpen={isCharacterOpen}
            onToggle={() => setIsCharacterOpen(!isCharacterOpen)}
            onCharacterClick={handleCharacterClick}
          />
        </div>
      </div>
    </div>
  );
};

export default Sidebar;