import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000'
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me')
}

export const datasetAPI = {
  getAll: () => api.get('/datasets/'),
  create: (data) => api.post('/datasets/', data),
  getById: (id) => api.get(`/datasets/${id}`),
  delete: (id) => api.delete(`/datasets/${id}`)
}

export default api
