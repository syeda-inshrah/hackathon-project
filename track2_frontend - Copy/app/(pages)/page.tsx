"use client"
import Header from "@/components/header"
import Hero from "@/components/hero"
import Services from "@/components/services"
import Features from "@/components/features"
import Stats from "@/components/stats"
import Testimonials from "@/components/testimonials"
import Footer from "@/components/footer"
import FloatingHelp from "@/components/floating-help"
import { useEffect, useState } from "react"
import ChatBot from "@/components/chatbot"
import GetLocationClient from "@/components/location"
import UseDeviceStatus from "@/components/statusdevice"

interface DeviceStatus {
  online: boolean;
  connection?: {
    downlink: number;
    effectiveType: string;
    rtt: number;
  };
  battery?: {
    level: number;
    charging: boolean;
  };
}

interface User {
  userid: string;
  username: string;
  password: string;
  is_loggedin: boolean;
  phone_number: string;
  platform: 'website' | 'mobile' | 'desktop';
  created_at: string;
  updated_at: string;
}

const user: User = {
  userid: '12345',
  username: 'john_doe',
  password: 'password123',
  is_loggedin: true,
  phone_number: '+1234567890',
  platform: 'mobile',
  created_at: '2023-10-17T10:00:00Z',
  updated_at: '2023-10-17T12:00:00Z'
};


export default function Page() {
  const [toggleChat, setToggleChat] = useState<boolean>(false)
  const [loc, setLoc] = useState<{ lat: number; lon: number } | null>(null);
  const [status, setStatus] = useState<DeviceStatus>({
    online: navigator.onLine,
  });

  return (
    <main
      className="min-h-screen text-white"
      style={{
        backgroundImage: "linear-gradient(135deg, #020617 0%, #1e1b4b 50%, #020617 100%)",
      }}
    >
      <GetLocationClient loc={loc} setLoc={setLoc}/>
      <UseDeviceStatus setStatus={setStatus}/>
      <Header />
      <Hero setToggleChat={setToggleChat} />
      <ChatBot isOpen={toggleChat} onClose={()=>setToggleChat(false)} loc={loc} status={status} user={user}/>
      <Services />
      <Features />
      <Stats />
      <Testimonials />
      <Footer />
      <FloatingHelp setToggleChat={setToggleChat} />
    </main>
  )
}
