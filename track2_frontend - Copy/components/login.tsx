"use client";
import { useState } from "react";
import { Zap, Lightbulb, Shield, Lock, ArrowRight, Loader2 } from 'lucide-react'
import { auth } from "@/lib/firebase";
import { signInWithEmailAndPassword, fetchSignInMethodsForEmail } from "firebase/auth";
import React from 'react'
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function LoginForm(): React.ReactElement {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const router = useRouter()

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!email || !password) {
            toast.error("All fields are required");
            return;
        }

        setIsLoading(true);

        try {
            // Replace this with your actual Firebase auth logic:
            await signInWithEmailAndPassword(auth, email, password);
            alert("Login successful!")
            toast.success("Login successful!");
            router.push("/");
        } catch (err: any) {
            if (err.code === "auth/invalid-credential") {
                // Check if email exists
                const methods = await fetchSignInMethodsForEmail(auth, email);
                if (methods.length === 0) {
                    toast.error("No account found. Please sign up first.");
                    alert("No account found. Please sign up first.");
                } else {
                    toast.error("Incorrect password. Try again.");
                    alert("Incorrect password. Try again.");
                }
                toast.error("Invalid credentials");
                alert("Invalid credentials");
            } else {
                toast.error(err.message || "Something went wrong");
                alert(err.message || "Something went wrong");
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 flex items-center justify-center p-4 sm:p-6 lg:p-8">
            <div className="w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 lg:gap-12 items-start">

                {/* Left Side - Features */}
                <div className="space-y-6 sm:space-y-8 order-2 lg:order-1">

                    {/* Logo and Branding */}
                    <div className="space-y-2">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl flex items-center justify-center flex-shrink-0">
                                <div className="w-5 h-6 sm:w-6 sm:h-8 bg-white rounded-md"></div>
                            </div>
                            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white">AgenticAI</h1>
                        </div>
                        <p className="text-base sm:text-lg text-gray-400 pl-1">Intelligent Learning Ecosystem</p>
                    </div>

                    {/* Feature Cards Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mt-8 sm:mt-12">

                        {/* Autonomous Agents */}
                        <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-4 sm:p-6 space-y-3">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-violet-500 to-purple-600 rounded-lg flex items-center justify-center">
                                <Zap className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                            </div>
                            <div className="space-y-2">
                                <h3 className="text-base sm:text-lg font-semibold text-white">Autonomous Agents</h3>
                                <p className="text-xs sm:text-sm text-gray-400 leading-relaxed">Self-learning AI agents that adapt to your learning style</p>
                            </div>
                        </div>

                        {/* Smart Tutors */}
                        <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-4 sm:p-6 space-y-3">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
                                <Lightbulb className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                            </div>
                            <div className="space-y-2">
                                <h3 className="text-base sm:text-lg font-semibold text-white">Smart Tutors</h3>
                                <p className="text-xs sm:text-sm text-gray-400 leading-relaxed">24/7 AI tutors providing personalized guidance</p>
                            </div>
                        </div>

                        {/* Predictive Analytics */}
                        <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-4 sm:p-6 space-y-3">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                                <Shield className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                            </div>
                            <div className="space-y-2">
                                <h3 className="text-base sm:text-lg font-semibold text-white">Predictive Analytics</h3>
                                <p className="text-xs sm:text-sm text-gray-400 leading-relaxed">AI-powered insights into learning patterns and progress</p>
                            </div>
                        </div>

                        {/* Secure Platform */}
                        <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-4 sm:p-6 space-y-3">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center">
                                <Lock className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                            </div>
                            <div className="space-y-2">
                                <h3 className="text-base sm:text-lg font-semibold text-white">Secure Platform</h3>
                                <p className="text-xs sm:text-sm text-gray-400 leading-relaxed">Enterprise-grade security for your learning data</p>
                            </div>
                        </div>
                    </div>

                    {/* Status Card */}
                    <div className="bg-slate-800/60 backdrop-blur-sm rounded-xl p-4 sm:p-6">
                        <div className="flex items-start gap-3">
                            <div className="flex items-center gap-2 flex-wrap">
                                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-sm sm:text-base font-semibold text-white">AI System Status: Online</span>
                            </div>
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                            <div className="flex gap-1">
                                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></div>
                                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                            </div>
                        </div>
                        <p className="text-xs sm:text-sm text-gray-400 mt-3">Processing 1,247 active learning sessions</p>
                    </div>
                </div>

                {/* Right Side - Login Panel */}
                <div className="bg-slate-800/60 backdrop-blur-sm rounded-2xl p-6 sm:p-8 lg:p-12 space-y-6 sm:space-y-8 order-1 lg:order-2">

                    {/* Header */}
                    <div className="space-y-2 sm:space-y-3">
                        <h2 className="text-2xl sm:text-3xl font-bold text-white">Access AI Portal</h2>
                        <p className="text-xs sm:text-sm text-gray-400">Continue to your intelligent learning environment</p>
                    </div>

                    {/* Form */}
                    <div className="space-y-5 sm:space-y-6">

                        {/* Email Input */}
                        <div className="space-y-2">
                            <label className="text-xs sm:text-sm text-gray-400">Institutional Email</label>
                            <input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                disabled={isLoading}
                                onKeyPress={(e) => {
                                    if (e.key === 'Enter') {
                                        handleLogin(e);
                                    }
                                }}
                                className="w-full bg-slate-900/80 text-gray-200 placeholder-gray-500 rounded-lg px-4 py-2.5 sm:py-3 text-sm sm:text-base border border-slate-700/50 focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                            />
                        </div>

                        {/* Access Key Input */}
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <label className="text-xs sm:text-sm text-gray-400">Access Key</label>
                                <button
                                    type="button"
                                    disabled={isLoading}
                                    className="text-xs text-violet-400 hover:text-violet-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Recover access
                                </button>
                            </div>
                            <input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                disabled={isLoading}
                                onKeyPress={(e) => {
                                    if (e.key === 'Enter') {
                                        handleLogin(e);
                                    }
                                }}
                                className="w-full bg-slate-900/80 text-gray-200 placeholder-gray-500 rounded-lg px-4 py-2.5 sm:py-3 text-sm sm:text-base border border-slate-700/50 focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                            />
                        </div>

                        {/* AI Authentication Badge */}
                        <div className="space-y-2">
                            <label className="text-xs sm:text-sm text-gray-400">AI Authentication</label>
                            <div className="bg-slate-900/50 rounded-lg px-4 py-2.5 sm:py-3 border border-slate-700/50 flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`}></div>
                                    <span className={`text-xs sm:text-sm font-medium ${isLoading ? 'text-yellow-500' : 'text-green-500'}`}>
                                        {isLoading ? 'Authenticating...' : 'Secure'}
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="button"
                            onClick={handleLogin}
                            disabled={isLoading || !email || !password}
                            className="w-full bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white font-semibold rounded-xl px-6 py-3 sm:py-4 text-sm sm:text-base flex items-center justify-center gap-2 transition-all shadow-lg shadow-violet-500/20 hover:shadow-violet-500/40 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:from-violet-600 disabled:hover:to-purple-600"
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 className="w-4 h-4 sm:w-5 sm:h-5 animate-spin" />
                                    <span>Authenticating...</span>
                                </>
                            ) : (
                                <>
                                    <span>Access AI Portal</span>
                                    <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5" />
                                </>
                            )}
                        </button>
                    </div>

                    {/* Footer Link */}
                    <div className="text-center pt-4">
                        <p className="text-xs sm:text-sm text-gray-400">
                            Need to register?{' '}
                            <button
                                type="button"
                                onClick={()=>router.push("/signup")}
                                disabled={isLoading}
                                className="text-cyan-400 hover:text-cyan-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed hover:cursor-pointer"
                            >
                                SignUp
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}