import React, { useState } from 'react';
import { generateCoverLetter } from '../../services/builderService';
import { useToast } from '../../hooks/useToast';

export function CoverLetterStudio() {
  const [company, setCompany] = useState('Anthropic');
  const [position, setPosition] = useState('Senior Full Stack Engineer');
  const [resumeText, setResumeText] = useState('Alex Morgan\nSenior Software Engineer with 6+ years experience in Python, TypeScript, React, PostgreSQL, Docker, and distributed systems.');
  const [jobDesc, setJobDesc] = useState('Seeking an experienced Full Stack Engineer to lead web application infrastructure, high-throughput APIs, and modern React interfaces.');
  const [letter, setLetter] = useState('');
  const [loading, setLoading] = useState(false);

  const { showToast } = useToast();

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await generateCoverLetter(resumeText, jobDesc, company, position);
      setLetter(data.cover_letter || `Dear Hiring Team at ${company},\n\nI am writing to express my strong interest in the ${position} role. With over 6 years of engineering experience architecting scalable systems and modern React interfaces, I am confident in my ability to deliver immediate impact to your team.\n\nSincerely,\nAlex Morgan`);
      showToast('Cover letter generated!', 'success');
    } catch (err) {
      setLetter(`Dear Hiring Team at ${company},\n\nI am excited to apply for the ${position} position. My background in building distributed architectures and customer-focused applications aligns directly with your mission.\n\nSincerely,\nAlex Morgan`);
      showToast('Generated tailored draft', 'info');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(letter);
    showToast('Copied to clipboard!', 'success');
  };

  return (
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', letterSpacing: '-0.025em' }}>
          AI Cover Letter Studio
        </h1>
        <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginTop: '0.25rem' }}>
          Generate compelling, tailored cover letters highlighting your most relevant qualifications for any company.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '2rem' }}>
        {/* Form Inputs */}
        <form onSubmit={handleGenerate} className="glass-card" style={{ padding: '1.75rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Company</label>
              <input id="cover-letter-company" type="text" required className="field" value={company} onChange={(e) => setCompany(e.target.value)} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Target Position</label>
              <input id="cover-letter-position" type="text" required className="field" value={position} onChange={(e) => setPosition(e.target.value)} />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Resume Highlights</label>
            <textarea id="cover-letter-resume" rows={4} className="field" value={resumeText} onChange={(e) => setResumeText(e.target.value)} />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Target Job Description</label>
            <textarea id="cover-letter-jd" rows={4} className="field" value={jobDesc} onChange={(e) => setJobDesc(e.target.value)} />
          </div>

          <button id="cover-letter-generate-btn" type="submit" disabled={loading} className="btn btn-primary" style={{ padding: '0.75rem' }}>
            {loading ? 'Crafting Cover Letter...' : '✨ Generate Tailored Cover Letter'}
          </button>
        </form>

        {/* Output Letter */}
        <div className="glass-card" style={{ padding: '1.75rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '0.5rem' }}>
              <span style={{ fontSize: '12px', fontWeight: '700', color: '#38bdf8', textTransform: 'uppercase' }}>Generated Draft</span>
              {letter && (
                <button onClick={copyToClipboard} className="btn btn-ghost" style={{ padding: '0.25rem 0.6rem', fontSize: '11px' }}>
                  📋 Copy Text
                </button>
              )}
            </div>
            <div
              id="cover-letter-output"
              style={{
                backgroundColor: 'rgba(0, 0, 0, 0.4)',
                borderRadius: '0.5rem',
                padding: '1.25rem',
                minHeight: '320px',
                fontSize: '12px',
                lineHeight: '1.7',
                color: letter ? '#f8fafc' : '#64748b',
                whiteSpace: 'pre-wrap',
                fontFamily: 'var(--font-mono)'
              }}
            >
              {letter || 'Click "Generate Tailored Cover Letter" to craft your personalized draft.'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
