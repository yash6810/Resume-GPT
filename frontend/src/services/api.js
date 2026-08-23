// Centralized API client with dynamic origin resolution & JWT injection

const FALLBACK_API_BASE = 'https://resumegpt.onrender.com';
const STORAGE_TOKEN = 'resumegpt_token';

export function getApiBase() {
  if (typeof window !== 'undefined' && window.location) {
    const origin = window.location.origin;
    if (origin && origin.startsWith('http')) {
      return origin;
    }
  }
  return FALLBACK_API_BASE;
}

export function getAuthToken() {
  try {
    return localStorage.getItem(STORAGE_TOKEN) || null;
  } catch (e) {
    return null;
  }
}

export function setAuthToken(token) {
  try {
    if (token) {
      localStorage.setItem(STORAGE_TOKEN, token);
    } else {
      localStorage.removeItem(STORAGE_TOKEN);
    }
  } catch (e) {
    console.error('Storage error:', e);
  }
}

export async function request(endpoint, options = {}) {
  const base = getApiBase();
  const url = endpoint.startsWith('http') ? endpoint : `${base}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
  
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  const token = getAuthToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  return response;
}
