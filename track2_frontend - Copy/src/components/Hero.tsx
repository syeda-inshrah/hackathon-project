import React from 'react';
import { Phone, BarChart3, Clock, Shield, Truck, Heart, Zap } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

const services = [
  { id: 1, title: 'Police', icon: 'Shield', color: 'blue' },
  { id: 2, title: 'Fire Dept', icon: 'Zap', color: 'red' },
  { id: 3, title: 'Medical', icon: 'Heart', color: 'green' },
  { id: 4, title: 'Rescue', icon: 'Truck', color: 'orange' }
];

const iconMap = {
  Shield,
  Zap,
  Heart,
  Truck
};

const colorMap = {
  blue: 'from-blue-500 to-blue-600',
  red: 'from-red-500 to-red-600',
  green: 'from-green-500 to-green-600',
  orange: 'from-orange-500 to-orange-600'
};

const Hero = () => {
  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center px-6 overflow-hidden py-24">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-3xl bg-emerald-500/20"></div>
        <div className="absolute bottom-1/3 right-1/4 w-[450px] h-[450px] rounded-full blur-3xl bg-purple-500/20"></div>
      </div>

      <div className="relative max-w-6xl mx-auto text-center z-10">
        <div className="mb-8">
          <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full backdrop-blur-sm bg-emerald-500/10 border border-emerald-500/20 text-emerald-300">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            <Clock className="w-4 h-4" />
            <span className="text-sm font-semibold">24/7 Emergency Services Available</span>
          </div>
        </div>

        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
          <span className="text-white">AI-Powered</span>
          <br />
          <span className="bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 bg-clip-text text-transparent">
            Emergency Response
          </span>
        </h1>

        <p className="text-lg sm:text-xl lg:text-2xl mb-10 max-w-3xl mx-auto leading-relaxed text-slate-300">
          Advanced emergency dispatch system connecting you with life-saving services in seconds.
          <span className="block mt-2 font-semibold text-emerald-400">Your safety is our priority.</span>
        </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <Button
              size="lg"
              className="px-8 py-4 rounded-xl text-lg font-bold shadow-lg transition-all bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white flex items-center gap-3"
              onClick={() => alert('Emergency help requested!')}
            >
              <Phone className="w-5 h-5" />
              Get Emergency Help
            </Button>
            <Button
              size="lg"
              className="px-8 py-4 rounded-xl text-lg font-semibold backdrop-blur-sm transition-all flex items-center gap-3 bg-slate-800/50 hover:bg-slate-800/70 text-slate-100 border border-slate-700"
              onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
            >
              <BarChart3 className="w-5 h-5" />
              Learn More
            </Button>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 max-w-4xl mx-auto">
            {services.map((service) => {
              const Icon = iconMap[service.icon];
              return (
                <button
                  key={service.id}
                  className="p-6 rounded-xl backdrop-blur-sm transition-all bg-slate-800/40 hover:bg-slate-800/60 border border-slate-700/50 hover:border-slate-600"
                >
                  <div className={`w-12 h-12 mx-auto mb-3 rounded-xl flex items-center justify-center bg-gradient-to-br ${colorMap[service.color]} shadow-md`}>
                    <Icon className="w-6 h-6 text-white" style={{ filter: 'brightness(1.5)' }} />
                  </div>
                  <div className="font-semibold text-sm text-slate-200">{service.title}</div>
                </button>
              );
            })}
          </div>
        </div>
    </section>
  );
};

export default Hero;
