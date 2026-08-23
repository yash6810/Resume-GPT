import React from 'react';

export function TermsModal({ isOpen, onClose }) {
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
          Terms of Service &amp; Scoring Disclaimers
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', fontSize: '0.875rem', color: '#94a3b8', lineHeight: '1.6' }}>
          <div>
            <strong style={{ color: '#f8fafc' }}>1. Screening Readiness &amp; Match Simulation</strong>
            <p>ATS Match scores and platform simulations represent objective parsing compatibility heuristics and keyword density models. They are designed to guide optimization and do not represent internal proprietary hiring decisions.</p>
          </div>
          <div>
            <strong style={{ color: '#f8fafc' }}>2. Anti-Fabrication &amp; Truthfulness</strong>
            <p>Users remain solely responsible for the factual accuracy of their resumes. You must only include skills and bullet achievements for which you have genuine, verifiable hands-on experience.</p>
          </div>
        </div>

        <button onClick={onClose} className="btn btn-primary" style={{ marginTop: '1.5rem', width: '100%' }}>
          Acknowledge &amp; Close
        </button>
      </div>
    </div>
  );
}
