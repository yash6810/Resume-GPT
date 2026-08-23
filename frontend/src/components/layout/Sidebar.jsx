import React from 'react';

export function Sidebar({ activePage, setActivePage, openModal }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: 'dashboard' },
    { id: 'analyzer', label: 'ATS Analyzer', icon: 'analytics' },
    { id: 'builder', label: 'Resume Builder', icon: 'edit_note' },
    { id: 'tracker', label: 'Application Pipeline', icon: 'work_history' },
    { id: 'coverletter', label: 'Cover Letter Studio', icon: 'history_edu' },
    { id: 'interview', label: 'Interview Prep', icon: 'psychology' },
    { id: 'simulator', label: 'ATS Simulators', icon: 'dns' },
  ];

  return (
    <aside style={{
      width: '260px',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderRight: '1px solid rgba(255, 255, 255, 0.08)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      padding: '1.25rem',
      flexShrink: 0
    }}>
      <div>
        {/* Brand Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem', paddingLeft: '0.5rem' }}>
          <div style={{
            width: '36px',
            height: '36px',
            background: 'linear-gradient(135deg, #0284c7 0%, #0d9488 100%)',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontWeight: '800',
            fontSize: '1.125rem',
            boxShadow: '0 4px 12px rgba(2, 132, 199, 0.4)'
          }}>
            R
          </div>
          <div>
            <div style={{ fontWeight: '800', fontSize: '1.125rem', letterSpacing: '-0.025em', color: '#fff' }}>
              Resume<span style={{ color: '#38bdf8' }}>GPT</span>
            </div>
            <div style={{ fontSize: '10px', color: '#94a3b8', fontWeight: '600', letterSpacing: '0.05em' }}>
              PRO ATS PLATFORM
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          {navItems.map((item) => {
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  width: '100%',
                  padding: '0.625rem 0.875rem',
                  borderRadius: '0.5rem',
                  fontSize: '0.875rem',
                  fontWeight: isActive ? '600' : '500',
                  color: isActive ? '#38bdf8' : '#94a3b8',
                  backgroundColor: isActive ? 'rgba(56, 189, 248, 0.12)' : 'transparent',
                  border: isActive ? '1px solid rgba(56, 189, 248, 0.25)' : '1px solid transparent',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.15s ease',
                  fontFamily: 'inherit'
                }}
              >
                <span className="material-symbols-outlined" style={{ fontSize: '1.25rem' }}>
                  {item.icon}
                </span>
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info & Legal */}
      <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.08)', paddingTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <button
          onClick={() => openModal('pricing')}
          style={{
            padding: '0.5rem',
            borderRadius: '0.5rem',
            background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(20, 184, 166, 0.15) 100%)',
            border: '1px solid rgba(56, 189, 248, 0.3)',
            color: '#38bdf8',
            fontSize: '11px',
            fontWeight: '700',
            cursor: 'pointer',
            textAlign: 'center'
          }}
        >
          ⚡ Upgrade to Pro · Unlimited Tailoring
        </button>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', fontSize: '11px', color: '#64748b' }}>
          <span onClick={() => openModal('privacy')} style={{ cursor: 'pointer', textDecoration: 'underline' }}>Privacy Policy</span>
          <span>·</span>
          <span onClick={() => openModal('terms')} style={{ cursor: 'pointer', textDecoration: 'underline' }}>Terms of Service</span>
        </div>
      </div>
    </aside>
  );
}
