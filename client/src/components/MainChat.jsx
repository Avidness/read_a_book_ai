// components/MainChat.jsx
import React from 'react';
import EmptyState from './EmptyState';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import FileUpload from './FileUpload';

const MainChat = ({ streamData, isStreaming, fetchStream }) => {
  const handleSendMessage = (message) => {
    fetchStream('send_input', { 'user_input': message });
  };

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <div className="flex-1 p-4 overflow-auto">
        {streamData.length === 0 ? (
          <EmptyState />
        ) : (
          <ChatMessages messages={streamData} />
        )}
      </div>

      <FileUpload />
      
      <ChatInput 
        onSendMessage={handleSendMessage}
        isStreaming={isStreaming}
      />
    </div>
  );
};

export default MainChat;