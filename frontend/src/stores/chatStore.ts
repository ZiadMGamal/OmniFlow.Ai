import { create } from "zustand";
import { io, Socket } from "socket.io-client";
import { useAuthStore } from "./authStore";
import api from "@/lib/api";

export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
  tools_called?: any[];
}

export interface Conversation {
  id: string;
  title: string;
  agent_id: string;
  updated_at: string;
}

interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  messages: Message[];
  isAgentTyping: boolean;
  socket: Socket | null;
  isConnected: boolean;
  
  // Actions
  fetchConversations: () => Promise<void>;
  setActiveConversation: (id: string) => Promise<void>;
  createConversation: (agentId: string, title: string) => Promise<string>;
  sendMessage: (content: string) => Promise<void>;
  connectWebSocket: (conversationId: string) => void;
  disconnectWebSocket: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  conversations: [],
  activeConversationId: null,
  messages: [],
  isAgentTyping: false,
  socket: null,
  isConnected: false,

  fetchConversations: async () => {
    try {
      const res = await api.get("/conversations");
      set({ conversations: res.data.conversations });
    } catch (error) {
      console.error("Failed to fetch conversations", error);
    }
  },

  setActiveConversation: async (id: string) => {
    set({ activeConversationId: id, messages: [] });
    try {
      const res = await api.get(`/conversations/${id}/messages`);
      set({ messages: res.data });
      get().connectWebSocket(id);
    } catch (error) {
      console.error("Failed to fetch messages", error);
    }
  },

  createConversation: async (agentId: string, title: string) => {
    try {
      const res = await api.post("/conversations", { agent_id: agentId, title });
      const newConv = res.data;
      set((state) => ({ 
        conversations: [newConv, ...state.conversations] 
      }));
      return newConv.id;
    } catch (error) {
      console.error("Failed to create conversation", error);
      throw error;
    }
  },

  sendMessage: async (content: string) => {
    const { socket, activeConversationId } = get();
    if (!socket || !activeConversationId) return;

    // Optimistic UI update
    const tempId = `temp_${Date.now()}`;
    const newMsg: Message = {
      id: tempId,
      role: "user",
      content,
      created_at: new Date().toISOString()
    };

    set((state) => ({
      messages: [...state.messages, newMsg],
      isAgentTyping: true
    }));

    // Send via WebSocket
    socket.emit("message", { content });
  },

  connectWebSocket: (conversationId: string) => {
    // Clean up existing socket
    get().disconnectWebSocket();

    const token = useAuthStore.getState().token;
    if (!token) return;

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
    
    // For FastAPI we use standard WebSocket, not socket.io
    // This is a simplified wrapper to adapt to standard WS
    const ws = new WebSocket(`${wsUrl}/api/v1/chat/ws/${conversationId}?token=${token}`);

    ws.onopen = () => {
      set({ isConnected: true });
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.event === "message_chunk") {
        // Handle streaming updates
        set((state) => {
          const msgs = [...state.messages];
          // Simple implementation: just append complete messages for MVP
          if (data.data.is_complete) {
            msgs.push({
              id: Date.now().toString(),
              role: "assistant",
              content: data.data.content,
              created_at: new Date().toISOString()
            });
            return { messages: msgs, isAgentTyping: false };
          }
          return state;
        });
      }
    };

    ws.onclose = () => {
      set({ isConnected: false, socket: null });
    };

    // Store a mock Socket object that adapts standard WS to our API
    set({ 
      socket: {
        emit: (event: string, payload: any) => {
          ws.send(JSON.stringify(payload));
        },
        close: () => ws.close()
      } as any 
    });
  },

  disconnectWebSocket: () => {
    const { socket } = get();
    if (socket) {
      socket.close();
      set({ socket: null, isConnected: false });
    }
  }
}));
