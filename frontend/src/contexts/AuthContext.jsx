import { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [authLoading, setAuthLoading] = useState(true)

  useEffect(() => {
    const rehydrateAuth = async () => {
      const token = localStorage.getItem('token')
      
      if (!token) {
        setUser(null)
        setAuthLoading(false)
        return
      }

      try {
        const response = await authAPI.getCurrentUser()
        setUser(response.data)
      } catch (error) {
        console.error('Auth rehydration failed:', error)
        localStorage.removeItem('token')
        setUser(null)
      } finally {
        setAuthLoading(false)
      }
    }

    rehydrateAuth()
  }, [])

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  const value = {
    user,
    authLoading,
    setUser,
    logout
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
