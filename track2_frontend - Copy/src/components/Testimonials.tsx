import React from 'react';
import { Star } from 'lucide-react';
import { testimonials } from '../mockData';

const Testimonials = () => {
  return (
    <section id="testimonials" className="py-20 px-6">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
            Professional Endorsements
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Trusted by emergency professionals and first responders nationwide
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((testimonial) => (
            <div 
              key={testimonial.id}
              className="p-8 rounded-2xl backdrop-blur-sm transition-all bg-slate-800/40 border border-slate-700/50 hover:border-slate-600"
            >
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold mr-4 bg-gradient-to-br from-emerald-500 to-teal-500 shadow-md">
                  {testimonial.avatar}
                </div>
                <div>
                  <h3 className="font-bold text-slate-100">{testimonial.name}</h3>
                  <p className="text-sm text-emerald-400">{testimonial.role}</p>
                </div>
              </div>

              <p className="text-sm leading-relaxed mb-6 text-slate-300">
                {testimonial.content}
              </p>

              <div className="flex gap-1">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 fill-amber-400 text-amber-400" />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
