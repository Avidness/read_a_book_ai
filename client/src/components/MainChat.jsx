// components/MainChat.jsx
import React from 'react';
import EmptyState from './EmptyState';
import ChatMessages from './ChatMessages';
import FileUpload from './FileUpload';

const MainChat = ({ messages, isUploading, onNewMessage, setIsUploading }) => {
  return (
    <div className="flex-1 flex flex-col min-w-0">
      <div className="flex-1 p-4 overflow-auto">
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          <ChatMessages messages={messages} />
        )}
      </div>

      <FileUpload 
        onNewMessage={onNewMessage}
        isUploading={isUploading}
        setIsUploading={setIsUploading}
      />
    </div>
  );
};

export default MainChat;