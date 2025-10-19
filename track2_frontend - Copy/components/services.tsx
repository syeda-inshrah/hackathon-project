"use client"

import { Shield, Heart, Flame, Car, Clock } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { services } from "@/lib/mock-data"

const iconMap = {
  shield: Shield,
  heart: Heart,
  flame: Flame,
  car: Car,
} as const

const colorMap = {
  blue: "from-blue-500 to-blue-600",
  red: "from-red-500 to-red-600",
  orange: "from-orange-500 to-orange-600",
  purple: "from-purple-500 to-purple-600",
} as const

export default function Services() {
  return (
    <section id="services" className="py-20 px-6 bg-slate-900/30">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">Emergency Services</h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Comprehensive emergency response services powered by advanced AI coordination
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {services.map((service) => {
            const Icon = iconMap[service.icon as keyof typeof iconMap]
            return (
              <div
                key={service.id}
                className="p-8 rounded-2xl backdrop-blur-sm transition-all bg-slate-800/40 border border-slate-700/50 hover:border-slate-600 hover:shadow-xl"
              >
                <div
                  className={`w-14 h-14 mb-6 rounded-xl flex items-center justify-center bg-gradient-to-br ${
                    colorMap[service.color as keyof typeof colorMap]
                  } shadow-lg`}
                >
                  <Icon className="w-7 h-7 text-white" style={{ filter: "brightness(1.5)" }} />
                </div>
                <h3 className="text-xl font-bold mb-3 text-slate-100">{service.title}</h3>
                <Badge variant="secondary" className="mb-3 bg-slate-700/50 text-slate-300 border-slate-600">
                  <Clock className="w-3 h-3 mr-1" />
                  {service.responseTime}
                </Badge>
                <p className="text-sm leading-relaxed text-slate-400">{service.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
