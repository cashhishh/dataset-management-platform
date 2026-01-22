import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

function ProtectedRoute({ children }) {
  const { user, authLoading } = useAuth()

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

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute
