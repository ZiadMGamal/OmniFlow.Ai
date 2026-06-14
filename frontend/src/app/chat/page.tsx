"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Paperclip, Mic, Bot, User, Menu } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { cn } from "@/lib/utils";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { id: 1, role: "assistant", content: "Hello! I'm OmniFlow, your multi-tool AI assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const newMsg = { id: Date.now(), role: "user", content: input };
    setMessages(prev => [...prev, newMsg]);
    setInput("");

    // Simulate agent typing
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: Date.now(),
        role: "assistant",
        content: "I'm thinking about how to solve this using my available tools..."
      }]);
    }, 1000);
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar (Desktop) */}
      <aside className="w-64 border-r glass hidden md:flex flex-col">
        <div className="h-16 flex items-center px-4 border-b border-border/50">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-purple-500 flex items-center justify-center text-white font-bold">
              <Bot size={20} />
            </div>
            <span className="font-bold tracking-tight">OmniFlow<span className="text-accent">.AI</span></span>
          </div>
        </div>
        <div className="p-4 flex-1 overflow-y-auto">
          <Button variant="outline" className="w-full justify-start mb-6 rounded-full glass">
            + New Chat
          </Button>
          <div className="space-y-1">
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-2">Recent</div>
            <button className="w-full text-left px-3 py-2 text-sm rounded-lg hover:bg-white/5 truncate">Research Python AI</button>
            <button className="w-full text-left px-3 py-2 text-sm rounded-lg hover:bg-white/5 truncate">Debug FastAPI Server</button>
            <button className="w-full text-left px-3 py-2 text-sm rounded-lg hover:bg-white/5 truncate">Analyze Q3 Data</button>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative">
        {/* Background Gradients */}
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-accent/5 blur-[150px] pointer-events-none" />
        
        {/* Mobile Header */}
        <header className="md:hidden h-14 glass flex items-center px-4 border-b">
          <Button variant="ghost" size="icon" className="mr-2">
            <Menu size={20} />
          </Button>
          <span className="font-bold tracking-tight">OmniFlow<span className="text-accent">.AI</span></span>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth pb-32">
          {messages.map((msg) => (
            <div 
              key={msg.id} 
              className={cn(
                "flex gap-4 max-w-3xl mx-auto animate-fade-in",
                msg.role === "user" ? "flex-row-reverse" : "flex-row"
              )}
            >
              <div className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                msg.role === "user" ? "bg-secondary text-secondary-foreground" : "bg-gradient-to-br from-accent to-purple-500 text-white"
              )}>
                {msg.role === "user" ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className={cn(
                "px-5 py-3.5 rounded-2xl max-w-[85%] leading-relaxed",
                msg.role === "user" 
                  ? "bg-secondary text-secondary-foreground rounded-tr-sm" 
                  : "glass rounded-tl-sm shadow-sm"
              )}>
                {msg.content}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-background via-background/90 to-transparent pt-10 pb-6 px-4">
          <div className="max-w-3xl mx-auto relative group">
            <form onSubmit={handleSend} className="relative flex items-center glass rounded-2xl shadow-lg border-white/10 transition-all duration-300 focus-within:border-accent/50 focus-within:shadow-[0_0_20px_rgba(99,102,241,0.2)]">
              <Button type="button" variant="ghost" size="icon" className="absolute left-2 text-muted-foreground hover:text-foreground rounded-xl">
                <Paperclip size={20} />
              </Button>
              <Input 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask OmniFlow to research, code, or analyze..." 
                className="border-0 bg-transparent h-14 pl-12 pr-24 shadow-none focus-visible:ring-0 text-base"
              />
              <div className="absolute right-2 flex items-center gap-1">
                <Button type="button" variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground rounded-xl hidden sm:flex">
                  <Mic size={20} />
                </Button>
                <Button type="submit" size="icon" className="h-10 w-10 rounded-xl bg-accent hover:bg-accent/90 text-white shadow-md transition-transform active:scale-95 disabled:opacity-50" disabled={!input.trim()}>
                  <Send size={18} className="ml-0.5" />
                </Button>
              </div>
            </form>
            <div className="text-center text-xs text-muted-foreground mt-3">
              OmniFlow can make mistakes. Consider verifying critical information.
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
