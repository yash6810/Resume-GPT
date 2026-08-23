import React, { useState } from 'react';
import { useToast } from '../../hooks/useToast';

export function AutoTailorModal({ isOpen, onClose, onApplyTailoring }) {
  const [role, setRole] = useState('Senior Cloud Architect');
  const [jd, setJd] = useState('Looking for an experienced Cloud Architect proficient in AWS, Kubernetes, Terraform, microservices, and high-availability distributed systems.');

  const { showToast } = useToast();

  if (!isOpen) return null;

  const handleTailor = (e) => {
    e.preventDefault();
    if (!role.trim()) return;

    onApplyTailoring(role, jd);
    showToast(`🎯 Auto-Tailored resume for "${role}"!`, 'success');
    onClose();
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
        maxWidth: '600px',
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

        <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#fff', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span className="material-symbols-outlined" style={{ color: '#14b8a6' }}>auto_fix_high</span>
          1-Click Auto-Tailor to Job Description
        </h3>
        <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginBottom: '1.5rem' }}>
          Inject target role keywords, metrics, and structured skills into your resume builder.
        </p>

        <form onSubmit={handleTailor} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>
              Target Job Title
            </label>
            <input
              type="text"
              required
              className="field"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>
              Job Description or Key Requirements
            </label>
            <textarea
              rows={5}
              className="field"
              value={jd}
              onChange={(e) => setJd(e.target.value)}
            />
          </div>

          <button type="submit" className="btn btn-accent" style={{ padding: '0.75rem', marginTop: '0.5rem' }}>
            🚀 Apply 1-Click Tailoring
          </button>
        </form>
      </div>
    </div>
  );
}
