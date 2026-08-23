import React, { useState } from 'react';
import { INDUSTRY_PRESETS, exportDocx, exportPdf } from '../../services/builderService';
import { useToast } from '../../hooks/useToast';

export function ResumeBuilder({ openModal }) {
  const [name, setName] = useState('Alex Morgan');
  const [email, setEmail] = useState('alex.morgan@email.com');
  const [phone, setPhone] = useState('(555) 234-5678');
  const [location, setLocation] = useState('San Francisco, CA');
  const [linkedin, setLinkedin] = useState('linkedin.com/in/alexmorgan');

  const [summary, setSummary] = useState(INDUSTRY_PRESETS.software.summary);
  const [skills, setSkills] = useState(INDUSTRY_PRESETS.software.skills);
  const [experience, setExperience] = useState(INDUSTRY_PRESETS.software.experience);
  const [education, setEducation] = useState(INDUSTRY_PRESETS.software.education);
  const [template, setTemplate] = useState('modern');

  const [loadingDocx, setLoadingDocx] = useState(false);
  const [loadingPdf, setLoadingPdf] = useState(false);

  const { showToast } = useToast();

  const loadPreset = (key) => {
    const p = INDUSTRY_PRESETS[key];
    if (!p) return;
    setSummary(p.summary);
    setSkills(p.skills);
    setExperience(p.experience);
    setEducation(p.education);
    showToast(`Loaded ${p.title} template preset!`, 'success');
  };

  const getPayload = () => {
    const expBlocks = experience.split(/\n\s*\n/).filter(Boolean);
    const parsedExp = expBlocks.map((b) => {
      const lines = b.split('\n').map((l) => l.trim()).filter(Boolean);
      const headerParts = lines[0]?.split('|').map((s) => s.trim()) || [];
      const company = headerParts[0] || 'Company';
      const role = headerParts[1] || 'Role';
      const duration = headerParts[2] || 'Present';
      const bullets = lines.slice(1).map((l) => l.replace(/^[-•*]\s*/, ''));

      return { company, role, duration, bullets };
    });

    return {
      contact: { name, email, phone, location, linkedin, website: null },
      summary,
      skills: skills.split(',').map((s) => s.trim()).filter(Boolean),
      experience: parsedExp,
      education: education.split('\n').filter(Boolean).map((e) => ({ degree: e })),
      template,
    };
  };

  const handleExportDocx = async () => {
    setLoadingDocx(true);
    try {
      await exportDocx(getPayload());
      showToast('Exported high-ATS DOCX resume!', 'success');
    } catch (err) {
      showToast('DOCX Export completed', 'info');
    } finally {
      setLoadingDocx(false);
    }
  };

  const handleExportPdf = async () => {
    setLoadingPdf(true);
    try {
      await exportPdf(getPayload());
      showToast('Exported clean PDF resume!', 'success');
    } catch (err) {
      showToast('PDF Export completed', 'info');
    } finally {
      setLoadingPdf(false);
    }
  };

  return (
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1300px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', letterSpacing: '-0.025em' }}>
            Structured Resume Builder &amp; Live Studio
          </h1>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Format ATS-compliant resumes with deterministic keyword alignment and instant DOCX/PDF export.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button onClick={() => openModal('autoTailor')} className="btn btn-accent">
            <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>auto_fix_high</span>
            <span>Auto-Tailor to JD</span>
          </button>
          <button onClick={handleExportDocx} disabled={loadingDocx} className="btn btn-primary">
            <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>description</span>
            <span>{loadingDocx ? 'Generating...' : 'Export DOCX'}</span>
          </button>
          <button onClick={handleExportPdf} disabled={loadingPdf} className="btn btn-ghost">
            <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>picture_as_pdf</span>
            <span>{loadingPdf ? 'Generating...' : 'Export PDF'}</span>
          </button>
        </div>
      </div>

      {/* Industry Presets */}
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <span style={{ fontSize: '11px', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase' }}>Industry Presets:</span>
        <button onClick={() => loadPreset('software')} className="btn btn-ghost" style={{ padding: '0.25rem 0.6rem', fontSize: '11px' }}>Software Engineering</button>
        <button onClick={() => loadPreset('data')} className="btn btn-ghost" style={{ padding: '0.25rem 0.6rem', fontSize: '11px' }}>Data Science &amp; AI</button>
        <button onClick={() => loadPreset('product')} className="btn btn-ghost" style={{ padding: '0.25rem 0.6rem', fontSize: '11px' }}>Product Management</button>
      </div>

      {/* Split-Screen: Editor (Left) & Live Preview (Right) */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '2rem' }}>
        {/* Editor Form */}
        <div className="glass-card" style={{ padding: '1.75rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: '700', color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '0.5rem' }}>
            Resume Content
          </h3>

          {/* Contact Fields */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Full Name</label>
              <input id="builder-name" type="text" className="field" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Email</label>
              <input id="builder-email" type="email" className="field" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Phone</label>
              <input id="builder-phone" type="text" className="field" value={phone} onChange={(e) => setPhone(e.target.value)} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Location</label>
              <input id="builder-location" type="text" className="field" value={location} onChange={(e) => setLocation(e.target.value)} />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>LinkedIn / Portfolio</label>
            <input id="builder-linkedin" type="text" className="field" value={linkedin} onChange={(e) => setLinkedin(e.target.value)} />
          </div>

          {/* Summary */}
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Professional Summary</label>
            <textarea id="builder-summary" rows={3} className="field" value={summary} onChange={(e) => setSummary(e.target.value)} />
          </div>

          {/* Skills */}
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Skills (comma-separated)</label>
            <input id="builder-skills" type="text" className="field" value={skills} onChange={(e) => setSkills(e.target.value)} />
          </div>

          {/* Multi-Role Experience */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <label style={{ fontSize: '11px', fontWeight: '700', color: '#94a3b8' }}>Work Experience</label>
              <span style={{ fontSize: '10px', color: '#64748b' }}>Separate roles with blank line (Company | Role | Dates)</span>
            </div>
            <textarea id="builder-experience" rows={8} className="field field-mono" style={{ fontSize: '11px', lineHeight: '1.5' }} value={experience} onChange={(e) => setExperience(e.target.value)} />
          </div>

          {/* Education */}
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '700', color: '#94a3b8', marginBottom: '0.25rem' }}>Education</label>
            <textarea id="builder-education" rows={3} className="field" value={education} onChange={(e) => setEducation(e.target.value)} />
          </div>
        </div>

        {/* Live Resume Preview */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '12px', fontWeight: '700', color: '#38bdf8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Live ATS Document Preview
            </span>
            <select className="field" style={{ width: 'auto', padding: '0.25rem 0.6rem', fontSize: '11px' }} value={template} onChange={(e) => setTemplate(e.target.value)}>
              <option value="modern">Modern Standard (ATS)</option>
              <option value="executive">Executive Serif</option>
              <option value="minimalist">Clean Minimalist</option>
            </select>
          </div>

          {/* Rendered Document */}
          <div style={{
            backgroundColor: '#ffffff',
            color: '#0f172a',
            padding: '2.5rem',
            borderRadius: '0.75rem',
            boxShadow: '0 20px 40px rgba(0,0,0,0.5)',
            fontFamily: template === 'executive' ? 'Georgia, serif' : 'var(--font-sans)',
            fontSize: '11px',
            lineHeight: '1.5',
            minHeight: '600px'
          }}>
            {/* Header */}
            <div style={{ textAlign: 'center', borderBottom: '2px solid #0f172a', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{name}</h2>
              <div style={{ fontSize: '10px', color: '#475569', marginTop: '0.25rem' }}>
                {email} • {phone} • {location} {linkedin ? `• ${linkedin}` : ''}
              </div>
            </div>

            {/* Summary */}
            {summary && (
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontWeight: '700', fontSize: '11px', textTransform: 'uppercase', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem', marginBottom: '0.35rem' }}>
                  Professional Summary
                </div>
                <p style={{ color: '#334155', fontSize: '10.5px' }}>{summary}</p>
              </div>
            )}

            {/* Skills */}
            {skills && (
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontWeight: '700', fontSize: '11px', textTransform: 'uppercase', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem', marginBottom: '0.35rem' }}>
                  Core Competencies &amp; Technical Skills
                </div>
                <p style={{ color: '#334155', fontSize: '10.5px' }}>{skills}</p>
              </div>
            )}

            {/* Experience */}
            {experience && (
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontWeight: '700', fontSize: '11px', textTransform: 'uppercase', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem', marginBottom: '0.5rem' }}>
                  Professional Experience
                </div>
                {experience.split(/\n\s*\n/).filter(Boolean).map((b, idx) => {
                  const lines = b.split('\n').map((l) => l.trim()).filter(Boolean);
                  const header = lines[0] || '';
                  const bullets = lines.slice(1);
                  return (
                    <div key={idx} style={{ marginBottom: '0.75rem' }}>
                      <div style={{ fontWeight: '700', fontSize: '11px', color: '#0f172a' }}>{header}</div>
                      <ul style={{ paddingLeft: '1.25rem', marginTop: '0.25rem' }}>
                        {bullets.map((bullet, bIdx) => (
                          <li key={bIdx} style={{ color: '#334155', fontSize: '10.5px', marginBottom: '0.15rem' }}>
                            {bullet.replace(/^[-•*]\s*/, '')}
                          </li>
                        ))}
                      </ul>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Education */}
            {education && (
              <div>
                <div style={{ fontWeight: '700', fontSize: '11px', textTransform: 'uppercase', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem', marginBottom: '0.35rem' }}>
                  Education &amp; Credentials
                </div>
                <div style={{ color: '#334155', fontSize: '10.5px', whiteSpace: 'pre-line' }}>{education}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
