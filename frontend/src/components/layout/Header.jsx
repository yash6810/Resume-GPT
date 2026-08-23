import React from 'react';
import { useAuth } from '../../hooks/useAuth';

export function Header({ openModal, toggleNotifs }) {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header style={{
      height: '64px',
      borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
      backgroundColor: 'rgba(15, 23, 42, 0.7)',
      backdropFilter: 'blur(16px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 1.5rem',
      flexShrink: 0
    }}>
      {/* Search / Live System Status */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <span style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.35rem',
          padding: '0.25rem 0.6rem',
          borderRadius: '9999px',
          backgroundColor: 'rgba(16, 185, 129, 0.15)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          color: '#6ee7b7',
          fontSize: '11px',
          fontWeight: '600'
        }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#10b981' }}></span>
          ATS Match Engine Online
        </span>
      </div>

      {/* Right Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <button
          onClick={toggleNotifs}
          style={{
            background: 'transparent',
            border: 'none',
            color: '#94a3b8',
            cursor: 'pointer',
            padding: '0.35rem',
            borderRadius: '0.375rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
          title="Notifications"
        >
          <span className="material-symbols-outlined" style={{ fontSize: '1.25rem' }}>notifications</span>
        </button>

        {isAuthenticated ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <button
              onClick={() => openModal('account')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.375rem 0.75rem',
                borderRadius: '0.5rem',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: '#f8fafc',
                fontSize: '0.875rem',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color: '#38bdf8' }}>account_circle</span>
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
                fontSize: '0.875rem',
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
              style={{ padding: '0.375rem 0.875rem', fontSize: '0.875rem' }}
            >
              Sign In
            </button>
            <button
              onClick={() => openModal('auth', 'register')}
              className="btn btn-primary"
              style={{ padding: '0.375rem 0.875rem', fontSize: '0.875rem' }}
            >
              Get Started Free
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
