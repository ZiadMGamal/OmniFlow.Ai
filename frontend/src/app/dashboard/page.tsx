"use client";

import Link from "next/link";
import { LayoutDashboard, Users, Zap, Search, Activity, Cpu } from "lucide-react";
import { CardContent, CardHeader, CardTitle, GlassCard } from "@/components/ui/Card";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const data = [
  { name: 'Mon', tokens: 4000, cost: 2.40 },
  { name: 'Tue', tokens: 3000, cost: 1.39 },
  { name: 'Wed', tokens: 2000, cost: 9.80 },
  { name: 'Thu', tokens: 2780, cost: 3.90 },
  { name: 'Fri', tokens: 1890, cost: 4.80 },
  { name: 'Sat', tokens: 2390, cost: 3.80 },
  { name: 'Sun', tokens: 3490, cost: 4.30 },
];

export default function DashboardPage() {
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r glass hidden md:flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-white/5">
          <span className="font-bold text-lg tracking-tight">OmniFlow<span className="text-accent">.AI</span></span>
        </div>
        <nav className="p-4 space-y-1 flex-1">
          <Link href="/dashboard" className="flex items-center px-3 py-2 text-sm rounded-lg bg-accent/10 text-accent font-medium">Dashboard</Link>
          <Link href="/chat" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Chat</Link>
          <Link href="/agents" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Agents</Link>
          <Link href="/workflows" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Workflows</Link>
          <Link href="/marketplace" className="flex items-center px-3 py-2 text-sm rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">Marketplace</Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative">
        <div className="absolute top-0 right-0 w-[50%] h-[50%] rounded-full bg-purple-500/10 blur-[150px] pointer-events-none" />
        
        <header className="h-16 flex items-center justify-between px-8 border-b border-white/5 glass sticky top-0 z-10">
          <h1 className="text-xl font-semibold tracking-tight">Analytics Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">Last updated: Just now</span>
          </div>
        </header>

        <div className="p-8 space-y-8 z-10 relative">
          {/* Top KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <GlassCard>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Total Tokens</CardTitle>
                <Cpu className="h-4 w-4 text-accent" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">19,550</div>
                <p className="text-xs text-muted-foreground mt-1">+20.1% from last month</p>
              </CardContent>
            </GlassCard>
            
            <GlassCard>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Compute Cost</CardTitle>
                <Activity className="h-4 w-4 text-green-500" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">$30.39</div>
                <p className="text-xs text-muted-foreground mt-1">+4.2% from last month</p>
              </CardContent>
            </GlassCard>

            <GlassCard>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Active Agents</CardTitle>
                <Users className="h-4 w-4 text-purple-500" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">12</div>
                <p className="text-xs text-muted-foreground mt-1">3 currently running tasks</p>
              </CardContent>
            </GlassCard>

            <GlassCard>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Tool Invocations</CardTitle>
                <Zap className="h-4 w-4 text-yellow-500" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">842</div>
                <p className="text-xs text-muted-foreground mt-1">Web Search is most used</p>
              </CardContent>
            </GlassCard>
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <GlassCard className="p-6">
              <h3 className="text-lg font-semibold mb-6">Token Usage Trends</h3>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorTokens" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                    <XAxis dataKey="name" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value / 1000}k`} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '8px' }}
                      itemStyle={{ color: '#fff' }}
                    />
                    <Area type="monotone" dataKey="tokens" stroke="#6366f1" strokeWidth={2} fillOpacity={1} fill="url(#colorTokens)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </GlassCard>

            <GlassCard className="p-6">
              <h3 className="text-lg font-semibold mb-6">Cost Breakdown by Model</h3>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                    <XAxis dataKey="name" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `$${value}`} />
                    <Tooltip 
                      cursor={{fill: 'rgba(255,255,255,0.05)'}}
                      contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '8px' }}
                    />
                    <Bar dataKey="cost" fill="#a855f7" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </GlassCard>
          </div>
        </div>
      </main>
    </div>
  );
}
