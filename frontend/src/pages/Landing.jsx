import { useNavigate } from 'react-router-dom'

function Landing() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen  bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center px-4">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent"></div>
      
      <div className="relative z-10 max-w-4xl mx-auto text-center">
        <div className="mb-8">
          <h1 className="text-6xl md:text-5xl font-bold text-white mb-6 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            Dataset Management Platform
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto">
            Securely store, manage, and collaborate on your datasets with enterprise-grade authentication and role-based access control.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/register')}
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all duration-300 shadow-lg shadow-purple-500/50 hover:shadow-purple-500/75"
          >
            Get Started
          </button>
          <button
            onClick={() => navigate('/login')}
            className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl border border-white/20 hover:bg-white/20 transition-all duration-300"
          >
            Sign In
          </button>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 bg-white/5 backdrop-blur-md rounded-2xl border border-white/10">
            <div className="text-purple-400 text-4xl mb-4">🔒</div>
            <h3 className="text-white font-semibold mb-2">Secure Authentication</h3>
            <p className="text-gray-400 text-sm">JWT-based authentication with bcrypt password hashing</p>
          </div>
          <div className="p-6 bg-white/5 backdrop-blur-md rounded-2xl border border-white/10">
            <div className="text-purple-400 text-4xl mb-4">👥</div>
            <h3 className="text-white font-semibold mb-2">Role-Based Access</h3>
            <p className="text-gray-400 text-sm">User and admin roles with granular permissions</p>
          </div>
          <div className="p-6 bg-white/5 backdrop-blur-md rounded-2xl border border-white/10">
            <div className="text-purple-400 text-4xl mb-4">📊</div>
            <h3 className="text-white font-semibold mb-2">Dataset Management</h3>
            <p className="text-gray-400 text-sm">Create, view, and manage your datasets effortlessly</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Landing
