"use client";

import { useState } from "react";
import Link from "next/link";
import { Plus, Play, MoreVertical, Network, Clock, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle, GlassCard } from "@/components/ui/Card";
import { cn } from "@/lib/utils";

const mockWorkflows = [
  { id: "1", name: "Customer Support Triage", status: "active", lastRun: "2 mins ago", nodes: 5 },
  { id: "2", name: "Daily Competitor Analysis", status: "idle", lastRun: "12 hours ago", nodes: 8 },
  { id: "3", name: "GitHub Issue Resolver", status: "failed", lastRun: "1 day ago", nodes: 4 },
];

export default function WorkflowsPage() {
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar - Reusable component in a real app */}
      <aside className="w-64 border-r glass hidden md:flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-white/5">
          <span className="font-bold text-lg tracking-tight">OmniFlow<span className="text-accent">.AI</span></span>
        </div>
        <nav className="p-4 space-y-1 flex-1">
          <Link href="/dashboard" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Dashboard</Link>
          <Link href="/chat" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Chat</Link>
          <Link href="/agents" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Agents</Link>
          <Link href="/workflows" className="flex items-center px-3 py-2 text-sm rounded-lg bg-accent/10 text-accent font-medium">Workflows</Link>
          <Link href="/marketplace" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Marketplace</Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {/* Ambient Gradients */}
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] rounded-full bg-accent/10 blur-[120px] pointer-events-none" />

        <header className="h-16 flex items-center justify-between px-8 border-b border-white/5 glass z-10">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-accent/20 text-accent">
              <Network size={20} />
            </div>
            <h1 className="text-xl font-semibold tracking-tight">Workflows</h1>
          </div>
          <Button asChild className="rounded-full shadow-md">
            <Link href="/workflows/new">
              <Plus size={16} className="mr-2" />
              Create Workflow
            </Link>
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-8 space-y-8 z-10">
          {/* Stats Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <GlassCard>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Active Workflows</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">12</div>
                <p className="text-xs text-green-500 mt-1 flex items-center"><CheckCircle2 size={12} className="mr-1" /> All systems operational</p>
              </CardContent>
            </GlassCard>
            <GlassCard>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Executions (24h)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-gradient">1,492</div>
                <p className="text-xs text-muted-foreground mt-1">+14% from yesterday</p>
              </CardContent>
            </GlassCard>
            <GlassCard>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Avg Compute Time</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">2.4s</div>
                <p className="text-xs text-muted-foreground mt-1">Highly optimized</p>
              </CardContent>
            </GlassCard>
          </div>

          {/* Workflows List */}
          <div className="space-y-4">
            <h2 className="text-lg font-medium tracking-tight mb-4">Your Pipelines</h2>
            {mockWorkflows.map((wf) => (
              <GlassCard key={wf.id} className="group flex items-center justify-between p-4 hover:border-accent/50 transition-all">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-accent/30 transition-colors">
                    <Network size={20} className="text-muted-foreground group-hover:text-accent transition-colors" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground tracking-tight">{wf.name}</h3>
                    <div className="flex items-center gap-3 text-xs text-muted-foreground mt-1">
                      <span className="flex items-center gap-1">
                        <div className={cn(
                          "w-2 h-2 rounded-full",
                          wf.status === "active" ? "bg-green-500" : wf.status === "failed" ? "bg-red-500" : "bg-yellow-500"
                        )} />
                        {wf.status.charAt(0).toUpperCase() + wf.status.slice(1)}
                      </span>
                      <span className="flex items-center gap-1"><Clock size={12} /> {wf.lastRun}</span>
                      <span>{wf.nodes} Nodes</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Button variant="ghost" size="icon" className="rounded-lg hover:bg-green-500/20 hover:text-green-500">
                    <Play size={18} />
                  </Button>
                  <Button variant="ghost" size="icon" className="rounded-lg" asChild>
                    <Link href={`/workflows/${wf.id}`}>
                      <Network size={18} />
                    </Link>
                  </Button>
                  <Button variant="ghost" size="icon" className="rounded-lg">
                    <MoreVertical size={18} />
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
