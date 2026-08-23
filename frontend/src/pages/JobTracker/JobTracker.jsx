import React from 'react';
import { useJobs } from '../../hooks/useJobs';

export function JobTracker({ openModal }) {
  const { jobs, moveJob, deleteJob } = useJobs();

  const columns = [
    { id: 'applied', label: 'Applied', color: '#38bdf8', icon: 'send' },
    { id: 'screening', label: 'Screening', color: '#818cf8', icon: 'phone_in_talk' },
    { id: 'interview', label: 'Technical Interview', color: '#f59e0b', icon: 'groups' },
    { id: 'offer', label: 'Offer Received', color: '#10b981', icon: 'verified' },
  ];

  return (
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', letterSpacing: '-0.025em' }}>
            Application Pipeline Kanban
          </h1>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Track application progress, ATS match records, and advance candidates through recruitment stages.
          </p>
        </div>

        <button onClick={() => openModal('addJob')} className="btn btn-primary">
          <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>add</span>
          <span>Add Application</span>
        </button>
      </div>

      {/* Kanban Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem', alignItems: 'start' }}>
        {columns.map((col) => {
          const colJobs = jobs.filter((j) => j.status === col.id);
          return (
            <div key={col.id} className="glass-card" style={{ padding: '1.25rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem', minHeight: '500px' }}>
              {/* Column Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '0.75rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className="material-symbols-outlined" style={{ color: col.color, fontSize: '1.1rem' }}>{col.icon}</span>
                  <span style={{ fontSize: '0.875rem', fontWeight: '700', color: '#f8fafc' }}>{col.label}</span>
                </div>
                <span style={{ padding: '0.15rem 0.5rem', borderRadius: '9999px', backgroundColor: 'rgba(255, 255, 255, 0.05)', fontSize: '11px', fontWeight: '700', color: '#94a3b8' }}>
                  {colJobs.length}
                </span>
              </div>

              {/* Cards List */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {colJobs.map((job) => (
                  <div
                    key={job.id}
                    className="glass-card"
                    style={{
                      padding: '1rem',
                      borderRadius: '0.75rem',
                      backgroundColor: 'rgba(15, 23, 42, 0.8)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.5rem',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div>
                        <div style={{ fontSize: '0.875rem', fontWeight: '700', color: '#fff' }}>{job.position}</div>
                        <div style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>{job.company}</div>
                      </div>
                      <span style={{
                        padding: '0.15rem 0.4rem',
                        borderRadius: '0.375rem',
                        fontSize: '11px',
                        fontWeight: '700',
                        fontFamily: 'var(--font-mono)',
                        backgroundColor: job.score >= 80 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(56, 189, 248, 0.15)',
                        color: job.score >= 80 ? '#6ee7b7' : '#38bdf8',
                        border: '1px solid currentColor'
                      }}>
                        {job.score}%
                      </span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem', paddingTop: '0.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.05)' }}>
                      <span style={{ fontSize: '10px', color: '#64748b' }}>{job.date || 'Recent'}</span>
                      <div style={{ display: 'flex', gap: '0.35rem' }}>
                        {col.id !== 'offer' && (
                          <button
                            onClick={() => moveJob(job.id)}
                            style={{ padding: '0.2rem 0.5rem', borderRadius: '0.25rem', backgroundColor: 'rgba(56, 189, 248, 0.15)', border: 'none', color: '#38bdf8', fontSize: '10px', fontWeight: '600', cursor: 'pointer' }}
                          >
                            Advance ➔
                          </button>
                        )}
                        <button
                          onClick={() => deleteJob(job.id)}
                          style={{ padding: '0.2rem 0.4rem', borderRadius: '0.25rem', backgroundColor: 'transparent', border: 'none', color: '#64748b', fontSize: '11px', cursor: 'pointer' }}
                          title="Delete application"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
