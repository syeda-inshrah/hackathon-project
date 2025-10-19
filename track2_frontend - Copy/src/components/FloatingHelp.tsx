import React from 'react';
import { MessageCircle } from 'lucide-react';

const FloatingHelp = () => {
  return (
    <button
      className="fixed bottom-6 right-6 p-4 rounded-xl shadow-2xl font-semibold z-40 flex items-center gap-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white"
      onClick={() => alert('Emergency help chat opened!')}
    >
      <MessageCircle className="w-5 h-5" />
      <span className="hidden sm:inline text-sm">Emergency Help</span>
    </button>
  );
};

export default FloatingHelp;
