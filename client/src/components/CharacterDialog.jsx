// components/CharacterDialog.jsx
import React from 'react';
import {
  DialogContent,
  DialogHeader,
  DialogTitle,
} from './Dialog';

const CharacterSection = ({ title, content }) => (
  <div>
    <h4 className="font-semibold text-white">{title}</h4>
    <p className="mt-2 text-white">{content}</p>
  </div>
);

const CharacterDialog = ({ character }) => (
  <DialogContent className="bg-stone-800 text-white border-stone-700">
    <DialogHeader>
      <DialogTitle className="text-xl font-bold text-white">
        {character.name}
      </DialogTitle>
    </DialogHeader>
    <div className="space-y-4">
      <CharacterSection 
        title="Character Arc" 
        content={character.arc} 
      />
      <CharacterSection 
        title="Physical Description" 
        content={character.physical_desc} 
      />
      <CharacterSection 
        title="Psychological Profile" 
        content={character.psychological_desc} 
      />
    </div>
  </DialogContent>
);

export default CharacterDialog;