export const services = [
  {
    id: 1,
    title: "Police Assistance",
    description: "Immediate connection to law enforcement with real-time location sharing and AI-powered threat assessment.",
    icon: "shield",
    color: "blue",
    responseTime: "2-4 min"
  },
  {
    id: 2,
    title: "Medical Emergency",
    description: "Connect with paramedics instantly. AI-guided first aid instructions while help is on the way.",
    icon: "heart",
    color: "red",
    responseTime: "3-6 min"
  },
  {
    id: 3,
    title: "Fire & Rescue",
    description: "Fast response fire department dispatch with AI building analysis for optimal entry strategies.",
    icon: "flame",
    color: "orange",
    responseTime: "4-7 min"
  },
  {
    id: 4,
    title: "Road Assistance",
    description: "24/7 roadside help with AI-powered location tracking and estimated arrival times.",
    icon: "car",
    color: "purple",
    responseTime: "15-30 min"
  }
];

export const features = [
  {
    id: 1,
    title: "AI-Powered Triage",
    description: "Smart call analysis that prioritizes emergencies and allocates resources efficiently.",
    icon: "brain"
  },
  {
    id: 2,
    title: "Real-Time Tracking",
    description: "Live location sharing and responder tracking so you always know help is coming.",
    icon: "map-pin"
  },
  {
    id: 3,
    title: "Multi-Language Support",
    description: "Instant translation in 50+ languages ensures everyone gets help in their native language.",
    icon: "languages"
  },
  {
    id: 4,
    title: "Predictive Analytics",
    description: "AI forecasts high-risk situations, enabling proactive emergency response and prevention.",
    icon: "trending-up"
  },
  {
    id: 5,
    title: "Automated Dispatch",
    description: "Intelligent routing sends the closest, most appropriate responders to your location.",
    icon: "zap"
  },
  {
    id: 6,
    title: "Medical Guidance",
    description: "AI-powered first aid instructions guide you through life-saving steps before help arrives.",
    icon: "activity"
  }
];

export const stats = [
  {
    id: 1,
    value: "2.5M+",
    label: "Lives Saved",
    description: "Emergency responses handled successfully"
  },
  {
    id: 2,
    value: "35%",
    label: "Faster Response",
    description: "Reduction in average response time"
  },
  {
    id: 3,
    value: "99.9%",
    label: "Uptime",
    description: "System availability 24/7/365"
  },
  {
    id: 4,
    value: "150+",
    label: "Cities Covered",
    description: "Across North America"
  }
];

export const testimonials = [
  {
    id: 1,
    name: "Sarah Johnson",
    role: "Emergency Dispatcher",
    location: "Los Angeles, CA",
    avatar: "SJ",
    content: "This AI system has transformed how we handle emergency calls. Response times are down 40% and we can prioritize critical cases instantly. It's saving lives every day.",
    rating: 5
  },
  {
    id: 2,
    name: "Dr. Michael Chen",
    role: "Paramedic Supervisor",
    location: "New York, NY",
    avatar: "MC",
    content: "The pre-arrival medical guidance feature is incredible. Callers receive life-saving instructions immediately while we're en route. We've seen significantly better patient outcomes.",
    rating: 5
  },
  {
    id: 3,
    name: "Captain Lisa Rodriguez",
    role: "Fire Department Chief",
    location: "Chicago, IL",
    avatar: "LR",
    content: "AI-powered building analysis gives our firefighters crucial information before they enter. The predictive modeling helps us prepare for high-risk situations. Outstanding technology.",
    rating: 5
  },
  {
    id: 4,
    name: "Officer James Williams",
    role: "Police Sergeant",
    location: "Houston, TX",
    avatar: "JW",
    content: "Real-time data sharing and crime trend analysis have made our responses more strategic and effective. The system's accuracy is impressive and has improved officer safety.",
    rating: 5
  }
];


// ===========================

export const emergencyServices = [
  { id: 'medical', name: 'Medical Emergency', icon: 'heart-pulse' },
  { id: 'police', name: 'Police Assistance', icon: 'shield' },
  { id: 'fire', name: 'Fire Department', icon: 'flame' },
  { id: 'rescue', name: 'Rescue Services', icon: 'life-buoy' }
];

interface Message {
  id: number;
  sender: 'user' | 'bot';
  message: string;
  timestamp: string;
}

export const mockConversation: Message[] = [
  {
    id: 1,
    sender: 'bot',
    message: 'Hello! I\'m your Emergency Response AI assistant. How can I help you today?',
    timestamp: '10:00 AM'
  },
  {
    id: 2,
    sender: 'user',
    message: 'I need medical assistance',
    timestamp: '10:01 AM'
  },
  {
    id: 3,
    sender: 'bot',
    message: 'I understand you need medical assistance. Can you describe the emergency? Is anyone injured?',
    timestamp: '10:01 AM'
  },
  {
    id: 4,
    sender: 'user',
    message: 'Yes, someone has fallen and is unconscious',
    timestamp: '10:02 AM'
  },
  {
    id: 5,
    sender: 'bot',
    message: 'Dispatching medical emergency services to your location immediately. Please stay on the line. Help is on the way. ETA: 5 minutes.',
    timestamp: '10:02 AM'
  }
];

export const quickActions = [
  { id: 1, text: 'Medical Emergency', category: 'medical' },
  { id: 2, text: 'Police Assistance', category: 'police' },
  { id: 3, text: 'Fire Emergency', category: 'fire' },
  { id: 4, text: 'Rescue Services', category: 'rescue' }
];
