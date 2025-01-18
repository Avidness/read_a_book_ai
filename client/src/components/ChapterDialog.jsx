// components/ChapterDialog.jsx
import React from 'react';
import {
  DialogContent,
  DialogHeader,
  DialogTitle,
} from './Dialog';

const ChapterDialog = ({ chapter }) => (
  <DialogContent className="bg-stone-800 text-white border-stone-700">
    <DialogHeader>
      <DialogTitle className="text-xl font-bold text-white">
        Chapter {chapter.chapter_id}: {chapter.chapter_name}
      </DialogTitle>
    </DialogHeader>
    <div className="space-y-4">
      <p className="mt-2 text-white">{chapter.chapter_summary}</p>
    </div>
  </DialogContent>
);

export default ChapterDialog;