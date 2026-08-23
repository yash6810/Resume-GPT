import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useTheme } from '../../hooks/useTheme';

export function Header({ openModal, toggleNotifs }) {
  const { user, isAuthenticated, logout } = useAuth();
  const { theme, toggleTheme, isLight } = useTheme();

  return (
    <header style={{
      height: '60px',
      borderBottom: '1px solid var(--border-color)',
      backgroundColor: 'var(--bg-secondary)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 1.5rem',
      flexShrink: 0
    }}>
      {/* Linear Search & Command Bar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', width: '380px' }}>
        <div className="command-search" style={{ width: '100%' }}>
          <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>search</span>
          <input
            type="text"
            placeholder="Search resumes, roles, skills..."
            style={{
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: 'var(--text-primary)',
              fontSize: '0.8125rem',
              width: '100%',
              fontFamily: 'inherit'
            }}
          />
          <span style={{
            fontSize: '10px',
            padding: '2px 5px',
            borderRadius: '4px',
            backgroundColor: 'rgba(255, 255, 255, 0.08)',
            color: 'var(--text-muted)',
            fontFamily: 'var(--font-mono)'
          }}>⌘K</span>
        </div>
      </div>

      {/* Right Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <span className="status-pill status-found" style={{ fontSize: '11px' }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: 'var(--accent-emerald)' }}></span>
          ATS Engine Online
        </span>

        {/* Theme Toggle Button */}
        <button
          onClick={toggleTheme}
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-primary)',
            cursor: 'pointer',
            padding: '0.4rem 0.65rem',
            borderRadius: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            fontSize: '0.75rem',
            fontWeight: '600',
            transition: 'all 0.2s ease',
            boxShadow: 'var(--specular-highlight)'
          }}
          title={isLight ? "Switch to Dark Mode" : "Switch to Light Mode"}
        >
          <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color: isLight ? 'var(--apple-orange)' : 'var(--apple-blue)' }}>
            {isLight ? 'light_mode' : 'dark_mode'}
          </span>
          <span style={{ fontSize: '11px', textTransform: 'capitalize' }}>
            {theme}
          </span>
        </button>

        <button
          onClick={toggleNotifs}
          style={{
            background: 'transparent',
            border: '1px solid var(--border-color)',
            color: 'var(--text-secondary)',
            cursor: 'pointer',
            padding: '0.4rem',
            borderRadius: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.2s ease'
          }}
          title="Notifications"
        >
          <span className="material-symbols-outlined" style={{ fontSize: '1.15rem' }}>notifications</span>
        </button>

        {isAuthenticated ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button
              onClick={() => openModal('account')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.375rem 0.75rem',
                borderRadius: '0.5rem',
                backgroundColor: 'var(--bg-card)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
                fontSize: '0.8125rem',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color: 'var(--accent-sky)' }}>account_circle</span>
              <span>{user?.full_name || user?.username || 'My Account'}</span>
            </button>
            <button
              onClick={logout}
              style={{
                padding: '0.375rem 0.75rem',
                borderRadius: '0.5rem',
                backgroundColor: 'transparent',
                border: '1px solid rgba(244, 63, 94, 0.3)',
                color: '#fda4af',
                fontSize: '0.8125rem',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              Sign Out
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button
              onClick={() => openModal('auth', 'login')}
              className="btn btn-ghost"
              style={{ padding: '0.375rem 0.875rem', fontSize: '0.8125rem' }}
            >
              Sign In
            </button>
            <button
              onClick={() => openModal('auth', 'register')}
              className="btn btn-primary"
              style={{ padding: '0.375rem 0.875rem', fontSize: '0.8125rem' }}
            >
              Get Started Free
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
