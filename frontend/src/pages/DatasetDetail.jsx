import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { datasetAPI } from '../services/api'
import Footer from '../components/Footer'
import AdvancedQualityReport from '../components/AdvancedQualityReport'
import DataProfiling from '../components/DataProfiling'
import DatasetVersions from '../components/DatasetVersions'
import QualityRules from '../components/QualityRules'

function DatasetDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [dataset, setDataset] = useState(null)
  const [columns, setColumns] = useState([])
  const [qualityReport, setQualityReport] = useState(null)
  const [preview, setPreview] = useState({ columns: [], rows: [], total_rows: 0 })
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    fetchDatasetDetail()
  }, [id])

  const fetchDatasetDetail = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const [detailRes, previewRes] = await Promise.all([
        datasetAPI.getDetail(id),
        datasetAPI.getPreview(id, 10)
      ])
      
      setDataset(detailRes.data?.dataset || null)
      setColumns(detailRes.data?.columns || [])
      setQualityReport(detailRes.data?.quality_report || null)
      setPreview(previewRes.data || { columns: [], rows: [], total_rows: 0 })
    } catch (err) {
      console.error('Failed to fetch dataset details:', err)
      if (err.response?.status === 404) {
        setError('Dataset not found')
      } else if (err.response?.status === 403) {
        setError('Access denied. You do not have permission to view this dataset.')
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again later.')
      } else {
        setError('Failed to load dataset details')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      try {
        await datasetAPI.delete(id)
        navigate('/datasets')
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

  if (loading) {
    return (
      <div className="flex items-center justify-center w-full min-h-screen overflow-x-hidden bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="text-center">
          <div className="inline-block w-16 h-16 mb-4 border-4 border-purple-500 rounded-full border-t-transparent animate-spin"></div>
          <div className="text-xl text-white">Loading dataset...</div>
        </div>
      </div>
    )
  }

  if (error || !dataset) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="max-w-md p-8 text-center border bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
          <div className="mb-4 text-6xl">⚠️</div>
          <h2 className="mb-2 text-2xl font-bold text-white">{error || 'Dataset not found'}</h2>
          <p className="mb-6 text-gray-400">The dataset you're looking for doesn't exist or you don't have access to it.</p>
          <button
            onClick={() => navigate('/datasets')}
            className="px-6 py-3 font-semibold text-white transition-colors bg-purple-600 hover:bg-purple-700 rounded-xl"
          >
            Back to Datasets
          </button>
        </div>
      </div>
    )
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'preview', label: 'Data Preview', icon: '👁️' },
    { id: 'quality', label: 'Quality Report', icon: '✅' },
    { id: 'advanced-quality', label: 'Advanced Quality', icon: '🔬' },
    { id: 'profiling', label: 'Data Profiling', icon: '📈' },
    { id: 'schema', label: 'Schema', icon: '📋' },
    { id: 'versions', label: 'Versions', icon: '🔄' },
    { id: 'rules', label: 'Quality Rules', icon: '📏' }
  ]

  return (
    <div className="flex flex-col min-h-screen overflow-x-hidden bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent"></div>
      
      <nav className="relative z-10 border-b bg-white/5 backdrop-blur-md border-white/10">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2 sm:gap-4">
              <button
                onClick={() => navigate('/datasets')}
                className="text-gray-300 transition-colors hover:text-white"
              >
                ← <span className="hidden sm:inline">Back</span>
              </button>
              <h1 className="text-base font-bold text-white truncate sm:text-xl max-w-[200px] sm:max-w-none">{dataset?.name || 'Dataset'}</h1>
            </div>
            
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-gray-300 sm:hidden hover:text-white focus:outline-none"
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={menuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
              </svg>
            </button>

            <button
              onClick={handleDelete}
              className="hidden px-3 py-2 text-sm text-red-400 transition-all rounded-lg sm:block sm:px-4 bg-red-600/20 hover:bg-red-600/30"
            >
              Delete Dataset
            </button>
          </div>

          {menuOpen && (
            <div className="py-4 sm:hidden">
              <button
                onClick={handleDelete}
                className="block w-full px-4 py-2 text-left text-red-400 transition-all rounded-lg bg-red-600/20 hover:bg-red-600/30"
              >
                Delete Dataset
              </button>
            </div>
          )}
        </div>
      </nav>

      <main className="relative z-10 flex-1 px-4 py-8 mx-auto overflow-x-hidden max-w-7xl sm:px-6 lg:px-8 sm:py-12">
        {/* Mobile dropdown */}
        <div className="mb-6 sm:hidden">
          <label htmlFor="tab-select" className="block mb-2 text-sm font-medium text-gray-300">
            Select View
          </label>
          <div className="relative">
            <select
              id="tab-select"
              value={activeTab}
              onChange={(e) => setActiveTab(e.target.value)}
              className="w-full px-4 py-3 pr-10 text-white transition-all border appearance-none bg-white/10 backdrop-blur-md border-white/20 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              {tabs.map((tab) => (
                <option key={tab.id} value={tab.id} className="bg-gray-800">
                  {tab.icon} {tab.label}
                </option>
              ))}
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>

        {/* Desktop tabs - Horizontal scrollable on small/medium screens */}
        <div className="hidden mb-8 -mx-4 sm:block sm:mx-0">
          <div className="flex gap-2 px-4 overflow-x-auto sm:px-0 scrollbar-hide">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 rounded-xl font-medium transition-all whitespace-nowrap flex-shrink-0 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg shadow-purple-500/50'
                    : 'bg-white/10 text-gray-300 hover:bg-white/15'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                <span className="hidden md:inline">{tab.label}</span>
                <span className="md:hidden">{tab.icon}</span>
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'overview' && (
          <div className="w-full space-y-6">
            <div className="w-full p-4 border sm:p-6 bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
              <h2 className="mb-4 text-2xl font-bold text-white">Dataset Information</h2>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                  <p className="text-sm text-gray-400">Name</p>
                  <p className="font-medium text-white">{dataset?.name || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Created</p>
                  <p className="font-medium text-white">
                    {dataset?.created_at ? new Date(dataset.created_at).toLocaleString() : 'N/A'}
                  </p>
                </div>
                <div className="md:col-span-2">
                  <p className="text-sm text-gray-400">Description</p>
                  <p className="font-medium text-white">{dataset?.description || 'No description'}</p>
                </div>
                {dataset?.file_name && (
                  <>
                    <div>
                      <p className="text-sm text-gray-400">Filename</p>
                      <p className="font-medium text-white">{dataset.file_name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">File Size</p>
                      <p className="font-medium text-white">
                        {dataset.file_size ? `${(dataset.file_size / 1024).toFixed(2)} KB` : 'N/A'}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Total Rows</p>
                      <p className="text-2xl font-medium text-white">
                        {dataset.row_count !== null && dataset.row_count !== undefined 
                          ? dataset.row_count.toLocaleString() 
                          : '0'}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Total Columns</p>
                      <p className="text-2xl font-medium text-white">{dataset.column_count || 0}</p>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'preview' && (
          <div className="w-full p-4 border sm:p-6 bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <h2 className="mb-4 text-xl font-bold text-white sm:text-2xl sm:mb-6">Data Preview</h2>
            {preview?.rows && Array.isArray(preview.rows) && preview.rows.length > 0 ? (
              <div className="w-full overflow-x-auto -mx-4 sm:mx-0 sm:rounded-lg">
                <div className="inline-block min-w-full align-middle">
                  <table className="min-w-full text-xs sm:text-sm">
                    <thead>
                      <tr className="border-b border-white/20">
                        {preview.columns?.map((col, idx) => (
                          <th key={idx} className="px-3 py-3 font-semibold text-left text-gray-300 whitespace-nowrap sm:px-4">
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {preview.rows.map((row, rowIdx) => (
                        <tr key={rowIdx} className="transition-colors border-b border-white/10 hover:bg-white/5">
                          {preview.columns?.map((col, colIdx) => (
                            <td key={colIdx} className="px-3 py-3 text-white whitespace-nowrap sm:px-4">
                              {row[col] !== null && row[col] !== undefined 
                                ? String(row[col]) 
                                : <span className="italic text-gray-500">null</span>
                              }
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <div className="py-12 text-center">
                <div className="mb-4 text-6xl">📋</div>
                <p className="text-gray-400">No preview data available</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'quality' && (
          <div className="w-full space-y-4 overflow-x-hidden sm:space-y-6">
            {qualityReport ? (
              <div className="w-full p-3 border sm:p-5 lg:p-6 bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
                <h2 className="mb-4 text-lg font-bold text-white sm:text-xl lg:text-2xl sm:mb-5 lg:mb-6">Data Quality Report</h2>
                
                <div className="grid grid-cols-1 gap-3 mb-5 sm:gap-4 sm:mb-6 sm:grid-cols-2 lg:gap-6 lg:mb-8">
                  <div className="p-3 sm:p-4 lg:p-5 rounded-xl bg-white/5">
                    <p className="mb-2 text-xs text-gray-400 sm:text-sm lg:mb-3">Overall Completeness</p>
                    <div className="space-y-2">
                      <p className="text-2xl font-bold text-white sm:text-3xl lg:text-4xl">
                        {qualityReport.completeness_score?.toFixed(1) || 0}%
                      </p>
                      <div className="w-full h-2 overflow-hidden bg-gray-700 rounded-full sm:h-3 lg:h-4">
                        <div 
                          className="h-full transition-all duration-500 bg-gradient-to-r from-green-500 to-emerald-500"
                          style={{ width: `${qualityReport.completeness_score || 0}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                  <div className="p-3 sm:p-4 lg:p-5 rounded-xl bg-white/5">
                    <p className="mb-2 text-xs text-gray-400 sm:text-sm lg:mb-3">Duplicate Rows</p>
                    <p className="text-2xl font-bold text-white sm:text-3xl lg:text-4xl">{qualityReport.duplicate_rows || 0}</p>
                    <p className="mt-1 text-xs text-gray-500 sm:text-sm">
                      {qualityReport.total_rows && qualityReport.total_rows > 0
                        ? ((qualityReport.duplicate_rows / qualityReport.total_rows) * 100).toFixed(2)
                        : 0}% of total
                    </p>
                  </div>
                </div>

                <h3 className="mb-3 text-base font-semibold text-white sm:text-lg lg:text-xl sm:mb-4">Null Values by Column</h3>
                {qualityReport.null_counts && typeof qualityReport.null_counts === 'object' && Object.keys(qualityReport.null_counts).length > 0 ? (
                  <div className="space-y-2 sm:space-y-3">
                    {Object.entries(qualityReport.null_counts).map(([column, count]) => (
                      <div key={column} className="p-3 rounded-lg sm:p-4 bg-white/5">
                        <div className="flex flex-col gap-1 mb-2 sm:flex-row sm:items-center sm:justify-between sm:gap-3">
                          <span className="text-xs font-medium text-white break-words sm:text-sm lg:text-base sm:flex-1 sm:min-w-0">
                            {column}
                          </span>
                          <span className="text-xs text-gray-400 sm:text-sm sm:flex-shrink-0 sm:whitespace-nowrap">
                            {count} null{count !== 1 ? 's' : ''}
                          </span>
                        </div>
                        <div className="w-full h-2 overflow-hidden bg-gray-700 rounded-full">
                          <div 
                            className="h-full transition-all duration-500 bg-gradient-to-r from-red-500 to-orange-500"
                            style={{ 
                              width: `${qualityReport.total_rows && qualityReport.total_rows > 0
                                ? Math.min((count / qualityReport.total_rows) * 100, 100)
                                : 0}%` 
                            }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="py-6 text-center sm:py-8">
                    <p className="text-sm text-gray-400 sm:text-base">No null value data available</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-8 text-center border sm:p-10 lg:p-12 bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
                <div className="mb-3 text-5xl sm:mb-4 sm:text-6xl">✅</div>
                <h3 className="mb-2 text-lg font-semibold text-white sm:text-xl">No Quality Report</h3>
                <p className="text-sm text-gray-400 sm:text-base">Quality analysis not available for this dataset</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'advanced-quality' && (
          <div className="w-full">
            <AdvancedQualityReport datasetId={id} />
          </div>
        )}

        {activeTab === 'profiling' && (
          <div className="w-full">
            <DataProfiling datasetId={id} />
          </div>
        )}

        {activeTab === 'schema' && (
          <div className="w-full p-4 border sm:p-6 bg-white/10 backdrop-blur-md rounded-2xl border-white/20">
            <h2 className="mb-4 text-xl font-bold text-white sm:text-2xl sm:mb-6">Dataset Schema</h2>
            {columns && Array.isArray(columns) && columns.length > 0 ? (
              <div className="space-y-3">
                {columns.map((col) => (
                  <div key={col?.id || col?.column_index} className="flex flex-col items-start justify-between gap-2 p-3 rounded-lg sm:flex-row sm:items-center sm:p-4 bg-white/5">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white truncate sm:text-base">{col?.column_name || 'Unknown'}</p>
                      <p className="text-xs text-gray-400 sm:text-sm">
                        Position: {col?.column_index !== null && col?.column_index !== undefined 
                          ? col.column_index + 1 
                          : 'N/A'}
                      </p>
                    </div>
                    <div className="px-3 py-2 rounded-lg sm:px-4 bg-purple-600/30">
                      <p className="font-mono text-xs text-purple-300 sm:text-sm">{col?.column_type || 'unknown'}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-12 text-center">
                <div className="mb-4 text-6xl">📋</div>
                <p className="text-gray-400">No schema information available</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'versions' && (
          <div className="w-full">
            <DatasetVersions />
          </div>
        )}

        {activeTab === 'rules' && (
          <div className="w-full">
            <QualityRules />
          </div>
        )}
      </main>
      
      <Footer />
    </div>
  )
}

export default DatasetDetail
