// components/ChatInput.jsx
import React, { useState } from 'react';
import { Send } from 'lucide-react';

const ChatInput = ({ onSendMessage, isStreaming }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isStreaming) return;
    
    onSendMessage(inputValue);
    setInputValue('');
  };

  return (
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
  );
};

export default ChatInput;