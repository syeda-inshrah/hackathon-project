"use client"

import { Phone, Mail, MapPin, Facebook, Twitter, Linkedin, Instagram } from "lucide-react"

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-slate-950 text-gray-300 pt-16 pb-8 px-6 border-t border-slate-800">
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          <div className="col-span-1">
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-gradient-to-br from-emerald-600 to-teal-600 p-2 rounded-xl">
                <Phone className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Emergency AI</span>
            </div>
            <p className="text-slate-400 mb-4">
              AI-powered emergency response system saving lives 24/7 across North America.
            </p>
            <div className="flex space-x-3">
              <button className="hover:bg-slate-800 rounded-full p-2 transition-colors" aria-label="Facebook">
                <Facebook className="w-5 h-5" />
              </button>
              <button className="hover:bg-slate-800 rounded-full p-2 transition-colors" aria-label="Twitter">
                <Twitter className="w-5 h-5" />
              </button>
              <button className="hover:bg-slate-800 rounded-full p-2 transition-colors" aria-label="LinkedIn">
                <Linkedin className="w-5 h-5" />
              </button>
              <button className="hover:bg-slate-800 rounded-full p-2 transition-colors" aria-label="Instagram">
                <Instagram className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div>
            <h3 className="text-white font-semibold text-lg mb-4">Services</h3>
            <ul className="space-y-2">
              <li>
                <a href="#services" className="hover:text-emerald-400 transition-colors">
                  Police Assistance
                </a>
              </li>
              <li>
                <a href="#services" className="hover:text-emerald-400 transition-colors">
                  Medical Emergency
                </a>
              </li>
              <li>
                <a href="#services" className="hover:text-emerald-400 transition-colors">
                  Fire & Rescue
                </a>
              </li>
              <li>
                <a href="#services" className="hover:text-emerald-400 transition-colors">
                  Road Assistance
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold text-lg mb-4">Company</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="hover:text-emerald-400 transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-emerald-400 transition-colors">
                  Careers
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-emerald-400 transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-emerald-400 transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold text-lg mb-4">Contact</h3>
            <ul className="space-y-3">
              <li className="flex items-center space-x-2">
                <Phone className="w-4 h-4 text-emerald-400" />
                <span>1-800-EMERGENCY</span>
              </li>
              <li className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-emerald-400" />
                <span>help@emergencyai.com</span>
              </li>
              <li className="flex items-start space-x-2">
                <MapPin className="w-4 h-4 text-emerald-400 mt-1" />
                <span>
                  123 Emergency Ave
                  <br />
                  San Francisco, CA 94105
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-8 text-center text-slate-500">
          <p>&copy; {currentYear} Emergency Response AI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
