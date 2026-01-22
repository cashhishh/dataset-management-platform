import { useNavigate } from 'react-router-dom'
import Footer from '../components/Footer'

function Landing() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent"></div>
      
      <main className="relative z-10 flex items-center justify-center flex-1 px-4 py-12">
        <div className="w-full max-w-4xl mx-auto text-center">
          <div className="mb-8">
            <h1 className="mb-6 text-4xl font-bold text-white sm:text-5xl lg:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
              Dataset Management Platform
            </h1>
            <p className="max-w-2xl mx-auto mb-12 text-lg text-gray-300 sm:text-xl lg:text-2xl">
              Securely store, manage, and collaborate on your datasets with enterprise-grade authentication and role-based access control.
            </p>
          </div>

          <div className="flex flex-col gap-4 justify-center sm:flex-row">
            <button
              onClick={() => navigate('/register')}
              className="px-6 py-3 sm:px-8 sm:py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all duration-300 shadow-lg shadow-purple-500/50 hover:shadow-purple-500/75"
            >
              Get Started
            </button>
            <button
              onClick={() => navigate('/login')}
              className="px-6 py-3 sm:px-8 sm:py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              Sign In
            </button>
          </div>

          <div className="grid grid-cols-1 gap-6 mt-12 sm:mt-16 sm:grid-cols-3">
            <div className="p-6 border bg-white/5 backdrop-blur-md rounded-2xl border-white/10">
              <div className="mb-4 text-4xl text-purple-400">🔒</div>
              <h3 className="mb-2 font-semibold text-white">Secure Authentication</h3>
              <p className="text-sm text-gray-400">JWT-based authentication with bcrypt password hashing</p>
            </div>
            <div className="p-6 border bg-white/5 backdrop-blur-md rounded-2xl border-white/10">
              <div className="mb-4 text-4xl text-purple-400">👥</div>
              <h3 className="mb-2 font-semibold text-white">Role-Based Access</h3>
              <p className="text-sm text-gray-400">User and admin roles with granular permissions</p>
            </div>
            <div className="p-6 border bg-white/5 backdrop-blur-md rounded-2xl border-white/10">
              <div className="mb-4 text-4xl text-purple-400">📊</div>
              <h3 className="mb-2 font-semibold text-white">Dataset Management</h3>
              <p className="text-sm text-gray-400">Create, view, and manage your datasets effortlessly</p>
            </div>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}

export default Landing
