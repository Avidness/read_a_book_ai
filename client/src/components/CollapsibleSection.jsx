// components/CollapsibleSection.jsx
import React from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';

const CollapsibleSection = ({ 
  icon: Icon, 
  title, 
  isOpen, 
  onToggle, 
  children 
}) => {
  return (
    <div className="space-y-2">
      <button
        onClick={onToggle}
        className="flex items-center justify-between w-full p-2 text-sm font-medium text-left text-amber-50 hover:bg-stone-700 rounded-lg"
      >
        <div className="flex items-center gap-2">
          <Icon className="w-4 h-4" />
          <span>{title}</span>
        </div>
        {isOpen ? (
          <ChevronDown className="w-4 h-4" />
        ) : (
          <ChevronRight className="w-4 h-4" />
        )}
      </button>
      {isOpen && (
        <div className="space-y-1">
          {children}
        </div>
      )}
    </div>
  );
};

export default CollapsibleSection;