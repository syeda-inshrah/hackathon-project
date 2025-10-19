"use client";
import { useState } from "react";
import { auth } from "@/lib/firebase";
import { createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
import { useRouter } from "next/navigation";
import Link from "next/link";
import toast from "react-hot-toast";
import { Zap, Lightbulb, Shield, Lock, ArrowRight } from 'lucide-react'

export default function SignupPage() {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const router = useRouter();

  const handleSignup = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // ✅ Basic client-side validation
    if (!name || !email || !password) {
      toast.error("All fields are required");
      return;
    }
    if (password.length < 6) {
      toast.error("Password must be at least 6 characters long");
      return;
    }

    try {
      // Create user
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
      );

      // Add display name
      if (auth.currentUser) {
        await updateProfile(auth.currentUser, { displayName: name });
      }

      toast.success("Signup successful! Please login.");
      router.push("/"); // go back to login
    } catch (err: any) {
      if (err.code === "auth/email-already-in-use") {
        toast.error("User already exists. Please login.");
      } else {
        toast.error(err.message || "Something went wrong");
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 flex items-center justify-center p-8">
      <div className="w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
        {/* Left Side - Features */}
        <div className="space-y-8">
          {/* Logo and Branding */}
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl flex items-center justify-center">
                <div className="w-6 h-8 bg-white rounded-md"></div>
              </div>
              <h1 className="text-4xl font-bold text-white">AgenticAI</h1>
            </div>
            <p className="text-lg text-gray-400 pl-1">Intelligent Learning Ecosystem</p>
          </div>

          {/* Feature Cards Grid */}
          <div className="grid grid-cols-2 gap-4 mt-12">
            {/* Autonomous Agents */}
            <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-6 space-y-3">
              <div className="w-12 h-12 bg-gradient-to-br from-violet-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-white">Autonomous Agents</h3>
                <p className="text-sm text-gray-400 leading-relaxed">Self-learning AI agents that adapt to your learning style</p>
              </div>
            </div>

            {/* Smart Tutors */}
            <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-6 space-y-3">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
                <Lightbulb className="w-6 h-6 text-white" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-white">Smart Tutors</h3>
                <p className="text-sm text-gray-400 leading-relaxed">24/7 AI tutors providing personalized guidance</p>
              </div>
            </div>

            {/* Predictive Analytics */}
            <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-6 space-y-3">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-white">Predictive Analytics</h3>
                <p className="text-sm text-gray-400 leading-relaxed">AI-powered insights into learning patterns and progress</p>
              </div>
            </div>

            {/* Secure Platform */}
            <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-6 space-y-3">
              <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center">
                <Lock className="w-6 h-6 text-white" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-white">Secure Platform</h3>
                <p className="text-sm text-gray-400 leading-relaxed">Enterprise-grade security for your learning data</p>
              </div>
            </div>
          </div>

          {/* Status Card */}
          <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-6">
            <div className="flex items-start gap-3">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-base font-semibold text-white">AI System Status: Online</span>
              </div>
            </div>
            <div className="flex items-center gap-2 mt-2">
              <div className="flex gap-1">
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></div>
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
              </div>
            </div>
            <p className="text-sm text-gray-400 mt-3">Processing 1,247 active learning sessions</p>
          </div>
        </div>

        {/* Right Side - Signup Panel */}
        <div className="bg-slate-800/60 backdrop-blur-sm rounded-2xl p-12 space-y-8 lg:mt-0">
          {/* Header */}
          <div className="space-y-3">
            <h2 className="text-3xl font-bold text-white">Create Account</h2>
            <p className="text-sm text-gray-400">Join our intelligent learning ecosystem</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSignup} className="space-y-6">
            {/* Full Name Input */}
            <div className="space-y-2">
              <label className="text-sm text-gray-400">Full Name</label>
              <input
                type="text"
                placeholder="Enter your full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full bg-slate-900/80 text-gray-200 placeholder-gray-500 rounded-lg px-4 py-3 border border-slate-700/50 focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500 transition-all"
              />
            </div>

            {/* Email Input */}
            <div className="space-y-2">
              <label className="text-sm text-gray-400">Institutional Email</label>
              <input
                type="email"
                placeholder="your.name@institution.edu"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-900/80 text-gray-200 placeholder-gray-500 rounded-lg px-4 py-3 border border-slate-700/50 focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500 transition-all"
              />
            </div>

            {/* Password Input */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm text-gray-400">Access Key</label>
                <button type="button" className="text-xs text-violet-400 hover:text-violet-300 transition-colors">Password requirements</button>
              </div>
              <input
                type="password"
                placeholder="Create your access key"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-900/80 text-gray-200 placeholder-gray-500 rounded-lg px-4 py-3 border border-slate-700/50 focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500 transition-all"
              />
            </div>

            {/* AI Authentication Badge */}
            <div className="space-y-2">
              <label className="text-sm text-gray-400">AI Authentication</label>
              <div className="bg-slate-900/50 rounded-lg px-4 py-3 border border-slate-700/50 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-green-500 font-medium">Secure Registration</span>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button 
              type="submit"
              className="w-full bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white font-semibold rounded-xl px-6 py-4 flex items-center justify-center gap-2 transition-all shadow-lg shadow-violet-500/20 hover:shadow-violet-500/40"
            >
              <span>Create Account</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </form>

          {/* Footer Link */}
          <div className="text-center pt-4">
            <p className="text-sm text-gray-400">
              Already have an account?{' '}
              <Link href="/login" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                Login here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}