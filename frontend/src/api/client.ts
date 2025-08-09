const API_BASE = import.meta.env.VITE_API_BASE_URL || (window.__API_BASE__ || 'http://localhost:5000');

async function request(path: string, opts: any = {}) {
  const url = API_BASE.replace(/\/$/, '') + path;
  const headers = opts.headers || {};
  if (opts.json) {
    headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(opts.json);
    delete opts.json;
  }
  if (opts.token) {
    headers['Authorization'] = `Bearer ${opts.token}`;
    delete opts.token;
  }
  opts.headers = headers;
  const res = await fetch(url, opts);
  const text = await res.text();
  try { return JSON.parse(text); } catch(e) { return text; }
}

export async function register(name: string, email: string, password: string) {
  return request('/api/auth/register', { method: 'POST', json: { name, email, password } });
}

export async function login(email: string, password: string) {
  return request('/api/auth/login', { method: 'POST', json: { email, password } });
}

export async function me(token: string) {
  return request('/api/auth/me', { method: 'GET', token });
}

export async function uploadResume(file: File, token?: string) {
  const form = new FormData();
  form.append('file', file);
  const headers:any = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch((API_BASE.replace(/\/$/, '') + '/api/upload_resume'), { method: 'POST', body: form, headers });
  return res.json();
}

export async function aiRecommend(payload: any, token?: string) {
  return request('/api/ai/recommend', { method: 'POST', json: payload, token });
}

export async function analyticsEvent(name: string, metadata: any = {}) {
  return request('/api/analytics/event', { method: 'POST', json: { name, metadata } });
}

export default { register, login, me, uploadResume, aiRecommend, analyticsEvent };
