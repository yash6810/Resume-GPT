import React, { useState } from 'react';
import { login, register, forgotPassword } from '../../services/authService';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../hooks/useToast';

export function AuthModal({ isOpen, onClose, initialTab = 'login' }) {
  const [tab, setTab] = useState(initialTab);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);

  const { setUser } = useAuth();
  const { showToast } = useToast();

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (tab === 'login') {
        const data = await login(username || email, password);
        setUser({ username: username || email });
        showToast('Signed in successfully!', 'success');
        onClose();
      } else if (tab === 'register') {
        await register(email, username, password, fullName);
        showToast('Account created! Please sign in.', 'success');
        setTab('login');
      } else if (tab === 'forgot') {
        await forgotPassword(email);
        showToast('Password reset link sent to your email!', 'success');
        setTab('login');
      }
    } catch (err) {
      showToast(err.message || 'Authentication error', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1rem'
    }}>
      <div className="glass-card" style={{
        width: '100%',
        maxWidth: '420px',
        borderRadius: '1rem',
        padding: '2rem',
        position: 'relative'
      }}>
        <button
          onClick={onClose}
          style={{ position: 'absolute', top: '1.25rem', right: '1.25rem', background: 'none', border: 'none', color: '#94a3b8', fontSize: '1.25rem', cursor: 'pointer' }}
        >
          ✕
        </button>

        <div style={{ display: 'flex', gap: '1rem', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', marginBottom: '1.5rem', paddingBottom: '0.5rem' }}>
          <button
            onClick={() => setTab('login')}
            style={{ background: 'none', border: 'none', color: tab === 'login' ? '#38bdf8' : '#94a3b8', fontWeight: '700', fontSize: '0.95rem', cursor: 'pointer' }}
          >
            Sign In
          </button>
          <button
            onClick={() => setTab('register')}
            style={{ background: 'none', border: 'none', color: tab === 'register' ? '#38bdf8' : '#94a3b8', fontWeight: '700', fontSize: '0.95rem', cursor: 'pointer' }}
          >
            Create Account
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {tab === 'register' && (
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '600', color: '#94a3b8', marginBottom: '0.35rem' }}>Full Name</label>
              <input
                type="text"
                className="field"
                placeholder="Alex Morgan"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
          )}

          {(tab === 'register' || tab === 'forgot') && (
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '600', color: '#94a3b8', marginBottom: '0.35rem' }}>Email Address</label>
              <input
                type="email"
                required
                className="field"
                placeholder="alex@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          )}

          {tab !== 'forgot' && (
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '600', color: '#94a3b8', marginBottom: '0.35rem' }}>Username or Email</label>
              <input
                type="text"
                required
                className="field"
                placeholder="alex_dev"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
          )}

          {tab !== 'forgot' && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <label style={{ fontSize: '11px', fontWeight: '600', color: '#94a3b8' }}>Password</label>
                {tab === 'login' && (
                  <span
                    onClick={() => setTab('forgot')}
                    style={{ fontSize: '11px', color: '#38bdf8', cursor: 'pointer' }}
                  >
                    Forgot?
                  </span>
                )}
              </div>
              <input
                type="password"
                required
                className="field"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '0.75rem', marginTop: '0.5rem' }}
          >
            {loading ? 'Processing...' : tab === 'login' ? 'Sign In to ResumeGPT' : tab === 'register' ? 'Create Account' : 'Send Reset Link'}
          </button>
        </form>
      </div>
    </div>
  );
}
