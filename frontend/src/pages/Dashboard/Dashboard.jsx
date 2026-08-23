import React from 'react';
import { useJobs } from '../../hooks/useJobs';

export function Dashboard({ setActivePage, openModal }) {
  const { metrics, lastScore } = useJobs();

  return (
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header Banner */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: '850', color: '#f8fafc', letterSpacing: '-0.03em' }}>
          Job Search Control Center
        </h1>
        <p style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
          Real-time ATS match diagnostics, pipeline conversion metrics, and 1-click resume tailoring.
        </p>
      </div>

      {/* Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
        {/* Total Pipeline */}
        <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Total Pipeline</span>
            <span className="material-symbols-outlined" style={{ color: '#38bdf8', fontSize: '1.25rem' }}>work_history</span>
          </div>
          <div id="dash-applied" style={{ fontSize: '2rem', fontWeight: '800', color: '#f8fafc', marginTop: '0.5rem', fontFamily: 'var(--font-mono)' }}>
            {metrics.totalJobs}
          </div>
          <div id="dash-applied-sub" style={{ fontSize: '11px', color: '#64748b', marginTop: '0.25rem' }}>
            {metrics.appliedCount} Applied · {metrics.screeningCount} Screening
          </div>
        </div>

        {/* Latest Match Score */}
        <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Latest Match Score</span>
            <span className="material-symbols-outlined" style={{ color: '#10b981', fontSize: '1.25rem' }}>verified</span>
          </div>
          <div id="dash-score" style={{ fontSize: '2rem', fontWeight: '800', color: '#10b981', marginTop: '0.5rem', fontFamily: 'var(--font-mono)' }}>
            {lastScore ? `${lastScore}%` : '--'}
          </div>
          <div style={{ fontSize: '11px', color: '#64748b', marginTop: '0.25rem' }}>
            Target: 85%+ for top callback tier
          </div>
        </div>

        {/* Active Interviews */}
        <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Interviews</span>
            <span className="material-symbols-outlined" style={{ color: '#f59e0b', fontSize: '1.25rem' }}>psychology</span>
          </div>
          <div id="dash-interviews" style={{ fontSize: '2rem', fontWeight: '800', color: '#f59e0b', marginTop: '0.5rem', fontFamily: 'var(--font-mono)' }}>
            {metrics.interviewCount}
          </div>
          <div style={{ fontSize: '11px', color: '#64748b', marginTop: '0.25rem' }}>
            Technical &amp; Behavioral rounds
          </div>
        </div>

        {/* Offers */}
        <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Offers</span>
            <span className="material-symbols-outlined" style={{ color: '#14b8a6', fontSize: '1.25rem' }}>emoji_events</span>
          </div>
          <div id="dash-offers" style={{ fontSize: '2rem', fontWeight: '800', color: '#14b8a6', marginTop: '0.5rem', fontFamily: 'var(--font-mono)' }}>
            {metrics.offerCount}
          </div>
          <div style={{ fontSize: '11px', color: '#64748b', marginTop: '0.25rem' }}>
            Yield achieved
          </div>
        </div>
      </div>

      {/* Conversion Funnel & Outcome Analytics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        {/* Funnel Card */}
        <div className="glass-card" style={{ padding: '1.75rem', borderRadius: '1rem', gridColumn: 'span 2' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="material-symbols-outlined" style={{ color: '#14b8a6' }}>filter_alt</span>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Application Conversion Funnel
              </h3>
            </div>
            <span id="funnel-callback-rate" style={{ padding: '0.25rem 0.75rem', borderRadius: '9999px', backgroundColor: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', color: '#6ee7b7', fontSize: '12px', fontWeight: '700', fontFamily: 'var(--font-mono)' }}>
              {metrics.callbackRate}% Callback Rate
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.75rem', textAlign: 'center' }}>
            <div style={{ padding: '1rem', borderRadius: '0.75rem', backgroundColor: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8' }}>Applied</div>
              <div id="funnel-applied" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#fff', fontFamily: 'var(--font-mono)', margin: '0.25rem 0' }}>{metrics.totalJobs}</div>
              <div style={{ fontSize: '10px', color: '#64748b' }}>100%</div>
            </div>
            <div style={{ padding: '1rem', borderRadius: '0.75rem', backgroundColor: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8' }}>Screening</div>
              <div id="funnel-screening" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#38bdf8', fontFamily: 'var(--font-mono)', margin: '0.25rem 0' }}>{metrics.screeningCount}</div>
              <div style={{ fontSize: '10px', color: '#38bdf8' }}>Stage 2</div>
            </div>
            <div style={{ padding: '1rem', borderRadius: '0.75rem', backgroundColor: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8' }}>Interview</div>
              <div id="funnel-interview" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#f59e0b', fontFamily: 'var(--font-mono)', margin: '0.25rem 0' }}>{metrics.interviewCount}</div>
              <div style={{ fontSize: '10px', color: '#f59e0b' }}>Stage 3</div>
            </div>
            <div style={{ padding: '1rem', borderRadius: '0.75rem', backgroundColor: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8' }}>Offer</div>
              <div id="funnel-offer" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#10b981', fontFamily: 'var(--font-mono)', margin: '0.25rem 0' }}>{metrics.offerCount}</div>
              <div style={{ fontSize: '10px', color: '#10b981' }}>Target Goal</div>
            </div>
          </div>
        </div>

        {/* Hiring Insights Card */}
        <div className="glass-card" style={{ padding: '1.75rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
              <span className="material-symbols-outlined" style={{ color: '#f59e0b' }}>insights</span>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Hiring Signal Insights
              </h3>
            </div>
            <p style={{ fontSize: '0.8125rem', color: '#cbd5e1', lineHeight: '1.6' }}>
              Applications tailored to <strong>85%+ Match Scores</strong> achieve an average of <strong>3.2x higher interview callback rates</strong> than generic submissions.
            </p>
          </div>
          <div style={{ padding: '0.75rem', borderRadius: '0.5rem', backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.25)', color: '#fde68a', fontSize: '11px', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>tips_and_updates</span>
            <span>Always tailor missing keywords before submitting.</span>
          </div>
        </div>
      </div>

      {/* Core Modules Launcher */}
      <div>
        <h3 style={{ fontSize: '1rem', fontWeight: '700', color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span className="material-symbols-outlined" style={{ color: '#38bdf8' }}>bolt</span> Core Workflows
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
          <div onClick={() => setActivePage('analyzer')} className="glass-card glass-card-interactive" style={{ padding: '1.5rem', borderRadius: '1rem' }}>
            <span className="material-symbols-outlined" style={{ color: '#38bdf8', fontSize: '2rem', marginBottom: '0.75rem' }}>analytics</span>
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: '#fff', marginBottom: '0.25rem' }}>ATS Match Analyzer</h4>
            <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>Analyze keywords against any job description, inspect subscores, and bridge gaps.</p>
          </div>

          <div onClick={() => setActivePage('builder')} className="glass-card glass-card-interactive" style={{ padding: '1.5rem', borderRadius: '1rem' }}>
            <span className="material-symbols-outlined" style={{ color: '#14b8a6', fontSize: '2rem', marginBottom: '0.75rem' }}>edit_note</span>
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: '#fff', marginBottom: '0.25rem' }}>Resume Builder &amp; Tailor</h4>
            <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>Structured multi-role builder with live split-screen preview and instant DOCX/PDF export.</p>
          </div>

          <div onClick={() => setActivePage('tracker')} className="glass-card glass-card-interactive" style={{ padding: '1.5rem', borderRadius: '1rem' }}>
            <span className="material-symbols-outlined" style={{ color: '#a855f7', fontSize: '2rem', marginBottom: '0.75rem' }}>work_history</span>
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: '#fff', marginBottom: '0.25rem' }}>Application Pipeline</h4>
            <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>Interactive Kanban board tracking applications across all recruitment stages.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
