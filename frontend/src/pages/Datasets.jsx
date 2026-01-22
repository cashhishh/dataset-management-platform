import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { datasetAPI } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import Footer from '../components/Footer'

function Datasets() {
  const navigate = useNavigate()
  const { logout } = useAuth()
  const [datasets, setDatasets] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [showUpload, setShowUpload] = useState(false)
  const [uploadData, setUploadData] = useState({
    name: '',
    description: '',
    file: null
  })
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState(null)
  const [uploadSuccess, setUploadSuccess] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  const fetchDatasets = async () => {
    try {
      setError(null)
      const response = await datasetAPI.getAll()
      setDatasets(response.data || [])
    } catch (err) {
      console.error('Failed to fetch datasets:', err)
      if (err.response?.status === 403) {
        setError('Access denied. You do not have permission to view datasets.')
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again later.')
      } else {
        setError('Failed to load datasets.')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDatasets()
  }, [])

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file && file.type === 'text/csv') {
      setUploadData({ ...uploadData, file })
    } else {
      alert('Please select a CSV file')
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type === 'text/csv') {
        setUploadData({ ...uploadData, file })
      } else {
        alert('Please select a CSV file')
      }
    }
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!uploadData.file) {
      setError('Please select a file')
      return
    }

    if (!uploadData.name.trim()) {
      setError('Please enter a dataset name')
      return
    }

    setUploading(true)
    setError(null)
    setUploadSuccess(false)
    
    try {
      const formData = new FormData()
      formData.append('file', uploadData.file)
      formData.append('name', uploadData.name)
      formData.append('description', uploadData.description || '')

      await datasetAPI.upload(formData)
      
      setUploadData({ name: '', description: '', file: null })
      setUploadSuccess(true)
      
      setTimeout(() => {
        setShowUpload(false)
        setUploadSuccess(false)
        fetchDatasets()
      }, 1500)
    } catch (err) {
      console.error('Failed to upload dataset:', err)
      if (err.response?.status === 400) {
        setError(err.response?.data?.detail || 'Invalid file or data. Please check and try again.')
      } else if (err.response?.status === 403) {
        setError('Access denied. You do not have permission to upload datasets.')
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again later.')
      } else {
        setError(err.response?.data?.detail || 'Failed to upload dataset. Please try again.')
      }
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      try {
        setError(null)
        await datasetAPI.delete(id)
        fetchDatasets()
      } catch (err) {
        console.error('Failed to delete dataset:', err)
        if (err.response?.status === 403) {
          setError('Access denied. You can only delete your own datasets.')
        } else if (err.response?.status === 404) {
          setError('Dataset not found.')
        } else {
          setError('Failed to delete dataset.')
        }
      }
    }
  }

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
                onClick={() => navigate('/dashboard')}
                className="px-3 py-2 text-sm text-gray-300 transition-colors sm:px-4 hover:text-white"
              >
                Dashboard
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
                  navigate('/dashboard')
                  setMenuOpen(false)
                }}
                className="block w-full px-4 py-2 text-left text-gray-300 transition-colors rounded-lg hover:text-white hover:bg-white/5"
              >
                Dashboard
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
        <div className="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center sm:mb-8">
          <h2 className="text-2xl font-bold text-white sm:text-3xl">Your Datasets</h2>
          <button
            onClick={() => setShowUpload(!showUpload)}
            className="w-full px-4 py-2 text-sm font-semibold text-white transition-all duration-300 shadow-lg sm:w-auto sm:px-6 sm:py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl hover:from-purple-700 hover:to-pink-700 shadow-purple-500/50"
          >
            {showUpload ? 'Cancel' : '📤 Upload CSV'}
          </button>
        </div>

        {error && (
          <div className="p-4 mb-6 border bg-red-500/20 border-red-500/50 rounded-xl">
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}

        {uploadSuccess && (
          <div className="p-4 mb-6 border bg-green-500/20 border-green-500/50 rounded-xl">
            <p className="text-sm text-green-300">✅ Dataset uploaded successfully!</p>
          </div>
        )}

        {showUpload && (
          <div className="p-6 mb-8 border bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <h3 className="mb-4 text-xl font-semibold text-white">Upload Dataset</h3>
            <form onSubmit={handleUpload} className="space-y-4">
              <div>
                <label className="block mb-2 text-sm font-medium text-gray-300">Dataset Name</label>
                <input
                  type="text"
                  value={uploadData.name}
                  onChange={(e) => setUploadData({ ...uploadData, name: e.target.value })}
                  className="w-full px-4 py-3 text-white placeholder-gray-500 border bg-white/5 border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="My Dataset"
                  required
                />
              </div>
              <div>
                <label className="block mb-2 text-sm font-medium text-gray-300">Description</label>
                <textarea
                  value={uploadData.description}
                  onChange={(e) => setUploadData({ ...uploadData, description: e.target.value })}
                  className="w-full px-4 py-3 text-white placeholder-gray-500 border bg-white/5 border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Dataset description"
                  rows="3"
                />
              </div>
              <div>
                <label className="block mb-2 text-sm font-medium text-gray-300">CSV File</label>
                <div
                  className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all ${
                    dragActive
                      ? 'border-purple-500 bg-purple-500/10'
                      : 'border-white/20 bg-white/5'
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <div className="mb-2 text-4xl">📊</div>
                  {uploadData.file ? (
                    <div className="space-y-1">
                      <p className="font-medium text-white">{uploadData.file.name}</p>
                      <p className="text-sm text-gray-400">
                        {(uploadData.file.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                  ) : (
                    <>
                      <p className="mb-1 text-gray-300">Drag & drop your CSV file here</p>
                      <p className="text-sm text-gray-500">or click to browse</p>
                    </>
                  )}
                </div>
              </div>
              <button
                type="submit"
                disabled={uploading || !uploadData.file || !uploadData.name.trim()}
                className="w-full py-3 font-semibold text-white transition-colors bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-xl"
              >
                {uploading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="inline-block w-4 h-4 border-2 border-white rounded-full border-t-transparent animate-spin"></span>
                    Uploading & Analyzing...
                  </span>
                ) : uploadSuccess ? (
                  '✅ Upload Complete!'
                ) : (
                  'Upload & Analyze'
                )}
              </button>
            </form>
          </div>
        )}

        {loading ? (
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="p-6 border bg-white/10 backdrop-blur-md rounded-2xl border-white/20 animate-pulse">
                <div className="w-3/4 h-6 mb-3 rounded bg-white/20"></div>
                <div className="w-full h-4 mb-2 rounded bg-white/10"></div>
                <div className="w-2/3 h-4 mb-4 rounded bg-white/10"></div>
                <div className="w-1/2 h-4 rounded bg-white/10"></div>
              </div>
            ))}
          </div>
        ) : datasets.length === 0 ? (
          <div className="p-12 text-center border bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <div className="mb-4 text-6xl">📊</div>
            <h3 className="mb-2 text-xl font-semibold text-white">No datasets yet</h3>
            <p className="text-gray-400">Create your first dataset to get started</p>
          </div>
        ) : Array.isArray(datasets) && datasets.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {datasets.map((dataset) => (
              <div
                key={dataset.id}
                className="p-6 transition-all border cursor-pointer bg-white/10 backdrop-blur-md rounded-2xl border-white/20 hover:bg-white/15"
                onClick={() => navigate(`/datasets/${dataset.id}`)}
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-semibold text-white">{dataset.name}</h3>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDelete(dataset.id)
                    }}
                    className="text-sm text-red-400 hover:text-red-300"
                  >
                    Delete
                  </button>
                </div>
                <p className="mb-4 text-sm text-gray-400">{dataset.description || 'No description'}</p>
                
                {dataset.file_name && (
                  <div className="mb-3 space-y-2">
                    <div className="flex items-center gap-2 text-xs text-gray-400">
                      <span>📁</span>
                      <span className="truncate">{dataset.file_name}</span>
                    </div>
                    {(dataset.row_count !== null && dataset.row_count !== undefined) && (
                      <div className="flex gap-4 text-xs text-gray-400">
                        <span>📊 {dataset.row_count?.toLocaleString()} rows</span>
                        <span>📈 {dataset.column_count || 0} columns</span>
                      </div>
                    )}
                    {dataset.file_size && (
                      <div className="text-xs text-gray-500">
                        {(dataset.file_size / 1024).toFixed(1)} KB
                      </div>
                    )}
                  </div>
                )}
                
                <p className="mt-2 text-xs text-gray-500">
                  Created: {new Date(dataset.created_at).toLocaleDateString()}
                </p>
                {dataset.owner_username && (
                  <p className="mt-1 text-xs text-purple-400">
                    Owner: {dataset.owner_username}
                  </p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="p-12 text-center border bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <div className="mb-4 text-6xl">⚠️</div>
            <h3 className="mb-2 text-xl font-semibold text-white">No datasets found</h3>
            <p className="text-gray-400">Try refreshing the page or uploading a new dataset</p>
          </div>
        )}
      </main>
      
      <Footer />
    </div>
  )
}

export default Datasets
