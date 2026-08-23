import React, { useState } from 'react';
import { rewriteBullet } from '../../services/analyzeService';
import { useToast } from '../../hooks/useToast';

export function BulletRewriterModal({ isOpen, onClose }) {
  const [bullet, setBullet] = useState('Helped the backend team fix slow database queries and deployed the application.');
  const [keywords, setKeywords] = useState('Python, PostgreSQL, Redis, Latency Optimization');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const { showToast } = useToast();

  if (!isOpen) return null;

  const handleRewrite = async (e) => {
    e.preventDefault();
    if (!bullet.trim()) return;

    setLoading(true);
    try {
      const kwList = keywords.split(',').map((k) => k.trim()).filter(Boolean);
      const res = await rewriteBullet(bullet, kwList);
      setResults(res);
      showToast('Bullet rewritten with ATS optimizations!', 'success');
    } catch (err) {
      showToast(err.message || 'Rewriting failed', 'error');
    } finally {
      setLoading(false);
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
        maxWidth: '680px',
        maxHeight: '90vh',
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

        <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#fff', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span className="material-symbols-outlined" style={{ color: '#38bdf8' }}>auto_fix_high</span>
          AI Bullet Rewriter &amp; Anti-Fabrication Guard
        </h3>
        <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginBottom: '1.5rem' }}>
          Transform weak statements into high-impact, quantified STAR-format accomplishments.
        </p>

        <form onSubmit={handleRewrite} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>
              Original Experience Bullet
            </label>
            <textarea
              required
              rows={3}
              className="field"
              value={bullet}
              onChange={(e) => setBullet(e.target.value)}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>
              Target Keywords (comma-separated)
            </label>
            <input
              type="text"
              className="field"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
            />
          </div>

          <button type="submit" disabled={loading} className="btn btn-primary" style={{ padding: '0.75rem' }}>
            {loading ? 'Generating High-Impact Variants...' : '✨ Rewrite & Optimize Bullet'}
          </button>
        </form>

        {results && results.variants && (
          <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', borderTop: '1px solid rgba(255, 255, 255, 0.1)', paddingTop: '1.5rem' }}>
            {results.verification_note && (
              <div style={{ padding: '0.75rem', borderRadius: '0.5rem', backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.25)', color: '#fde68a', fontSize: '12px' }}>
                🛡️ {results.verification_note}
              </div>
            )}

            <div>
              <span style={{ fontSize: '11px', fontWeight: '700', color: '#38bdf8', letterSpacing: '0.05em' }}>VARIANT 1: ATS HIGH-DENSITY</span>
              <div style={{ marginTop: '0.35rem', padding: '0.875rem', borderRadius: '0.5rem', backgroundColor: 'rgba(0, 0, 0, 0.4)', border: '1px solid rgba(56, 189, 248, 0.2)', fontSize: '0.875rem', color: '#f8fafc' }}>
                {results.variants[0]}
              </div>
            </div>

            {results.variants[1] && (
              <div>
                <span style={{ fontSize: '11px', fontWeight: '700', color: '#10b981', letterSpacing: '0.05em' }}>VARIANT 2: EXECUTIVE STAR NARRATIVE</span>
                <div style={{ marginTop: '0.35rem', padding: '0.875rem', borderRadius: '0.5rem', backgroundColor: 'rgba(0, 0, 0, 0.4)', border: '1px solid rgba(16, 185, 129, 0.2)', fontSize: '0.875rem', color: '#f8fafc' }}>
                  {results.variants[1]}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
