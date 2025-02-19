// frontend/app/components/futuristic-thinking.tsx

import type React from "react";

export const FuturisticThinking: React.FC = () => {
  return (
    <div className="flex items-center justify-center w-full h-16">
      <svg className="w-24 h-16" viewBox="0 0 120 30" xmlns="http://www.w3.org/2000/svg">
        <circle className="animate-pulse-fast" cx="15" cy="15" r="15" fill="currentColor" />
        <circle className="animate-pulse-medium" cx="60" cy="15" r="15" fill="currentColor" />
        <circle className="animate-pulse-slow" cx="105" cy="15" r="15" fill="currentColor" />
        <line className="animate-expand-fast" x1="30" y1="15" x2="45" y2="15" stroke="currentColor" strokeWidth="2" />
        <line className="animate-expand-slow" x1="75" y1="15" x2="90" y2="15" stroke="currentColor" strokeWidth="2" />
      </svg>
    </div>
  );
};
