import * as React from "react"
import { create<any>(() => ({
  user: null,
  isAuthenticated: false,
  token: null,
  login: (data: any) => {},
  logout: () => {},
}))

// Placeholder for Zustand stores, we'll build them fully next
