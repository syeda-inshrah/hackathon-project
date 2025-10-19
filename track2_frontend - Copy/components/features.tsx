"use client"

import { Brain, MapPin, Languages, TrendingUp, Zap, Activity } from "lucide-react"
import { features } from "@/lib/mock-data"

const iconMap = {
  brain: Brain,
  "map-pin": MapPin,
  languages: Languages,
  "trending-up": TrendingUp,
  zap: Zap,
  activity: Activity,
} as const

export default function Features() {
  return (
    <section id="features" className="py-20 px-6">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">Advanced Features</h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Cutting-edge technology ensuring fastest and most efficient emergency response
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => {
            const Icon = iconMap[feature.icon]
            return (
              <div key={feature.id} className="text-center">
                <div className="w-16 h-16 mx-auto mb-6 rounded-xl flex items-center justify-center bg-gradient-to-br from-emerald-600 to-teal-600 shadow-lg">
                  <Icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-lg font-bold mb-3 text-slate-100">{feature.title}</h3>
                <p className="text-sm leading-relaxed text-slate-400">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
