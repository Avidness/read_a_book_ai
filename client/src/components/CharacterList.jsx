// components/CharacterList.jsx
import React from 'react';
import { Users } from 'lucide-react';
import CollapsibleSection from './CollapsibleSection';

const CharacterList = ({ characters, isOpen, onToggle, onCharacterClick }) => {
    return (
      <CollapsibleSection
        icon={Users}
        title="Characters"
        isOpen={isOpen}
        onToggle={onToggle}
      >
        {characters.map((character) => (
          <button
            key={character.name}
            onClick={() => onCharacterClick(character)}
            className="w-full p-2 text-sm text-left text-amber-50 hover:bg-stone-700 rounded-lg pl-8"
          >
            {character.name}
          </button>
        ))}
      </CollapsibleSection>
    );
  };
  
  export default CharacterList;