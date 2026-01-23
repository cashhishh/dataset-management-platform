import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data, {
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    }
  }),
  getCurrentUser: () => api.get('/auth/me')
}

export const datasetAPI = {
  getAll: () => api.get('/datasets/'),
  create: (data) => api.post('/datasets/', data),
  upload: (formData) => api.post('/datasets/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getById: (id) => api.get(`/datasets/${id}`),
  getDetail: (id) => api.get(`/datasets/${id}/detail`),
  getPreview: (id, limit = 10) => api.get(`/datasets/${id}/preview`, { params: { limit } }),
  getQuality: (id) => api.get(`/datasets/${id}/quality`),
  getAdvancedQuality: (id) => api.get(`/datasets/${id}/advanced-quality`),
  getProfile: (id) => api.get(`/datasets/${id}/profile`),
  delete: (id) => api.delete(`/datasets/${id}`),
  
  // Versioning
  getVersions: (id) => api.get(`/datasets/${id}/versions/`),
  uploadVersion: (id, formData) => api.post(`/datasets/${id}/versions/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getVersion: (id, versionNum) => api.get(`/datasets/${id}/versions/${versionNum}`),
  compareVersions: (id, v1, v2) => api.get(`/datasets/${id}/versions/compare/${v1}/${v2}`),
  deleteVersion: (id, versionNum) => api.delete(`/datasets/${id}/versions/${versionNum}`),
  
  // Quality Rules
  getQualityRules: (id, activeOnly = true) => api.get(`/datasets/${id}/rules/`, { params: { active_only: activeOnly } }),
  createQualityRule: (id, ruleData) => api.post(`/datasets/${id}/rules/`, ruleData),
  deleteQualityRule: (datasetId, ruleId) => api.delete(`/datasets/${datasetId}/rules/${ruleId}`),
  toggleQualityRule: (datasetId, ruleId, isActive) => api.post(`/datasets/${datasetId}/rules/${ruleId}/toggle`, null, { params: { is_active: isActive } }),
  validateQualityRules: (id) => api.post(`/datasets/${id}/rules/validate`),
  
  // Sharing
  shareDataset: (id, shareData) => api.post(`/datasets/${id}/shares/`, shareData),
  getShares: (id) => api.get(`/datasets/${id}/shares/`),
  getSharedWithMe: () => api.get('/datasets/0/shares/shared-with-me'),
  revokeShare: (datasetId, shareId) => api.delete(`/datasets/${datasetId}/shares/${shareId}`),
  
  // Export
  exportQualityJSON: (id) => api.get(`/datasets/${id}/export/quality/json`, { responseType: 'blob' }),
  exportQualityCSV: (id) => api.get(`/datasets/${id}/export/quality/csv`, { responseType: 'blob' })
}

// Background Tasks API
export const taskAPI = {
  createTask: (taskData) => api.post('/tasks/', taskData),
  getTask: (taskId) => api.get(`/tasks/${taskId}`),
  getUserTasks: (limit = 50) => api.get('/tasks/', { params: { limit } }),
  cancelTask: (taskId) => api.delete(`/tasks/${taskId}`)
}

export default api
