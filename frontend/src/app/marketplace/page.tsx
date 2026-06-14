"use client";

import Link from "next/link";
import { Download, Globe, MessageSquare, Database, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { CardContent, CardHeader, GlassCard } from "@/components/ui/Card";

const integrations = [
  { id: 1, name: "Tavily Search", provider: "Tavily", desc: "Real-time AI web search engine.", category: "Search", icon: Globe, installed: true },
  { id: 2, name: "Slack", provider: "Slack", desc: "Send messages and read channels.", category: "Communication", icon: MessageSquare, installed: true },
  { id: 3, name: "PostgreSQL", provider: "Community", desc: "Direct database querying tool.", category: "Database", icon: Database, installed: false },
  { id: 4, name: "GitHub", provider: "GitHub", desc: "Manage PRs, issues, and repos.", category: "Developer Tools", icon: Database, installed: false },
];

export default function MarketplacePage() {
  return (
    <div className="flex h-screen bg-background">
      <aside className="w-64 border-r glass hidden md:flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-white/5">
          <span className="font-bold text-lg tracking-tight">OmniFlow<span className="text-accent">.AI</span></span>
        </div>
        <nav className="p-4 space-y-1 flex-1">
          <Link href="/dashboard" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Dashboard</Link>
          <Link href="/chat" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Chat</Link>
          <Link href="/agents" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Agents</Link>
          <Link href="/workflows" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Workflows</Link>
          <Link href="/marketplace" className="flex items-center px-3 py-2 text-sm rounded-lg bg-accent/10 text-accent font-medium">Marketplace</Link>
        </nav>
      </aside>

      <main className="flex-1 overflow-y-auto relative">
        <header className="h-48 glass flex flex-col justify-end px-8 pb-8 border-b border-white/5 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-[50%] h-[150%] rounded-full bg-blue-500/10 blur-[150px] pointer-events-none" />
          <h1 className="text-3xl font-bold tracking-tight mb-2">Integration Marketplace</h1>
          <p className="text-muted-foreground max-w-xl">Supercharge your agents with pre-built tools, connectors, and external API integrations.</p>
        </header>

        <div className="p-8">
          <div className="flex items-center gap-4 mb-8 border-b border-white/5 pb-4">
            <button className="text-sm font-medium text-accent border-b-2 border-accent pb-4 -mb-[17px]">All Integrations</button>
            <button className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors pb-4 -mb-[17px]">Installed</button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {integrations.map((item) => (
              <GlassCard key={item.id} className="flex flex-col h-full hover:bg-white/5 transition-colors">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center">
                      <item.icon size={24} className="text-foreground" />
                    </div>
                    {item.installed ? (
                      <div className="flex items-center text-xs text-green-500 font-medium px-2 py-1 rounded-full bg-green-500/10 border border-green-500/20">
                        <CheckCircle2 size={12} className="mr-1" /> Installed
                      </div>
                    ) : (
                      <Button variant="outline" size="sm" className="rounded-full h-8 text-xs">
                        <Download size={14} className="mr-1" /> Install
                      </Button>
                    )}
                  </div>
                  <h3 className="text-lg font-semibold mt-4">{item.name}</h3>
                  <div className="text-xs text-muted-foreground">By {item.provider}</div>
                </CardHeader>
                <CardContent className="pt-0 flex-1 flex flex-col">
                  <p className="text-sm text-muted-foreground mb-4">{item.desc}</p>
                  <div className="mt-auto">
                    <span className="text-xs px-2 py-1 rounded-md bg-white/5 border border-white/10">{item.category}</span>
                  </div>
                </CardContent>
              </GlassCard>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
