import React, { useState } from 'react';
import { useJobs } from '../../hooks/useJobs';
import { useToast } from '../../hooks/useToast';

export function AddJobModal({ isOpen, onClose }) {
  const [company, setCompany] = useState('');
  const [position, setPosition] = useState('');
  const [status, setStatus] = useState('applied');
  const [score, setScore] = useState(88);

  const { addJob } = useJobs();
  const { showToast } = useToast();

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!company.trim() || !position.trim()) {
      showToast('Company and Position are required', 'error');
      return;
    }

    addJob({
      company,
      position,
      status,
      score: Number(score) || 85,
    });

    showToast(`Added ${company} to Application Pipeline!`, 'success');
    setCompany('');
    setPosition('');
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
        maxWidth: '480px',
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
          Add Tracked Application
        </h3>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>Company Name</label>
            <input
              type="text"
              required
              className="field"
              placeholder="e.g. Stripe"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>Job Title</label>
            <input
              type="text"
              required
              className="field"
              placeholder="e.g. Senior Backend Engineer"
              value={position}
              onChange={(e) => setPosition(e.target.value)}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>Initial Pipeline Stage</label>
            <select
              className="field"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <option value="applied">Applied (Submitted)</option>
              <option value="screening">Recruiter Screening</option>
              <option value="interview">Technical Interview</option>
              <option value="offer">Offer Received</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.35rem' }}>Target ATS Match Score</label>
            <input
              type="number"
              min="0"
              max="100"
              className="field"
              value={score}
              onChange={(e) => setScore(e.target.value)}
            />
          </div>

          <button type="submit" className="btn btn-primary" style={{ padding: '0.75rem', marginTop: '0.5rem' }}>
            Save Application to Pipeline
          </button>
        </form>
      </div>
    </div>
  );
}
