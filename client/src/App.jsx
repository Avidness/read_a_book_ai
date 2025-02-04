import React, { useEffect } from 'react';
import { useStreamFetcher } from "./hooks/useStreamFetcher";
import MainChat from './components/MainChat';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const App = () => {
  const { streamData, isStreaming, fetchStream } = useStreamFetcher(apiUrl);

  useEffect(() => {
    streamData.forEach(chunk => {
      try {
        const data = JSON.parse(chunk);
        console.log(data);
        // TODO: parse results
      } catch (error) {
        console.error(error);
      }
    });
  }, [streamData]);

  return (
    <div className="flex h-screen w-full bg-stone-900">
      <MainChat 
        streamData={streamData}
        isStreaming={isStreaming}
        fetchStream={fetchStream}
      />
    </div>
  );
};

export default App;