import { request, setAuthToken } from './api.js';

export async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const res = await request('/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData.toString(),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Authentication failed' }));
    throw new Error(err.detail || 'Login failed');
  }

  const data = await res.json();
  if (data.access_token) {
    setAuthToken(data.access_token);
  }
  return data;
}

export async function register(email, username, password, fullName = '') {
  const res = await request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      username,
      password,
      full_name: fullName,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Registration failed' }));
    throw new Error(err.detail || 'Registration failed');
  }

  return res.json();
}

export async function getCurrentUser() {
  const res = await request('/auth/me', { method: 'GET' });
  if (!res.ok) return null;
  return res.json();
}

export async function forgotPassword(email) {
  const res = await request('/auth/forgot-password', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || 'Password reset request failed');
  }
  return res.json();
}

export async function resetPassword(token, newPassword) {
  const res = await request('/auth/reset-password', {
    method: 'POST',
    body: JSON.stringify({ token, new_password: newPassword }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Reset failed' }));
    throw new Error(err.detail || 'Password reset failed');
  }
  return res.json();
}

export async function changePassword(currentPassword, newPassword) {
  const res = await request('/auth/change-password', {
    method: 'POST',
    body: JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Update failed' }));
    throw new Error(err.detail || 'Password change failed');
  }
  return res.json();
}

export async function deleteAccount() {
  const res = await request('/auth/me', { method: 'DELETE' });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Deletion failed' }));
    throw new Error(err.detail || 'Account deletion failed');
  }
  setAuthToken(null);
  return res.json();
}

export function logout() {
  setAuthToken(null);
}
