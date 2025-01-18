// components/ChatMessages.jsx
import React from 'react';
import ReactMarkdown from 'react-markdown';

const ChatMessages = ({ messages }) => {
  return (
    <div className="space-y-4">
      {messages.map((message, index) => (
        <div 
          key={index} 
          className="text-amber-50 prose prose-invert max-w-none"
        >
          <ReactMarkdown>{message}</ReactMarkdown>
        </div>
      ))}
    </div>
  );
};

export default ChatMessages;