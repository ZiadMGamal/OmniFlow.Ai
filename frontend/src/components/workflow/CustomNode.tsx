import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { Bot, Zap, Globe, Code, Database, Mail } from 'lucide-react';

const iconMap = {
  agent: Bot,
  trigger: Zap,
  web_search: Globe,
  python_executor: Code,
  database: Database,
  email: Mail,
};

const colorMap = {
  agent: "border-accent shadow-[0_0_15px_rgba(99,102,241,0.2)] bg-accent/5",
  trigger: "border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.2)] bg-purple-500/5",
  tool: "border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.2)] bg-blue-500/5",
};

export const CustomNode = memo(({ data, isConnectable }: any) => {
  const Icon = iconMap[data.icon as keyof typeof iconMap] || Bot;
  const nodeType = data.type as keyof typeof colorMap;
  const colorClass = colorMap[nodeType] || colorMap.tool;

  return (
    <div className={`px-4 py-3 shadow-lg rounded-xl glass border-2 ${colorClass} min-w-[200px] backdrop-blur-xl transition-all hover:scale-[1.02]`}>
      <Handle
        type="target"
        position={Position.Top}
        isConnectable={isConnectable}
        className="w-3 h-3 bg-foreground border-2 border-background"
      />
      
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg bg-background/50 flex items-center justify-center`}>
          <Icon size={16} className="text-foreground" />
        </div>
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-0.5">{data.type}</div>
          <div className="text-sm font-bold text-foreground">{data.label}</div>
        </div>
      </div>
      
      {data.description && (
        <div className="mt-2 text-xs text-muted-foreground border-t border-white/10 pt-2">
          {data.description}
        </div>
      )}

      <Handle
        type="source"
        position={Position.Bottom}
        id="a"
        isConnectable={isConnectable}
        className="w-3 h-3 bg-foreground border-2 border-background"
      />
    </div>
  );
});

CustomNode.displayName = "CustomNode";
