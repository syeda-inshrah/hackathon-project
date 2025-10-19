export type Service = {
  id: number
  title: string
  description: string
  icon: "shield" | "heart" | "flame" | "car"
  color: "blue" | "red" | "orange" | "purple"
  responseTime: string
}

export type Feature = {
  id: number
  title: string
  description: string
  icon: "brain" | "map-pin" | "languages" | "trending-up" | "zap" | "activity"
}

export type Stat = { id: number; value: string; label: string; description: string }
export type Testimonial = {
  id: number
  name: string
  role: string
  location: string
  avatar: string
  content: string
  rating: number
}

export const services: Service[] = [
  {
    id: 1,
    title: "Police Assistance",
    description:
      "Immediate connection to law enforcement with real-time location sharing and AI-powered threat assessment.",
    icon: "shield",
    color: "blue",
    responseTime: "2-4 min",
  },
  {
    id: 2,
    title: "Medical Emergency",
    description: "Connect with paramedics instantly. AI-guided first aid instructions while help is on the way.",
    icon: "heart",
    color: "red",
    responseTime: "3-6 min",
  },
  {
    id: 3,
    title: "Fire & Rescue",
    description: "Fast response fire department dispatch with AI building analysis for optimal entry strategies.",
    icon: "flame",
    color: "orange",
    responseTime: "4-7 min",
  },
  {
    id: 4,
    title: "Road Assistance",
    description: "24/7 roadside help with AI-powered location tracking and estimated arrival times.",
    icon: "car",
    color: "purple",
    responseTime: "15-30 min",
  },
]

export const features: Feature[] = [
  {
    id: 1,
    title: "AI-Powered Triage",
    description: "Smart call analysis that prioritizes emergencies and allocates resources efficiently.",
    icon: "brain",
  },
  {
    id: 2,
    title: "Real-Time Tracking",
    description: "Live location sharing and responder tracking so you always know help is coming.",
    icon: "map-pin",
  },
  {
    id: 3,
    title: "Predictive Analytics",
    description: "AI forecasts high-risk situations, enabling proactive emergency response and prevention.",
    icon: "trending-up",
  },
  {
    id: 4,
    title: "Medical Guidance",
    description: "AI-powered first aid instructions guide you through life-saving steps before help arrives.",
    icon: "activity",
  },
]

export const stats: Stat[] = [
  { id: 1, value: "2.5M+", label: "Lives Saved", description: "Emergency responses handled successfully" },
  { id: 2, value: "35%", label: "Faster Response", description: "Reduction in average response time" },
  { id: 3, value: "99.9%", label: "Uptime", description: "System availability 24/7/365" },
  { id: 4, value: "150+", label: "Cities Covered", description: "Across North America" },
]

export const testimonials: Testimonial[] = [
  {
    id: 1,
    name: "Sarah Johnson",
    role: "Emergency Dispatcher",
    location: "Los Angeles, CA",
    avatar: "SJ",
    content:
      "This AI system has transformed how we handle emergency calls. Response times are down 40% and we can prioritize critical cases instantly. It's saving lives every day.",
    rating: 5,
  },
  {
    id: 2,
    name: "Dr. Michael Chen",
    role: "Paramedic Supervisor",
    location: "New York, NY",
    avatar: "MC",
    content:
      "The pre-arrival medical guidance feature is incredible. Callers receive life-saving instructions immediately while we're en route. We've seen significantly better patient outcomes.",
    rating: 5,
  },
  {
    id: 3,
    name: "Captain Lisa Rodriguez",
    role: "Fire Department Chief",
    location: "Chicago, IL",
    avatar: "LR",
    content:
      "AI-powered building analysis gives our firefighters crucial information before they enter. The predictive modeling helps us prepare for high-risk situations. Outstanding technology.",
    rating: 5,
  }
]
