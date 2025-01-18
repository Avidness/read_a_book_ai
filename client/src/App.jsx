import React, { useState, useEffect } from 'react';
import { useStreamFetcher } from "./hooks/useStreamFetcher";
import Sidebar from './components/Sidebar';
import MainChat from './components/MainChat';
import { Dialog } from './components/Dialog';
import ChapterDialog from './components/ChapterDialog';
import CharacterDialog from './components/CharacterDialog';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const App = () => {
  // Content state
  const [chapters, setChapters] = useState([]);
  const [characters, setCharacters] = useState([]);
  
  // Dialog state
  const [selectedItem, setSelectedItem] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  // Chat state
  const { streamData, isStreaming, fetchStream } = useStreamFetcher(apiUrl);

  // Process stream data for both chat and content objects
  useEffect(() => {
    streamData.forEach(chunk => {
      try {
        const data = JSON.parse(chunk);
        setChapters(data["chapters"]);
        setCharacters(data["characters"]);
      } catch (error) {
        console.error(error);
      }
    });
  }, [streamData]);

  const handleItemClick = (item) => {
    setSelectedItem(item);
    setIsDialogOpen(true);
  };

  return (
    <div className="flex h-screen w-full bg-stone-900">
      <Sidebar 
        chapters={chapters}
        characters={characters}
        onItemClick={handleItemClick}
      />
      
      <MainChat 
        streamData={streamData}
        isStreaming={isStreaming}
        fetchStream={fetchStream}
      />

      {/* Dialog for both Chapter and Character details */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        {selectedItem?.type === 'chapter' && (
          <ChapterDialog chapter={selectedItem} />
        )}
        {selectedItem?.type === 'character' && (
          <CharacterDialog character={selectedItem} />
        )}
      </Dialog>
    </div>
  );
};

export default App;