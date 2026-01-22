import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authAPI } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import Footer from '../components/Footer'

const ACCOUNT_HISTORY_KEY = 'account_history'

function Register() {
  const navigate = useNavigate()
  const { user, authLoading, setUser } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    role: 'user'
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})

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

  const validateForm = () => {
    const errors = {}
    if (!formData.email.trim()) {
      errors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Please enter a valid email address'
    }
    if (!formData.username.trim()) {
      errors.username = 'Username is required'
    } else if (formData.username.length < 3) {
      errors.username = 'Username must be at least 3 characters'
    }
    if (!formData.password) {
      errors.password = 'Password is required'
    } else if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters'
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
      await authAPI.register(formData)
      const loginResponse = await authAPI.login({
        email: formData.email,
        password: formData.password
      })
      localStorage.setItem('token', loginResponse.data.access_token)
      saveAccountToHistory(formData.email)
      const userResponse = await authAPI.getCurrentUser()
      setUser(userResponse.data)
    } catch (err) {
      if (err.response?.status === 400) {
        const detail = err.response?.data?.detail
        if (detail?.includes('email')) {
          setError('This email is already registered. Please use a different email or sign in.')
        } else if (detail?.includes('username')) {
          setError('This username is already taken. Please choose a different username.')
        } else {
          setError(detail || 'Invalid registration data. Please check your information.')
        }
      } else if (err.response?.status === 422) {
        setError('Please check your information and try again.')
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again later.')
      } else {
        setError(err.response?.data?.detail || 'Registration failed. Please try again.')
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
          <h2 className="mb-2 text-3xl font-bold text-center text-white">Create Account</h2>
          <p className="mb-8 text-center text-gray-400">Get started with your account</p>

          {error && (
            <div className="p-3 mb-4 text-sm text-red-200 border rounded-lg bg-red-500/20 border-red-500/50">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block mb-2 text-sm font-medium text-gray-300">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                className={`w-full px-4 py-3 text-white placeholder-gray-500 border ${
                  fieldErrors.email ? 'border-red-500' : 'border-white/10'
                } bg-white/5 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent`}
                placeholder="you@example.com"
              />
              {fieldErrors.email && (
                <p className="mt-1 text-sm text-red-400">{fieldErrors.email}</p>
              )}
            </div>

            <div>
              <label className="block mb-2 text-sm font-medium text-gray-300">Username</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => handleInputChange('username', e.target.value)}
                className={`w-full px-4 py-3 text-white placeholder-gray-500 border ${
                  fieldErrors.username ? 'border-red-500' : 'border-white/10'
                } bg-white/5 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent`}
                placeholder="johndoe"
              />
              {fieldErrors.username && (
                <p className="mt-1 text-sm text-red-400">{fieldErrors.username}</p>
              )}
            </div>

            <div>
              <label className="block mb-2 text-sm font-medium text-gray-300">Password</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                className={`w-full px-4 py-3 text-white placeholder-gray-500 border ${
                  fieldErrors.password ? 'border-red-500' : 'border-white/10'
                } bg-white/5 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent`}
                placeholder="••••••••"
              />
              {fieldErrors.password && (
                <p className="mt-1 text-sm text-red-400">{fieldErrors.password}</p>
              )}
              {formData.password && formData.password.length > 0 && !fieldErrors.password && (
                <p className={`mt-1 text-sm ${formData.password.length >= 6 ? 'text-green-400' : 'text-yellow-400'}`}>
                  {formData.password.length >= 6 ? '✓ Password is strong enough' : `${formData.password.length}/6 characters`}
                </p>
              )}
            </div>

            <div>
              <label className="block mb-2 text-sm font-medium text-gray-300">Role</label>
              <select
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                className="w-full px-4 py-3 text-white border bg-white/5 border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="user" className="bg-gray-800">User</option>
                <option value="admin" className="bg-gray-800">Admin</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 font-semibold text-white transition-all duration-300 shadow-lg bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl hover:from-purple-700 hover:to-pink-700 shadow-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating account...' : 'Sign Up'}
            </button>
          </form>

          <p className="mt-6 text-sm text-center text-gray-400">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-purple-400 hover:text-purple-300">
              Sign in
            </Link>
          </p>
        </div>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}

export default Register
