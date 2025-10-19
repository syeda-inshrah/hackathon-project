import React from 'react';
import './App.css';
import Header from './components/Header';
import Hero from './components/Hero';
import Services from './components/Services';
import Features from './components/Features';
import Stats from './components/Stats';
import Testimonials from './components/Testimonials';
import Footer from './components/Footer';
import FloatingHelp from './components/FloatingHelp';

function App() {
  return (
    <div className="App">
      <Header />
      <Hero />
      <Services />
      <Features />
      <Stats />
      <Testimonials />
      <Footer />
      <FloatingHelp />
    </div>
  );
}

export default App;
