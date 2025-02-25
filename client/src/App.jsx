// App.jsx
import React, { useState } from 'react';
import MainChat from './components/MainChat';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleNewMessage = (message) => {
    setMessages(prev => [...prev, message]);
  };

  return (
    <div className="flex h-screen w-full bg-stone-900">
      <MainChat 
        messages={messages}
        isUploading={isUploading}
        onNewMessage={handleNewMessage}
        setIsUploading={setIsUploading}
      />
    </div>
  );
};

export default App;