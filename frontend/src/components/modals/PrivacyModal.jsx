import React from 'react';

export function PrivacyModal({ isOpen, onClose }) {
  if (!isOpen) return null;

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
        maxWidth: '640px',
        maxHeight: '85vh',
        overflowY: 'auto',
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

        <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#fff', marginBottom: '1rem' }}>
          Zero-Knowledge Privacy Policy &amp; Data Rights
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', fontSize: '0.875rem', color: '#94a3b8', lineHeight: '1.6' }}>
          <div>
            <strong style={{ color: '#f8fafc' }}>1. Zero-Knowledge Processing</strong>
            <p>Your resume text, contact details, work history, and job descriptions are processed ephemerally solely to compute scoring and formatting. We never sell, monetize, or share your data.</p>
          </div>
          <div>
            <strong style={{ color: '#f8fafc' }}>2. No AI Model Training</strong>
            <p>Your uploaded resumes and proprietary work history are never used to train public LLM models or commercial datasets.</p>
          </div>
          <div>
            <strong style={{ color: '#f8fafc' }}>3. Complete GDPR &amp; CCPA Right to Erasure</strong>
            <p>You can permanently delete your entire account, stored jobs, and resume history at any moment with a single click in your Account settings.</p>
          </div>
        </div>

        <button onClick={onClose} className="btn btn-primary" style={{ marginTop: '1.5rem', width: '100%' }}>
          Understood &amp; Accept
        </button>
      </div>
    </div>
  );
}
