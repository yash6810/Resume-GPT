import React, { useState } from 'react';

const SAMPLE_QUESTIONS = [
  {
    category: 'System Design & Architecture',
    question: 'How would you architect a distributed, high-throughput caching tier for a latency-critical application?',
    framework: 'STAR / Architecture Framework: 1. Functional & Non-Functional Requirements → 2. High-Level Diagram → 3. Cache Eviction (LRU/LFU) & Consistency (Write-through vs Write-back) → 4. Bottleneck mitigation.'
  },
  {
    category: 'Behavioral & Leadership',
    question: 'Tell me about a time when you had to resolve a severe production outage under high stakeholder pressure.',
    framework: 'STAR: Situation (incident context) → Task (root cause triage) → Action (orchestrated rollback, hotfix, post-mortem) → Result (reduced MTTR by 50% and instituted automated canary alerts).'
  },
  {
    category: 'Technical Deep-Dive',
    question: 'Explain how PostgreSQL index scans differ from sequential scans and how you optimize slow join queries.',
    framework: 'Technical Strategy: Discuss B-Tree indexes, EXPLAIN ANALYZE interpretation, vacuuming/statistics, partition pruning, and selective column indexing.'
  }
];

export function InterviewPrep() {
  const [role, setRole] = useState('Senior Software Engineer');

  return (
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1100px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', letterSpacing: '-0.025em' }}>
          Interview Preparation &amp; STAR Coaching
        </h1>
        <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginTop: '0.25rem' }}>
          Master technical and behavioral rounds tailored to your target job role.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {SAMPLE_QUESTIONS.map((q, idx) => (
          <div key={idx} className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: '#38bdf8', letterSpacing: '0.05em' }}>
                {q.category}
              </span>
              <span style={{ padding: '0.15rem 0.5rem', borderRadius: '9999px', backgroundColor: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8', fontSize: '10px', fontWeight: '700' }}>
                Question {idx + 1}
              </span>
            </div>

            <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#f8fafc' }}>
              {q.question}
            </h3>

            <div style={{ padding: '0.875rem', borderRadius: '0.5rem', backgroundColor: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255, 255, 255, 0.05)', fontSize: '0.8125rem', color: '#cbd5e1', lineHeight: '1.6' }}>
              <strong style={{ color: '#10b981' }}>Structured Answer Framework: </strong>
              {q.framework}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
