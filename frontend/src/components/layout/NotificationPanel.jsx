import React from 'react';

export function NotificationPanel({ isOpen, onClose }) {
  if (!isOpen) return null;

  const notifs = [
    { id: 1, title: 'Resume Analyzed', text: 'Senior Software Engineer resume scored 88/100.', time: '10m ago', icon: 'check_circle', color: '#10b981' },
    { id: 2, title: 'Interview Milestone', text: 'Application moved to Screening for Initech.', time: '1h ago', icon: 'trending_up', color: '#38bdf8' },
    { id: 3, title: 'Pro Tip', text: 'Quantify metrics in your experience bullets to increase recruiter response.', time: '1d ago', icon: 'lightbulb', color: '#f59e0b' }
  ];

  return (
    <div style={{
      position: 'absolute',
      top: '64px',
      right: '1.5rem',
      width: '320px',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      backdropFilter: 'blur(20px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '0.75rem',
      boxShadow: '0 20px 40px rgba(0,0,0,0.6)',
      zIndex: 50,
      padding: '1rem',
      animation: 'fadeIn 0.2s ease-out'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
        <h4 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#f8fafc' }}>Notifications</h4>
        <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer' }}>✕</button>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {notifs.map((n) => (
          <div key={n.id} style={{ display: 'flex', gap: '0.75rem', padding: '0.5rem', borderRadius: '0.5rem', backgroundColor: 'rgba(255, 255, 255, 0.03)' }}>
            <span className="material-symbols-outlined" style={{ fontSize: '1.25rem', color: n.color }}>{n.icon}</span>
            <div>
              <div style={{ fontSize: '12px', fontWeight: '600', color: '#f8fafc' }}>{n.title}</div>
              <div style={{ fontSize: '11px', color: '#94a3b8' }}>{n.text}</div>
              <div style={{ fontSize: '10px', color: '#64748b', marginTop: '0.2rem' }}>{n.time}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
