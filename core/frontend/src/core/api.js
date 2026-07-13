// Cliente API base para el frontend
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiClient {
  constructor() {
    this.baseUrl = API_BASE;
  }

  getToken() {
    return localStorage.getItem('token');
  }

  async request(method, endpoint, data = null) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = { 'Content-Type': 'application/json' };
    const token = this.getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const config = { method, headers };
    if (data && method !== 'GET') config.body = JSON.stringify(data);

    const response = await fetch(url, config);
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Error ${response.status}`);
    }
    return response.json();
  }

  get(endpoint) { return this.request('GET', endpoint); }
  post(endpoint, data) { return this.request('POST', endpoint, data); }
  put(endpoint, data) { return this.request('PUT', endpoint, data); }
  delete(endpoint) { return this.request('DELETE', endpoint); }
}

export const api = new ApiClient();

export const contactosApi = {
  listar: (tipo) => api.get(`/contactos${tipo ? `?tipo=${tipo}` : ''}`),
  crear: (data) => api.post('/contactos', data),
  obtener: (id) => api.get(`/contactos/${id}`),
  actualizar: (id, data) => api.put(`/contactos/${id}`, data),
  eliminar: (id) => api.delete(`/contactos/${id}`),
};

export const authApi = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  me: () => api.get('/auth/me'),
};
