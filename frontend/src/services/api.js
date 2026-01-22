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
  login: (data) => api.post('/auth/login', data),
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
  delete: (id) => api.delete(`/datasets/${id}`)
}

export default api
