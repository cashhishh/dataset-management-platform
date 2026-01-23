import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authAPI } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import Footer from '../components/Footer'

const ACCOUNT_HISTORY_KEY = 'account_history'

function Login() {
  const navigate = useNavigate()
  const { user, authLoading, setUser } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [accountHistory, setAccountHistory] = useState([])
  const [fieldErrors, setFieldErrors] = useState({})

  useEffect(() => {
    const history = JSON.parse(localStorage.getItem(ACCOUNT_HISTORY_KEY) || '[]')
    setAccountHistory(history)
  }, [])

  useEffect(() => {
    if (!authLoading && user) {
      navigate('/datasets', { replace: true })
    }
  }, [user, authLoading, navigate])

  const saveAccountToHistory = (email) => {
    const history = JSON.parse(localStorage.getItem(ACCOUNT_HISTORY_KEY) || '[]')
    if (!history.includes(email)) {
      const newHistory = [email, ...history].slice(0, 5)
      localStorage.setItem(ACCOUNT_HISTORY_KEY, JSON.stringify(newHistory))
    }
  }

  const handleAccountClick = (email) => {
    setFormData({ ...formData, email })
    setError('')
    setFieldErrors({})
  }

  const validateForm = () => {
    const errors = {}
    if (!formData.email.trim()) {
      errors.email = 'Email is required'
    }
    if (!formData.password) {
      errors.password = 'Password is required'
    }
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setFieldErrors({})

    if (!validateForm()) {
      return
    }

    setLoading(true)

    try {
      const response = await authAPI.login(formData)
      localStorage.setItem('token', response.data.access_token)
      saveAccountToHistory(formData.email)
      const userResponse = await authAPI.getCurrentUser()
      setUser(userResponse.data)
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Invalid email or password. Please try again.')
      } else if (err.response?.status === 404) {
        setError('No account found with this email.')
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again.')
      } else {
        setError(err.response?.data?.detail || 'Login failed. Please check your credentials.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setFormData({ ...formData, [field]: value })
    if (fieldErrors[field]) {
      setFieldErrors({ ...fieldErrors, [field]: '' })
    }
    if (error) {
      setError('')
    }
  }

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="text-white">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-4 h-4 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-4 h-4 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent"></div>
      
      <main className="relative z-10 flex items-center justify-center flex-1 px-4 py-12">
        <div className="w-full max-w-md">
        <div className="p-8 border shadow-2xl bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
          <h2 className="mb-2 text-3xl font-bold text-center text-white">Welcome Back</h2>
          <p className="mb-8 text-center text-gray-400">Sign in to your account</p>

          {error && (
            <div className="p-3 mb-4 text-sm text-red-200 border rounded-lg bg-red-500/20 border-red-500/50">
              {error}
            </div>
          )}

          {accountHistory.length > 0 && (
            <div className="mb-6">
              <p className="mb-2 text-xs font-medium text-gray-400">Previously used accounts</p>
              <div className="space-y-2">
                {accountHistory.map((email, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => handleAccountClick(email)}
                    className="flex items-center w-full gap-3 px-3 py-2 text-sm text-left transition-all border rounded-lg bg-white/5 border-white/10 hover:bg-white/10 hover:border-purple-500/50"
                  >
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-purple-500/20">
                      <span className="text-sm font-semibold text-purple-300">
                        {email.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <span className="text-gray-300 truncate">{email}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block mb-2 text-sm font-medium text-gray-300">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                className={`w-full px-4 py-3 text-white placeholder-gray-500 border bg-white/5 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  fieldErrors.email ? 'border-red-500/50' : 'border-white/10'
                }`}
                placeholder="you@example.com"
              />
              {fieldErrors.email && (
                <p className="mt-1 text-xs text-red-300">{fieldErrors.email}</p>
              )}
            </div>

            <div>
              <label className="block mb-2 text-sm font-medium text-gray-300">Password</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                className={`w-full px-4 py-3 text-white placeholder-gray-500 border bg-white/5 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  fieldErrors.password ? 'border-red-500/50' : 'border-white/10'
                }`}
                placeholder="••••••••"
              />
              {fieldErrors.password && (
                <p className="mt-1 text-xs text-red-300">{fieldErrors.password}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 font-semibold text-white transition-all duration-300 shadow-lg bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl hover:from-purple-700 hover:to-pink-700 shadow-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="mt-6 text-sm text-center text-gray-400">
            Don't have an account?{' '}
            <Link to="/register" className="font-medium text-purple-400 hover:text-purple-300">
              Sign up
            </Link>
          </p>
        </div>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}

export default Login
