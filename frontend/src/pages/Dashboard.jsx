import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { authAPI } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import Footer from '../components/Footer'

function Dashboard() {
  const navigate = useNavigate()
  const { logout } = useAuth()
  const [user, setUser] = useState(null)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    authAPI.getCurrentUser()
      .then(res => setUser(res.data))
      .catch(() => {
        localStorage.removeItem('token')
        navigate('/login')
      })
  }, [navigate])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent"></div>
      
      <nav className="relative z-10 border-b bg-white/5 backdrop-blur-md border-white/10">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <h1 className="text-lg font-bold text-white sm:text-xl">Dataset Platform</h1>
            
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-gray-300 sm:hidden hover:text-white focus:outline-none"
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={menuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
              </svg>
            </button>

            <div className="hidden gap-3 sm:flex sm:gap-4">
              <button
                onClick={() => navigate('/datasets')}
                className="px-3 py-2 text-sm text-gray-300 transition-colors sm:px-4 hover:text-white"
              >
                Datasets
              </button>
              <button
                onClick={handleLogout}
                className="px-3 py-2 text-sm text-white transition-all rounded-lg sm:px-4 bg-white/10 hover:bg-white/20"
              >
                Logout
              </button>
            </div>
          </div>

          {menuOpen && (
            <div className="py-4 space-y-2 sm:hidden">
              <button
                onClick={() => {
                  navigate('/datasets')
                  setMenuOpen(false)
                }}
                className="block w-full px-4 py-2 text-left text-gray-300 transition-colors rounded-lg hover:text-white hover:bg-white/5"
              >
                Datasets
              </button>
              <button
                onClick={handleLogout}
                className="block w-full px-4 py-2 text-left text-white transition-all rounded-lg bg-white/10 hover:bg-white/20"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>

      <main className="relative z-10 flex-1 px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8 sm:py-12">
        <div className="p-6 mb-6 border sm:p-8 sm:mb-8 bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
          <h2 className="mb-4 text-2xl font-bold text-white sm:text-3xl">Welcome to Dashboard</h2>
          {user && (
            <div className="space-y-2">
              <p className="text-sm text-gray-300 sm:text-base">
                <span className="font-semibold">Email:</span> {user.email}
              </p>
              <p className="text-sm text-gray-300 sm:text-base">
                <span className="font-semibold">Username:</span> {user.username}
              </p>
              <p className="text-sm text-gray-300 sm:text-base">
                <span className="font-semibold">Role:</span> 
                <span className={`ml-2 px-3 py-1 rounded-full text-xs sm:text-sm ${
                  user.role === 'admin' 
                    ? 'bg-purple-500/20 text-purple-300' 
                    : 'bg-blue-500/20 text-blue-300'
                }`}>
                  {user.role}
                </span>
              </p>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-3">
          <div className="p-6 border bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <div className="mb-4 text-4xl">📊</div>
            <h3 className="mb-2 text-lg font-semibold text-white sm:text-xl">Your Datasets</h3>
            <p className="mb-4 text-sm text-gray-400">Manage and view your datasets</p>
            <button
              onClick={() => navigate('/datasets')}
              className="w-full px-4 py-2 text-sm text-white transition-colors bg-purple-600 rounded-lg sm:w-auto hover:bg-purple-700"
            >
              View Datasets
            </button>
          </div>

          <div className="p-6 border bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <div className="mb-4 text-4xl">🔒</div>
            <h3 className="mb-2 text-lg font-semibold text-white sm:text-xl">Secure Access</h3>
            <p className="text-sm text-gray-400">JWT-based authentication protecting your data</p>
          </div>

          <div className="p-6 border bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <div className="mb-4 text-4xl">⚡</div>
            <h3 className="mb-2 text-lg font-semibold text-white sm:text-xl">Fast & Reliable</h3>
            <p className="text-sm text-gray-400">Built with FastAPI and React for optimal performance</p>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}

export default Dashboard
