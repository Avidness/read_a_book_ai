import React from 'react';

const BookIcon = ({ className = "w-5 h-5" }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" className={className}>
    <path 
      d="M6 4C4.9 4 4 4.9 4 6v20c0 1.1 0.9 2 2 2h20c1.1 0 2-0.9 2-2V6c0-1.1-0.9-2-2-2H6z"
      fill="#92400e" />
    <path 
      d="M7 6h18v18H7V6z"
      fill="#fef3c7" />
    <path 
      d="M8 7h2v16H8V7z"
      fill="#f59e0b" />
    <path 
      d="M12 10h10M12 14h10M12 18h10"
      stroke="#92400e"
      strokeWidth="1"
      strokeLinecap="round" />
  </svg>
);

export default BookIcon;