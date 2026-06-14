"use client";

import React, { useState, useCallback } from 'react';
import ReactFlow, {
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
  Node,
  Edge,
  Connection,
  NodeChange,
  EdgeChange,
  BackgroundVariant,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { ArrowLeft, Play, Save, Settings, Plus } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { CustomNode } from '@/components/workflow/CustomNode';

const nodeTypes = {
  custom: CustomNode,
};

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'custom',
    position: { x: 250, y: 50 },
    data: { label: 'Webhook Trigger', type: 'trigger', icon: 'trigger', description: 'Listens for incoming GitHub PRs' },
  },
  {
    id: '2',
    type: 'custom',
    position: { x: 250, y: 200 },
    data: { label: 'Code Review Agent', type: 'agent', icon: 'agent', description: 'Analyzes code quality & security' },
  },
  {
    id: '3',
    type: 'custom',
    position: { x: 100, y: 350 },
    data: { label: 'Web Search', type: 'tool', icon: 'web_search', description: 'Finds recent CVEs' },
  },
  {
    id: '4',
    type: 'custom',
    position: { x: 400, y: 350 },
    data: { label: 'Slack Notification', type: 'tool', icon: 'email', description: 'Posts review summary' },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#6366f1', strokeWidth: 2 } },
  { id: 'e2-3', source: '2', target: '3', animated: true, style: { stroke: '#a1a1aa', strokeWidth: 2 } },
  { id: 'e2-4', source: '2', target: '4', animated: true, style: { stroke: '#a1a1aa', strokeWidth: 2 } },
];

export default function WorkflowBuilderPage({ params }: { params: { id: string } }) {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);

  const onNodesChange = useCallback(
    (changes: NodeChange[]) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  
  const onEdgesChange = useCallback(
    (changes: EdgeChange[]) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#6366f1', strokeWidth: 2 } }, eds)),
    []
  );

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Topbar */}
      <header className="h-14 flex items-center justify-between px-4 border-b border-white/5 glass z-50">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" asChild className="rounded-lg">
            <Link href="/workflows">
              <ArrowLeft size={18} />
            </Link>
          </Button>
          <div className="flex flex-col">
            <span className="font-semibold text-sm tracking-tight">GitHub PR Review Pipeline</span>
            <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Unsaved Changes</span>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" className="rounded-lg">
            <Settings size={16} className="mr-2" /> Configure
          </Button>
          <Button variant="outline" size="sm" className="rounded-lg glass border-white/10">
            <Save size={16} className="mr-2" /> Save Draft
          </Button>
          <Button size="sm" className="rounded-lg shadow-[0_0_15px_rgba(99,102,241,0.5)]">
            <Play size={16} className="mr-2" /> Deploy & Run
          </Button>
        </div>
      </header>

      {/* Main Builder Area */}
      <div className="flex-1 flex relative">
        {/* Node Palette Sidebar */}
        <div className="w-64 border-r border-white/5 glass z-10 p-4 flex flex-col gap-6 overflow-y-auto">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Triggers</h3>
            <div className="space-y-2">
              <div className="p-3 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 cursor-grab flex items-center gap-3 transition-colors">
                <Zap size={16} className="text-purple-500" />
                <span className="text-sm font-medium">Webhook</span>
              </div>
              <div className="p-3 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 cursor-grab flex items-center gap-3 transition-colors">
                <Clock size={16} className="text-purple-500" />
                <span className="text-sm font-medium">Schedule (Cron)</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Agents</h3>
            <div className="space-y-2">
              <div className="p-3 rounded-lg border border-accent/30 bg-accent/5 hover:bg-accent/10 cursor-grab flex items-center gap-3 transition-colors">
                <Bot size={16} className="text-accent" />
                <span className="text-sm font-medium">ReAct Agent</span>
              </div>
              <div className="p-3 rounded-lg border border-accent/30 bg-accent/5 hover:bg-accent/10 cursor-grab flex items-center gap-3 transition-colors">
                <Network size={16} className="text-accent" />
                <span className="text-sm font-medium">Supervisor</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Tools</h3>
            <div className="space-y-2">
              <div className="p-3 rounded-lg border border-blue-500/30 bg-blue-500/5 hover:bg-blue-500/10 cursor-grab flex items-center gap-3 transition-colors">
                <Globe size={16} className="text-blue-500" />
                <span className="text-sm font-medium">Web Search</span>
              </div>
              <div className="p-3 rounded-lg border border-blue-500/30 bg-blue-500/5 hover:bg-blue-500/10 cursor-grab flex items-center gap-3 transition-colors">
                <Code size={16} className="text-blue-500" />
                <span className="text-sm font-medium">Python Sandbox</span>
              </div>
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 h-full relative bg-[#09090b]">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            fitView
            className="dark"
          >
            <Background color="#27272a" variant={BackgroundVariant.Dots} gap={16} size={1} />
            <Controls className="bg-card border-border fill-foreground" />
          </ReactFlow>
        </div>
      </div>
    </div>
  );
}
