import { useState, useEffect } from 'react'
import { datasetAPI } from '../services/api'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'

const COLORS = ['#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#6366f1', '#84cc16']

export default function DataProfiling({ datasetId }) {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedColumn, setSelectedColumn] = useState(null)

  useEffect(() => {
    loadProfile()
  }, [datasetId])

  const loadProfile = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await datasetAPI.getProfile(datasetId)
      setProfile(response.data)
      
      // Auto-select first column with interesting data
      if (response.data?.column_profiles?.length > 0) {
        setSelectedColumn(response.data.column_profiles[0])
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load profiling data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    )
  }

  if (!profile || !profile.success) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">{profile?.error || 'Unable to generate profile'}</p>
      </div>
    )
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Dataset Overview */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="p-4 bg-white shadow rounded-xl">
          <p className="mb-1 text-xs text-gray-600 sm:text-sm">Total Rows</p>
          <p className="text-xl font-bold text-gray-900 sm:text-2xl">{profile.dataset_info.total_rows.toLocaleString()}</p>
        </div>
        <div className="p-4 bg-white shadow rounded-xl">
          <p className="mb-1 text-xs text-gray-600 sm:text-sm">Total Columns</p>
          <p className="text-xl font-bold text-gray-900 sm:text-2xl">{profile.dataset_info.total_columns}</p>
        </div>
        <div className="p-4 bg-white shadow rounded-xl">
          <p className="mb-1 text-xs text-gray-600 sm:text-sm">Missing Values</p>
          <p className="text-xl font-bold text-orange-600 sm:text-2xl">{profile.total_missing_values?.toLocaleString() || 0}</p>
        </div>
        <div className="p-4 bg-white shadow rounded-xl">
          <p className="mb-1 text-xs text-gray-600 sm:text-sm">Total Outliers</p>
          <p className="text-xl font-bold text-purple-600 sm:text-2xl">{profile.total_outliers?.toLocaleString() || 0}</p>
        </div>
      </div>

      {/* Missing Values Overview */}
      {profile.missing_summary && profile.missing_summary.length > 0 && (
        <div className="p-4 bg-white shadow sm:p-6 rounded-xl">
          <h3 className="mb-4 text-base font-semibold text-gray-900 sm:text-lg">Missing Values by Column</h3>
          <div className="w-full h-64 sm:h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={profile.missing_summary}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="column_name" angle={-45} textAnchor="end" height={100} fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="present_count" fill="#10b981" name="Present" stackId="a" />
                <Bar dataKey="total_missing" fill="#ef4444" name="Missing" stackId="a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Column Selector */}
      <div className="p-4 bg-white shadow sm:p-6 rounded-xl">
        <h3 className="mb-4 text-base font-semibold text-gray-900 sm:text-lg">Column Details</h3>
        <div className="mb-6">
          <label className="block mb-2 text-sm font-medium text-gray-700">Select Column</label>
          <select
            value={selectedColumn?.column_name || ''}
            onChange={(e) => {
              const col = profile.column_profiles.find(c => c.column_name === e.target.value)
              setSelectedColumn(col)
            }}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            {profile.column_profiles.map((col) => (
              <option key={col.column_name} value={col.column_name}>
                {col.column_name} ({col.is_numeric ? 'Numeric' : 'Categorical'})
              </option>
            ))}
          </select>
        </div>

        {selectedColumn && (
          <div className="space-y-4 sm:space-y-6">
            {/* Column Info */}
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <div>
                <p className="text-xs text-gray-600 sm:text-sm">Data Type</p>
                <p className="text-sm font-semibold text-gray-900 break-words sm:text-base">{selectedColumn.data_type}</p>
              </div>
              <div>
                <p className="text-xs text-gray-600 sm:text-sm">Total Values</p>
                <p className="text-sm font-semibold text-gray-900 sm:text-base">{selectedColumn.total_values.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-xs text-gray-600 sm:text-sm">Unique Values</p>
                <p className="text-sm font-semibold text-gray-900 sm:text-base">{selectedColumn.unique_count.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-xs text-gray-600 sm:text-sm">Null Count</p>
                <p className="text-sm font-semibold text-orange-600 sm:text-base">{selectedColumn.null_count.toLocaleString()}</p>
              </div>
            </div>

            {/* Numeric Column Visualization */}
            {selectedColumn.is_numeric && selectedColumn.histogram && selectedColumn.histogram.bins.length > 0 && (
              <div>
                <h4 className="mb-3 text-sm font-semibold text-gray-800 sm:text-base">Distribution</h4>
                
                {/* Statistics */}
                {selectedColumn.statistics && (
                  <div className="grid grid-cols-2 gap-4 p-4 mb-4 bg-gray-50 sm:grid-cols-5 rounded-xl">
                    <div>
                      <p className="text-xs text-gray-600">Min</p>
                      <p className="text-sm font-semibold text-gray-900 break-words">{selectedColumn.statistics.min}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Max</p>
                      <p className="text-sm font-semibold text-gray-900 break-words">{selectedColumn.statistics.max}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Mean</p>
                      <p className="text-sm font-semibold text-gray-900 break-words">{selectedColumn.statistics.mean}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Median</p>
                      <p className="text-sm font-semibold text-gray-900 break-words">{selectedColumn.statistics.median}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Std Dev</p>
                      <p className="text-sm font-semibold text-gray-900 break-words">{selectedColumn.statistics.std}</p>
                    </div>
                  </div>
                )}

                {/* Histogram */}
                <div className="w-full h-64 sm:h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={selectedColumn.histogram.bins}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="label" angle={-45} textAnchor="end" height={100} fontSize={12} />
                      <YAxis fontSize={12} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '12px' }} />
                      <Bar dataKey="count" fill="#8b5cf6" name="Frequency" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Outliers */}
                {selectedColumn.outliers && selectedColumn.outliers.has_outliers && (
                  <div className="p-4 mt-4 border border-purple-200 bg-purple-50 rounded-xl">
                    <h5 className="mb-2 text-sm font-semibold text-purple-900 sm:text-base">Outlier Detection</h5>
                    <div className="grid grid-cols-2 gap-4 text-xs sm:grid-cols-4 sm:text-sm">
                      <div>
                        <p className="text-purple-700">Outliers Found</p>
                        <p className="font-semibold text-purple-900">
                          {selectedColumn.outliers.outlier_count} ({selectedColumn.outliers.outlier_percentage}%)
                        </p>
                      </div>
                      <div>
                        <p className="text-purple-700">Lower Bound</p>
                        <p className="font-semibold text-purple-900 break-all">{selectedColumn.outliers.lower_bound}</p>
                      </div>
                      <div>
                        <p className="text-purple-700">Upper Bound</p>
                        <p className="font-semibold text-purple-900 break-all">{selectedColumn.outliers.upper_bound}</p>
                      </div>
                      <div>
                        <p className="text-purple-700">IQR</p>
                        <p className="font-semibold text-purple-900 break-all">{selectedColumn.outliers.iqr}</p>
                      </div>
                    </div>
                    {selectedColumn.outliers.outliers.length > 0 && (
                      <div className="mt-3">
                        <p className="mb-1 text-xs text-purple-700">Sample Outlier Values:</p>
                        <p className="text-xs font-mono text-purple-900 break-all sm:text-sm">
                          {selectedColumn.outliers.outliers.slice(0, 10).join(', ')}
                          {selectedColumn.outliers.outliers.length > 10 && '...'}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Categorical Column Visualization */}
            {!selectedColumn.is_numeric && selectedColumn.value_counts && selectedColumn.value_counts.length > 0 && (
              <div>
                <h4 className="mb-3 text-sm font-semibold text-gray-800 sm:text-base">Value Frequency</h4>
                
                <div className="grid gap-6 md:grid-cols-2">
                  {/* Bar Chart */}
                  <div className="w-full h-64 sm:h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={selectedColumn.value_counts} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" fontSize={12} />
                        <YAxis dataKey="value" type="category" width={80} fontSize={10} />
                        <Tooltip />
                        <Legend wrapperStyle={{ fontSize: '12px' }} />
                        <Bar dataKey="count" fill="#ec4899" name="Count" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Pie Chart */}
                  <div className="w-full h-64 sm:h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={selectedColumn.value_counts}
                          dataKey="count"
                          nameKey="value"
                          cx="50%"
                          cy="50%"
                          outerRadius={80}
                          label={(entry) => `${entry.value} (${entry.percentage}%)`}
                          fontSize={10}
                        >
                          {selectedColumn.value_counts.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend wrapperStyle={{ fontSize: '12px' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Frequency Table */}
                <div className="mt-4 overflow-x-auto rounded-xl">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase sm:px-6">Value</th>
                        <th className="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase sm:px-6">Count</th>
                        <th className="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase sm:px-6">Percentage</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {selectedColumn.value_counts.map((item, idx) => (
                        <tr key={idx}>
                          <td className="px-3 py-4 text-xs text-gray-900 break-words sm:px-6 sm:text-sm whitespace-normal">{item.value}</td>
                          <td className="px-3 py-4 text-xs text-gray-900 sm:px-6 sm:text-sm whitespace-nowrap">{item.count.toLocaleString()}</td>
                          <td className="px-3 py-4 text-xs text-gray-900 sm:px-6 sm:text-sm whitespace-nowrap">{item.percentage}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
