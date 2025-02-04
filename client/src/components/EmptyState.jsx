// components/EmptyState.jsx
import React from 'react';
import { MessageSquare } from 'lucide-react';

const EmptyState = () => {
  return (
    <div className="flex items-center justify-center h-full text-amber-200/60">
      <div className="flex flex-col items-center gap-2">
        <MessageSquare className="w-12 h-12" />
        <p>Upload a file to begin.</p>
      </div>
    </div>
  );
};

export default EmptyState;