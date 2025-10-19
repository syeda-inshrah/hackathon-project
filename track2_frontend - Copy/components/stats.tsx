"use client"

import { stats } from "@/lib/mock-data"

export default function Stats() {
  return (
    <section id="stats" className="py-20 px-6 bg-slate-900/30">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white">Trusted Performance</h2>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat) => (
            <div key={stat.id} className="text-center">
              <div className="text-4xl sm:text-5xl font-bold mb-2 text-emerald-400">{stat.value}</div>
              <div className="text-base font-medium text-slate-400">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
