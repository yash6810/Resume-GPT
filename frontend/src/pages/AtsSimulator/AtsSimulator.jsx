import React from 'react';

const SIMULATORS = [
  {
    name: 'Greenhouse Parsing Engine',
    badge: 'Standard Compatible',
    score: '96%',
    color: '#10b981',
    description: 'Header hierarchy and chronological work experience blocks parse with 100% field accuracy.',
    checklist: ['Contact details extract cleanly', 'Date formats (YYYY / Mon YYYY) recognized', 'Zero multi-column table collisions']
  },
  {
    name: 'Lever Candidate Indexer',
    badge: 'High Keyword Density',
    score: '92%',
    color: '#38bdf8',
    description: 'Keyword extraction recognizes 92% of target skills and categorizes technical proficiencies correctly.',
    checklist: ['Technical skills taxonomy mapped', 'Action verbs identified in experience', 'Clear section demarcation']
  },
  {
    name: 'Workday Enterprise Ingestion',
    badge: 'Strict Plain-Text Safe',
    score: '94%',
    color: '#a855f7',
    description: 'Structure complies with strict corporate parser constraints without text truncation.',
    checklist: ['Standard standard UTF-8 characters', 'Single-column linear text flow', 'Bullet symbols mapped cleanly']
  }
];

export function AtsSimulator() {
  return (
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', letterSpacing: '-0.025em' }}>
          Enterprise ATS Platform Simulators
        </h1>
        <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginTop: '0.25rem' }}>
          Simulate observable parsing behaviors, text extraction integrity, and keyword indexing across top ATS systems.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        {SIMULATORS.map((sim, idx) => (
          <div key={idx} className="glass-card" style={{ padding: '1.75rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <span style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: sim.color }}>
                  {sim.badge}
                </span>
                <span style={{ fontSize: '1.25rem', fontWeight: '800', color: sim.color, fontFamily: 'var(--font-mono)' }}>
                  {sim.score}
                </span>
              </div>

              <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#fff', marginBottom: '0.5rem' }}>
                {sim.name}
              </h3>
              <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: '1.5', marginBottom: '1rem' }}>
                {sim.description}
              </p>

              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem', fontSize: '12px', color: '#cbd5e1' }}>
                {sim.checklist.map((item, cIdx) => (
                  <li key={cIdx} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ color: '#10b981' }}>✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', fontSize: '11px', color: '#64748b' }}>
              Simulated parser model based on observable indexing rules.
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
