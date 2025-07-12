import { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../api/auth'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token') || null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initializeAuth = async () => {
      if (token) {
        try {
          const userData = await authAPI.getCurrentUser(token)
          setUser(userData)
        } catch (error) {
          console.error('Failed to fetch user:', error)
          logout()
        }
      }
      setLoading(false)
    }

    initializeAuth()
  }, [token])

  const login = async (credentials) => {
    try {
      const { access } = await authAPI.login(credentials)
      localStorage.setItem('token', access)
      setToken(access)
      const userData = await authAPI.getCurrentUser(access)
      setUser(userData)
      return { success: true }
    } catch (error) {
      return { success: false, error }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!token,
    isEventOwner: user?.is_event_owner || false,
    isApproved: user?.is_approved || false,
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  return useContext(AuthContext)
}