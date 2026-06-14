import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import api from "@/lib/api";

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (credentials: any) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  setTokens: (token: string, refreshToken: string) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (credentials) => {
        set({ isLoading: true, error: null });
        try {
          const response = await api.post("/auth/login", credentials);
          const { access_token, refresh_token, user } = response.data;
          
          set({
            token: access_token,
            refreshToken: refresh_token,
            user,
            isAuthenticated: true,
            isLoading: false
          });
        } catch (error: any) {
          set({ 
            error: error.response?.data?.detail || "Login failed", 
            isLoading: false 
          });
          throw error;
        }
      },

      register: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const response = await api.post("/auth/register", data);
          const { access_token, refresh_token, user } = response.data;
          
          set({
            token: access_token,
            refreshToken: refresh_token,
            user,
            isAuthenticated: true,
            isLoading: false
          });
        } catch (error: any) {
          set({ 
            error: error.response?.data?.detail || "Registration failed", 
            isLoading: false 
          });
          throw error;
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
        });
      },

      setTokens: (token, refreshToken) => {
        set({ token, refreshToken });
      },

      clearError: () => {
        set({ error: null });
      }
    }),
    {
      name: "omniflow-auth",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ 
        token: state.token, 
        refreshToken: state.refreshToken, 
        user: state.user,
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);
