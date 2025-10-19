import React, { useState, useRef, useEffect } from "react";
import { X, Send, Phone, Loader2 } from "lucide-react";

interface Message {
  id: number;
  sender: "user" | "bot";
  message: string;
  timestamp: string;
}

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
  platform: "website" | "mobile" | "desktop";
  created_at: string;
  updated_at: string;
}

interface Coordinates {
  latitude: number;
  longitude: number;
  formatted_coordinates: string;
}

interface ChatBotProps {
  isOpen: boolean;
  onClose: () => void;
  loc: { lat: number; lon: number } | null;
  status: DeviceStatus;
  user: User;
}

const ChatBot: React.FC<ChatBotProps> = ({
  isOpen,
  onClose,
  loc,
  status,
  user,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      sender: "bot",
      message:
        "Hello! I'm your Emergency AI Assistant. How can I help you today?",
      timestamp: new Date().toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);
  const [inputValue, setInputValue] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (inputValue.trim() && !isLoading) {
      const userMessage: Message = {
        id: messages.length + 1,
        sender: "user",
        message: inputValue,
        timestamp: new Date().toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, userMessage]);
      const currentMessage = inputValue;
      setInputValue("");
      setIsLoading(true);

      try {
        const coordinates: Coordinates = loc
          ? {
              latitude: loc.lat,
              longitude: loc.lon,
              formatted_coordinates: `${loc.lat.toFixed(6)}, ${loc.lon.toFixed(
                6
              )}`,
            }
          : {
              latitude: 0,
              longitude: 0,
              formatted_coordinates: "0.000000, 0.000000",
            };

        const requestPayload = {
          user: {
            userid: user.userid,
            username: user.username,
            password: user.password,
            is_loggedin: user.is_loggedin,
            phone_number: user.phone_number,
            platform: user.platform,
            created_at: user.created_at,
            updated_at: user.updated_at,
          },
          message: currentMessage,
          status: {
            connection: status.connection
              ? {
                  downlink: Number(status.connection.downlink),
                  effectiveType: status.connection.effectiveType || "unknown",
                  // 👇 ensure rtt is an integer
                  rtt: Math.round(Number(status.connection.rtt) || 0),
                }
              : {
                  downlink: 0,
                  effectiveType: "unknown",
                  rtt: 0,
                },
            battery: status.battery
              ? {
                  // 👇 ensure integer
                  level: Math.round(Number(status.battery.level) || 100),
                  charging: Boolean(status.battery.charging),
                }
              : {
                  level: 100,
                  charging: false,
                },
          },
          coordinates: loc
            ? {
                latitude: Number(loc.lat),
                longitude: Number(loc.lon),
                formatted_coordinates: `${loc.lat.toFixed(
                  6
                )}, ${loc.lon.toFixed(6)}`,
              }
            : {
                latitude: 0,
                longitude: 0,
                formatted_coordinates: "0.000000, 0.000000",
              },
        };

        console.log(
          "Sending payload:",
          JSON.stringify(requestPayload, null, 2)
        );

        // ✅ Replaced axios with fetch
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 40000); // 30s timeout

        const response = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(requestPayload),
          signal: controller.signal,
        });

        clearTimeout(timeout);

        if (!response.ok) {
          const errorData = await response.json().catch(() => null);
          throw new Error(
            errorData?.detail
              ? `Error: ${errorData.detail}`
              : `Server error: ${response.status}`
          );
        }

        const data = await response.text(); // FastAPI can return plain text or JSON
        const botMessage =
          data || "I received your message. How else can I assist you?";

        const botResponse: Message = {
          id: messages.length + 2,
          sender: "bot",
          message: botMessage,
          timestamp: new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };

        setMessages((prev) => [...prev, botResponse]);
      } catch (error: any) {
        console.error("Error sending message:", error);

        let errorMsg =
          "Sorry, I encountered an error processing your request. Please try again or contact emergency services directly if this is urgent.";

        if (error.name === "AbortError") {
          errorMsg = "Request timed out. Please check your connection.";
        } else if (error.message.includes("Server error")) {
          errorMsg = error.message;
        } else if (error.message.includes("Failed to fetch")) {
          errorMsg =
            "Unable to reach the server. Please check your connection.";
        } else if (error.message) {
          errorMsg = `Request error: ${error.message}`;
        }

        const errorMessage: Message = {
          id: messages.length + 2,
          sender: "bot",
          message: errorMsg,
          timestamp: new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };

        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === "Enter" && !isLoading) {
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-4 right-4 md:bottom-6 md:right-6 z-50 animate-in slide-in-from-bottom-5 duration-300 w-full max-w-[calc(100vw-2rem)] md:max-w-md">
      <div className="w-full h-[500px] md:h-[500px] bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-3 md:p-4 flex items-center justify-between">
          <div className="flex items-center gap-2 md:gap-3">
            <div className="w-8 h-8 md:w-10 md:h-10 bg-white/20 rounded-full flex items-center justify-center">
              <Phone className="w-4 h-4 md:w-5 md:h-5 text-white" />
            </div>
            <div>
              <h3 className="text-white font-semibold text-base md:text-lg">
                Emergency AI Assistant
              </h3>
              <p className="text-emerald-100 text-xs">
                {isLoading ? "Typing..." : "Online • Ready to help"}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white/20 rounded-full h-8 w-8 md:h-10 md:w-10 flex items-center justify-center transition-colors"
          >
            <X className="w-4 h-4 md:w-5 md:h-5" />
          </button>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-3 md:p-4 space-y-3 md:space-y-4 bg-slate-900">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[85%] md:max-w-[75%] rounded-2xl px-3 py-2 md:px-4 md:py-3 ${
                  msg.sender === "user"
                    ? "bg-emerald-500 text-white rounded-br-sm"
                    : "bg-slate-800 text-slate-200 rounded-bl-sm"
                }`}
              >
                <p className="text-xs md:text-sm leading-relaxed break-words">
                  {msg.message}
                </p>
                <p
                  className={`text-[10px] md:text-xs mt-1 ${
                    msg.sender === "user"
                      ? "text-emerald-100"
                      : "text-slate-500"
                  }`}
                >
                  {msg.timestamp}
                </p>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-slate-800 text-slate-200 rounded-2xl rounded-bl-sm px-3 py-2 md:px-4 md:py-3">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-xs md:text-sm">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-3 md:p-4 bg-slate-800 border-t border-slate-700">
          {loc && (
            <div className="mb-2 text-xs text-slate-400 flex items-center gap-1">
              <span>📍</span>
              <span>
                Location: {loc.lat.toFixed(4)}, {loc.lon.toFixed(4)}
              </span>
            </div>
          )}

          <div className="flex gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setInputValue(e.target.value)
              }
              onKeyPress={handleKeyPress}
              placeholder={
                isLoading ? "AI is responding..." : "Describe your emergency..."
              }
              disabled={isLoading}
              className="flex-1 px-3 py-2 md:px-4 md:py-3 bg-slate-900 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors duration-200 text-xs md:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl px-3 md:px-4 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[40px]"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
