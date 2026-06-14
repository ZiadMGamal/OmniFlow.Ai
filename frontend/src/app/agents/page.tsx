"use client";

import Link from "next/link";
import { Plus, Settings2, ShieldAlert, Cpu, Globe, ArrowUpRight } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { CardContent, CardHeader, GlassCard } from "@/components/ui/Card";
import { cn } from "@/lib/utils";

const agents = [
  { id: 1, name: "Data Analyst Pro", model: "GPT-4o", tools: ["Python Sandbox", "DB Access"], type: "ReAct", status: "online" },
  { id: 2, name: "Web Researcher", model: "Claude 3.5 Sonnet", tools: ["Tavily Search"], type: "ReAct", status: "online" },
  { id: 3, name: "Customer Triage", model: "Gemini 1.5 Pro", tools: ["Zendesk", "Email"], type: "Supervisor", status: "offline" },
  { id: 4, name: "Code Reviewer", model: "Claude 3 Opus", tools: ["GitHub", "Python Sandbox"], type: "ReAct", status: "online" },
];

export default function AgentsPage() {
  return (
    <div className="flex h-screen bg-background">
      <aside className="w-64 border-r glass hidden md:flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-white/5">
          <span className="font-bold text-lg tracking-tight">OmniFlow<span className="text-accent">.AI</span></span>
        </div>
        <nav className="p-4 space-y-1 flex-1">
          <Link href="/dashboard" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Dashboard</Link>
          <Link href="/chat" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Chat</Link>
          <Link href="/agents" className="flex items-center px-3 py-2 text-sm rounded-lg bg-accent/10 text-accent font-medium">Agents</Link>
          <Link href="/workflows" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Workflows</Link>
          <Link href="/marketplace" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Marketplace</Link>
        </nav>
      </aside>

      <main className="flex-1 overflow-y-auto relative">
        <header className="h-16 flex items-center justify-between px-8 border-b border-white/5 glass sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <Cpu className="text-accent" size={20} />
            <h1 className="text-xl font-semibold tracking-tight">Agents Fleet</h1>
          </div>
          <Button asChild className="rounded-full shadow-md">
            <Link href="/agents/new">
              <Plus size={16} className="mr-2" />
              Create Agent
            </Link>
          </Button>
        </header>

        <div className="p-8 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {agents.map((agent) => (
              <GlassCard key={agent.id} className="group hover:border-accent/50 transition-all flex flex-col h-full">
                <CardHeader className="pb-4 border-b border-white/5">
                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-2">
                      <div className={cn(
                        "w-2 h-2 rounded-full",
                        agent.status === "online" ? "bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]" : "bg-muted-foreground"
                      )} />
                      <h3 className="font-semibold text-lg tracking-tight">{agent.name}</h3>
                    </div>
                    <Button variant="ghost" size="icon" className="h-8 w-8 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
                      <Settings2 size={16} />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="pt-4 flex-1 flex flex-col gap-4">
                  <div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Model</div>
                    <div className="text-sm font-medium">{agent.model}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Architecture</div>
                    <div className="text-sm font-medium">{agent.type}</div>
                  </div>
                  <div className="mt-auto">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Tools</div>
                    <div className="flex flex-wrap gap-2">
                      {agent.tools.map(tool => (
                        <div key={tool} className="text-xs px-2 py-1 rounded-md bg-white/5 border border-white/10 flex items-center gap-1">
                          {tool.includes("Search") ? <Globe size={12} className="text-blue-400" /> : <Cpu size={12} className="text-purple-400" />}
                          {tool}
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
                <div className="p-4 border-t border-white/5 mt-auto">
                  <Button variant="ghost" className="w-full justify-between group/btn hover:bg-accent/10 hover:text-accent">
                    Open Console
                    <ArrowUpRight size={16} className="opacity-50 group-hover/btn:opacity-100 transition-opacity" />
                  </Button>
                </div>
              </GlassCard>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
