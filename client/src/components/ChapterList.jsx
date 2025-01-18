// components/ChapterList.jsx
import React from 'react';
import { Book } from 'lucide-react';
import CollapsibleSection from './CollapsibleSection';

const ChapterList = ({ chapters, isOpen, onToggle, onChapterClick }) => {
  return (
    <CollapsibleSection
      icon={Book}
      title="Chapters"
      isOpen={isOpen}
      onToggle={onToggle}
    >
      {chapters.map((chapter) => (
        <button
          key={chapter.chapter_id}
          onClick={() => onChapterClick(chapter)}
          className="w-full p-2 text-sm text-left text-amber-50 hover:bg-stone-700 rounded-lg pl-8"
        >
          Chapter {chapter.chapter_id}: {chapter.chapter_name}
        </button>
      ))}
    </CollapsibleSection>
  );
};

export default ChapterList;