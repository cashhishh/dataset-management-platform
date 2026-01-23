import { useState, useEffect } from 'react'
import { datasetAPI } from '../services/api'

export default function AdvancedQualityReport({ datasetId }) {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadReport()
  }, [datasetId])

  const loadReport = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await datasetAPI.getAdvancedQuality(datasetId)
      setReport(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load quality report')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-12 h-12 border-b-2 border-indigo-600 rounded-full animate-spin"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 border border-red-200 rounded-lg bg-red-50">
        <p className="text-red-800">{error}</p>
      </div>
    )
  }

  if (!report) {
    return null
  }

  const getQualityColor = (score) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getQualityBgColor = (score) => {
    if (score >= 90) return 'bg-green-100'
    if (score >= 70) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Overall Quality Score */}
      <div className="p-4 bg-white shadow sm:p-6 rounded-xl">
        <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
          <div className="flex-1">
            <h3 className="text-base font-semibold text-gray-900 sm:text-lg">Overall Quality Score</h3>
            <p className="mt-1 text-xs text-gray-600 sm:text-sm">
              {report.dataset_metrics.total_rows.toLocaleString()} rows × {report.dataset_metrics.total_columns} columns
            </p>
          </div>
          <div className={`text-4xl font-bold sm:text-5xl ${getQualityColor(report.quality_score)}`}>
            {report.quality_score.toFixed(1)}
          </div>
        </div>
      </div>

      {/* Issues Summary */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="p-4 bg-white shadow rounded-xl">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-600 sm:text-sm">Missing Values</p>
              <p className="mt-1 text-xl font-semibold text-gray-900 sm:text-2xl">
                {report.issues_summary.missing_values.toLocaleString()}
              </p>
            </div>
            <div className="flex-shrink-0 p-3 bg-yellow-100 rounded-full">
              <svg className="w-5 h-5 text-yellow-600 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="p-4 bg-white shadow rounded-xl">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-600 sm:text-sm">Invalid Values</p>
              <p className="mt-1 text-xl font-semibold text-gray-900 sm:text-2xl">
                {report.issues_summary.invalid_values.toLocaleString()}
              </p>
            </div>
            <div className="flex-shrink-0 p-3 bg-red-100 rounded-full">
              <svg className="w-5 h-5 text-red-600 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
          </div>
        </div>

        <div className="p-4 bg-white shadow rounded-xl">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-600 sm:text-sm">Outliers</p>
              <p className="mt-1 text-xl font-semibold text-gray-900 sm:text-2xl">
                {report.issues_summary.outliers.toLocaleString()}
              </p>
            </div>
            <div className="flex-shrink-0 p-3 bg-purple-100 rounded-full">
              <svg className="w-5 h-5 text-purple-600 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="p-4 bg-white shadow rounded-xl">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-600 sm:text-sm">Type Issues</p>
              <p className="mt-1 text-xl font-semibold text-gray-900 sm:text-2xl">
                {report.issues_summary.type_inconsistencies.toLocaleString()}
              </p>
            </div>
            <div className="flex-shrink-0 p-3 bg-blue-100 rounded-full">
              <svg className="w-5 h-5 text-blue-600 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Column Quality Details */}
      <div className="overflow-hidden bg-white shadow rounded-xl">
        <div className="px-4 py-4 border-b border-gray-200 sm:px-6">
          <h3 className="text-base font-semibold text-gray-900 sm:text-lg">Column Quality Analysis</h3>
        </div>
        <div className="w-full overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Column</th>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Type</th>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Null %</th>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Empty %</th>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Invalid</th>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Type Consistency</th>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Outliers</th>
                <th className="px-3 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6">Numeric Stats</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {report.column_quality.map((col) => (
                <tr key={col.column_name} className="hover:bg-gray-50">
                  <td className="px-3 py-4 text-xs font-medium text-gray-900 sm:px-6 sm:text-sm whitespace-nowrap">
                    {col.column_name}
                  </td>
                  <td className="px-3 py-4 text-xs text-gray-600 sm:px-6 sm:text-sm whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium bg-gray-100 rounded">
                      {col.inferred_type}
                    </span>
                  </td>
                  <td className="px-3 py-4 text-xs text-gray-600 sm:px-6 sm:text-sm whitespace-nowrap">
                    {col.null_percentage.toFixed(1)}%
                  </td>
                  <td className="px-3 py-4 text-xs text-gray-600 sm:px-6 sm:text-sm whitespace-nowrap">
                    {col.empty_percentage.toFixed(1)}%
                  </td>
                  <td className="px-3 py-4 text-xs text-gray-600 sm:px-6 sm:text-sm whitespace-nowrap">
                    {col.invalid_count > 0 ? (
                      <span className="font-medium text-red-600">{col.invalid_count}</span>
                    ) : (
                      <span className="text-green-600">✓</span>
                    )}
                  </td>
                  <td className="px-3 py-4 text-xs sm:px-6 sm:text-sm whitespace-nowrap">
                    {col.type_consistency_percentage === 100 ? (
                      <span className="font-medium text-green-600">100%</span>
                    ) : (
                      <span className="font-medium text-yellow-600">
                        {col.type_consistency_percentage.toFixed(1)}%
                      </span>
                    )}
                  </td>
                  <td className="px-3 py-4 text-xs text-gray-600 sm:px-6 sm:text-sm whitespace-nowrap">
                    {col.outlier_info ? (
                      col.outlier_info.outlier_count > 0 ? (
                        <span className="font-medium text-purple-600">
                          {col.outlier_info.outlier_count} ({col.outlier_info.outlier_percentage.toFixed(1)}%)
                        </span>
                      ) : (
                        <span className="text-green-600">None</span>
                      )
                    ) : (
                      <span className="text-gray-400">N/A</span>
                    )}
                  </td>
                  <td className="px-3 py-4 text-xs text-gray-600 sm:px-6 sm:text-sm">
                    {col.numeric_stats ? (
                      <div className="space-y-1">
                        <div className="text-xs">
                          <span className="text-gray-500">Range:</span> {col.numeric_stats.min.toFixed(2)} - {col.numeric_stats.max.toFixed(2)}
                        </div>
                        <div className="text-xs">
                          <span className="text-gray-500">Mean:</span> {col.numeric_stats.mean.toFixed(2)} | 
                          <span className="ml-1 text-gray-500">Median:</span> {col.numeric_stats.median.toFixed(2)}
                        </div>
                      </div>
                    ) : (
                      <span className="text-gray-400">N/A</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      {report.recommendations && report.recommendations.length > 0 && (
        <div className="p-4 bg-white shadow sm:p-6 rounded-xl">
          <h3 className="mb-4 text-base font-semibold text-gray-900 sm:text-lg">Recommendations</h3>
          <ul className="space-y-2">
            {report.recommendations.map((rec, index) => (
              <li key={index} className="flex items-start">
                <svg className="flex-shrink-0 w-5 h-5 mr-2 text-indigo-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span className="text-xs text-gray-700 sm:text-sm">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
