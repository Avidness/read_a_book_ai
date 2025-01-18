// components/CharacterDialog.jsx
import React from 'react';
import {
  DialogContent,
  DialogHeader,
  DialogTitle,
} from './Dialog';

const CharacterSection = ({ title, content }) => (
  <div>
    <h4 className="font-semibold">{title}</h4>
    <p className="mt-2">{content}</p>
  </div>
);

const CharacterDialog = ({ character }) => (
  <DialogContent className="bg-stone-800 text-amber-50 border-stone-700">
    <DialogHeader>
      <DialogTitle className="text-xl font-bold">
        {character.character_name}
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