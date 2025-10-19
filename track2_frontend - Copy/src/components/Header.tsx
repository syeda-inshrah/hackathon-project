import React, { useState } from 'react';
import { Phone, Moon, Sun } from 'lucide-react';
import { Button } from './ui/button';

const Header = () => {
  const [isDark, setIsDark] = useState(false);
  const [activeTab, setActiveTab] = useState('home');

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle('dark');
  };

  const menuItems = ['Home', 'Services', 'Features', 'Stats', 'Testimonials'];

  const scrollToSection = (section) => {
    setActiveTab(section.toLowerCase());
    const element = document.getElementById(section.toLowerCase());
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="bg-gradient-to-br from-emerald-600 to-teal-600 p-2 rounded-xl">
              <Phone className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white">
              Emergency Response AI
            </span>
          </div>

          <nav className="hidden md:flex items-center space-x-8">
            {menuItems.map((item) => (
              <button
                key={item}
                onClick={() => scrollToSection(item)}
                className={`text-sm font-medium transition-colors hover:text-emerald-400 ${
                  activeTab === item.toLowerCase() ? 'text-emerald-400' : 'text-slate-300'
                }`}
              >
                {item}
              </button>
            ))}
          </nav>

          <div className="flex items-center space-x-4">
            <Button
              onClick={toggleTheme}
              className="px-4 py-2.5 rounded-xl backdrop-blur-xl transition-all shadow-lg bg-slate-800/90 text-emerald-400 border border-slate-700/50 hover:bg-slate-700/90 hover:border-emerald-500/30"
            >
              <div className="flex items-center gap-2 font-medium text-sm">
                {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                <span className="hidden sm:inline">{isDark ? 'Light' : 'Dark'}</span>
              </div>
            </Button>
            <Button
              className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white shadow-lg"
              onClick={() => alert('Emergency call initiated!')}
            >
              <Phone className="w-4 h-4 mr-2" />
              Emergency
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
