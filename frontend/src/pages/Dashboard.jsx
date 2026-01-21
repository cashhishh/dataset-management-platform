import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { authAPI } from '../services/api'

function Dashboard() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)

  useEffect(() => {
    authAPI.getCurrentUser()
      .then(res => setUser(res.data))
      .catch(() => {
        localStorage.removeItem('token')
        navigate('/login')
      })
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent"></div>
      
      <nav className="relative z-10 bg-white/5 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold text-white">Dataset Platform</h1>
            <div className="flex gap-4">
              <button
                onClick={() => navigate('/datasets')}
                className="px-4 py-2 text-gray-300 hover:text-white transition-colors"
              >
                Datasets
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 p-8 mb-8">
          <h2 className="text-3xl font-bold text-white mb-4">Welcome to Dashboard</h2>
          {user && (
            <div className="space-y-2">
              <p className="text-gray-300">
                <span className="font-semibold">Email:</span> {user.email}
              </p>
              <p className="text-gray-300">
                <span className="font-semibold">Username:</span> {user.username}
              </p>
              <p className="text-gray-300">
                <span className="font-semibold">Role:</span> 
                <span className={`ml-2 px-3 py-1 rounded-full text-sm ${
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

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 p-6">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold text-white mb-2">Your Datasets</h3>
            <p className="text-gray-400 mb-4">Manage and view your datasets</p>
            <button
              onClick={() => navigate('/datasets')}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
            >
              View Datasets
            </button>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 p-6">
            <div className="text-4xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold text-white mb-2">Secure Access</h3>
            <p className="text-gray-400">JWT-based authentication protecting your data</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 p-6">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold text-white mb-2">Fast & Reliable</h3>
            <p className="text-gray-400">Built with FastAPI and React for optimal performance</p>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
