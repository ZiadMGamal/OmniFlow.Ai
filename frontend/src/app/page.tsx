import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Bot, Sparkles, Zap, Shield, GitBranch, ArrowRight } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background overflow-hidden relative">
      {/* Background Gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-accent/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-500/20 blur-[120px] pointer-events-none" />
      
      {/* Navbar */}
      <header className="fixed top-0 w-full glass z-50 px-6 py-4 flex items-center justify-between border-b-0">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-purple-500 flex items-center justify-center text-white font-bold">
            <Bot size={20} />
          </div>
          <span className="font-bold text-xl tracking-tight">OmniFlow<span className="text-accent">.AI</span></span>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/login" className="text-sm font-medium hover:text-accent transition-colors">Sign In</Link>
          <Button asChild className="rounded-full shadow-[0_0_15px_rgba(99,102,241,0.5)]">
            <Link href="/chat">Get Started</Link>
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <main className="pt-32 pb-20 px-6 max-w-7xl mx-auto flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass text-sm text-muted-foreground mb-8 animate-fade-in">
          <Sparkles size={14} className="text-accent" />
          <span>The next generation of AI agents</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 max-w-4xl animate-slide-up" style={{ animationDelay: "100ms", animationFillMode: "both" }}>
          The Universal Multi-Tool <br className="hidden md:block" />
          <span className="text-gradient">AI Agent Platform</span>
        </h1>
        
        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10 animate-slide-up" style={{ animationDelay: "200ms", animationFillMode: "both" }}>
          Build, deploy, and interact with specialized AI agents capable of reasoning, researching, coding, and executing complex workflows autonomously.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center gap-4 animate-slide-up" style={{ animationDelay: "300ms", animationFillMode: "both" }}>
          <Button size="lg" asChild className="rounded-full h-14 px-8 text-lg w-full sm:w-auto shadow-[0_0_20px_rgba(99,102,241,0.6)]">
            <Link href="/chat">
              Start Chatting <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
          <Button variant="glass" size="lg" className="rounded-full h-14 px-8 text-lg w-full sm:w-auto">
            View Documentation
          </Button>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-3 gap-6 mt-32 w-full animate-slide-up" style={{ animationDelay: "400ms", animationFillMode: "both" }}>
          <div className="glass p-8 rounded-2xl text-left hover:bg-white/5 transition-all">
            <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center text-accent mb-6">
              <Zap size={24} />
            </div>
            <h3 className="text-xl font-semibold mb-3">Multi-Agent Orchestration</h3>
            <p className="text-muted-foreground">Seamlessly coordinate researchers, coders, and APIs via an intelligent supervisor graph.</p>
          </div>
          <div className="glass p-8 rounded-2xl text-left hover:bg-white/5 transition-all">
            <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center text-purple-500 mb-6">
              <GitBranch size={24} />
            </div>
            <h3 className="text-xl font-semibold mb-3">Infinite Tool Use</h3>
            <p className="text-muted-foreground">Equip agents with real-time web search, python sandboxes, file editing, and direct DB access.</p>
          </div>
          <div className="glass p-8 rounded-2xl text-left hover:bg-white/5 transition-all">
            <div className="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center text-green-500 mb-6">
              <Shield size={24} />
            </div>
            <h3 className="text-xl font-semibold mb-3">Enterprise Grade RAG</h3>
            <p className="text-muted-foreground">Built on Qdrant and Redis for infinite persistent semantic memory and hyper-fast context.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
