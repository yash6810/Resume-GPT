import React, { useState } from 'react';
import { changePassword, deleteAccount } from '../../services/authService';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../hooks/useToast';

export function AccountModal({ isOpen, onClose }) {
  const { user, logout } = useAuth();
  const { showToast } = useToast();

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await changePassword(currentPassword, newPassword);
      showToast('Password changed successfully!', 'success');
      setCurrentPassword('');
      setNewPassword('');
    } catch (err) {
      showToast(err.message || 'Password update failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm('Are you absolutely sure? This will permanently delete your account, stored jobs, and resume history (GDPR Right to Erasure).')) {
      try {
        await deleteAccount();
        logout();
        showToast('Account permanently erased.', 'info');
        onClose();
      } catch (err) {
        showToast(err.message || 'Deletion failed', 'error');
      }
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1rem'
    }}>
      <div className="glass-card" style={{
        width: '100%',
        maxWidth: '520px',
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

        <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#fff', marginBottom: '1.5rem' }}>
          Account Settings
        </h3>

        {/* Profile Details */}
        <div style={{ padding: '1rem', borderRadius: '0.75rem', backgroundColor: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.06)', marginBottom: '1.5rem' }}>
          <div style={{ fontSize: '0.875rem', fontWeight: '700', color: '#f8fafc' }}>{user?.full_name || user?.username}</div>
          <div style={{ fontSize: '0.8125rem', color: '#94a3b8', marginTop: '0.2rem' }}>{user?.email || 'Active User'}</div>
          <div style={{ display: 'inline-block', marginTop: '0.5rem', padding: '0.2rem 0.5rem', borderRadius: '9999px', fontSize: '10px', fontWeight: '700', backgroundColor: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8' }}>
            Plan: {user?.plan ? user.plan.toUpperCase() : 'STARTER'}
          </div>
        </div>

        {/* Change Password Form */}
        <form onSubmit={handleChangePassword} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.5rem' }}>
          <h4 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#fff' }}>Change Password</h4>
          <input
            type="password"
            required
            className="field"
            placeholder="Current Password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
          <input
            type="password"
            required
            className="field"
            placeholder="New Password (min 8 chars)"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <button type="submit" disabled={loading} className="btn btn-ghost" style={{ alignSelf: 'flex-start' }}>
            {loading ? 'Updating...' : 'Update Password'}
          </button>
        </form>

        {/* GDPR Account Deletion */}
        <div style={{ borderTop: '1px solid rgba(244, 63, 94, 0.2)', paddingTop: '1rem' }}>
          <div style={{ fontSize: '0.8125rem', color: '#fda4af', marginBottom: '0.5rem' }}>
            Permanent GDPR Data Erasure
          </div>
          <button
            type="button"
            onClick={handleDeleteAccount}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '0.5rem',
              backgroundColor: 'rgba(244, 63, 94, 0.1)',
              border: '1px solid rgba(244, 63, 94, 0.3)',
              color: '#f43f5e',
              fontSize: '0.8125rem',
              fontWeight: '600',
              cursor: 'pointer'
            }}
          >
            Delete My Account &amp; Data
          </button>
        </div>
      </div>
    </div>
  );
}
