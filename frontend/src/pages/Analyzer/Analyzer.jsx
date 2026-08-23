import React, { useState } from 'react';
import { analyzeResume, parseResumeFile } from '../../services/analyzeService';
import { useJobs } from '../../hooks/useJobs';
import { useToast } from '../../hooks/useToast';

const SAMPLE_RESUME = `ALEX MORGAN
alex.morgan@email.com • (555) 234-5678 • San Francisco, CA • linkedin.com/in/alexmorgan

PROFESSIONAL SUMMARY
Senior Software Engineer with 6+ years designing, scaling, and deploying distributed cloud architectures. Proven track record reducing system latency by 42% and leading cross-functional engineering teams in agile environments.

SKILLS
Languages: Python, TypeScript, JavaScript, SQL, Go
Frameworks & Libraries: React, Node.js, FastAPI, Django, Redux, Next.js
Databases: PostgreSQL, Redis, MongoDB, MySQL
Cloud & DevOps: Docker, Kubernetes, AWS (EC2, S3, RDS, Lambda), CI/CD Pipelines, Git, Linux
Architecture: Microservices, REST APIs, GraphQL, System Architecture, Distributed Systems

EXPERIENCE
Apex Cloud Solutions | Senior Software Engineer | 2022 - Present
- Architected high-throughput microservices using Python and FastAPI, handling 15M+ daily requests with 99.99% uptime.
- Engineered automated CI/CD deployment pipelines on AWS and Docker, slashing release cycles from 2 weeks to 35 minutes.
- Spearheaded database query optimizations in PostgreSQL and Redis, reducing p99 latency by 45%.
- Mentored 5 junior engineers and conducted 50+ technical code reviews to enforce code quality standards.

TechForge Labs | Software Engineer | 2019 - 2022
- Developed responsive web applications using React and TypeScript, boosting core user engagement metrics by 28%.
- Integrated secure OAuth2 and Stripe payment processing systems, processing $2.5M+ in annual transaction volume.
- Automated ETL data pipelines that synchronized real-time customer data across 4 distinct production services.

EDUCATION
B.S. in Computer Science — University of California, Berkeley (2015 - 2019)`;

const SAMPLE_JD = `Role: Senior Backend Engineer
Company: CloudScale Technologies

We are seeking a Senior Backend Engineer to build scalable microservices and distributed data pipelines.

Requirements:
- 5+ years building backend systems in Python, Go, or Node.js.
- Strong hands-on expertise with PostgreSQL, Redis, Docker, and Kubernetes.
- Experience architecting cloud infrastructure on AWS or GCP.
- Familiarity with CI/CD Pipelines, GraphQL, and high-availability System Architecture.
- Solid understanding of Unit Testing and microservice design patterns.`;

export function Analyzer({ setActivePage, openModal }) {
  const [role, setRole] = useState('Senior Backend Engineer');
  const [resumeText, setResumeText] = useState(SAMPLE_RESUME);
  const [jobDesc, setJobDesc] = useState(SAMPLE_JD);
  const [results, setResults] = useState(null);
  const [prevScore, setPrevScore] = useState(null);
  const [scoreDelta, setScoreDelta] = useState(0);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview'); // overview, matrix, coaching
  const [matrixFilter, setMatrixFilter] = useState('all'); // all, matched, missing

  const { addJob, setLastScore } = useJobs();
  const { showToast } = useToast();

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      showToast('Parsing resume document...', 'info');
      const data = await parseResumeFile(file);
      if (data.text) {
        setResumeText(data.text);
        showToast('Resume parsed successfully!', 'success');
      }
    } catch (err) {
      showToast(err.message || 'File upload error', 'error');
    }
  };

  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      showToast('Please provide resume text', 'error');
      return;
    }
    if (!jobDesc.trim()) {
      showToast('Please provide a target job description', 'error');
      return;
    }

    setLoading(true);
    try {
      const data = await analyzeResume(resumeText, jobDesc);
      
      const newScore = Math.round(data.ats_score || 88);
      if (results?.ats_score) {
        const delta = newScore - Math.round(results.ats_score);
        setPrevScore(Math.round(results.ats_score));
        setScoreDelta(delta);
      }
      
      setResults(data);
      setLastScore(newScore);
      showToast(`Analysis complete! Match Index: ${newScore}/100`, 'success');
    } catch (err) {
      showToast(err.message || 'Analysis error', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleBridgeToBuilder = () => {
    if (!results) return;

    addJob({
      company: 'Target Enterprise',
      position: role,
      score: Math.round(results.ats_score || 88),
      status: 'applied',
    });

    showToast(`🎯 Bridged missing skills to Builder & created application entry!`, 'success');
    setActivePage('builder');
  };

  const filteredMatches = results ? {
    matched: results.skill_matches || [],
    missing: results.missing_skills || []
  } : { matched: [], missing: [] };

  return (
    <div className="fade-in" style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      
      {/* 1. Header & Setup Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1.25rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
            <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--text-muted)' }}>Workspace</span>
            <span style={{ fontSize: '0.8125rem', color: 'var(--border-color)' }}>/</span>
            <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--apple-blue)' }}>ATS Analyzer</span>
          </div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: 'var(--text-primary)', letterSpacing: '-0.03em' }}>
            Resume &amp; Job Match Optimizer
          </h1>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
            Evaluate semantic fit, bridge critical keyword gaps, and generate tailored applications.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button onClick={() => openModal('bulletRewriter')} className="btn btn-ghost">
            <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>auto_fix_high</span>
            <span>STAR Bullet Coach</span>
          </button>
          <button id="analyze-btn" onClick={handleAnalyze} disabled={loading} className="btn btn-primary" style={{ padding: '0.625rem 1.25rem' }}>
            <span className="material-symbols-outlined" style={{ fontSize: '1.15rem' }}>speed</span>
            <span>{loading ? 'Analyzing Fit...' : 'Run Match Analysis'}</span>
          </button>
        </div>
      </div>

      {/* 2. Clean Input Dual-Panels */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem' }}>
        {/* Resume Input Card */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{ padding: '0.875rem 1.25rem', borderBottom: '1px solid var(--border-color)', backgroundColor: 'var(--bg-secondary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color: 'var(--apple-teal)' }}>description</span>
              <span style={{ fontSize: '0.8125rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.04em', color: 'var(--text-primary)' }}>1. Candidate Resume</span>
            </div>
            <label style={{ cursor: 'pointer', fontSize: '0.75rem', color: 'var(--apple-blue)', display: 'flex', alignItems: 'center', gap: '0.35rem', fontWeight: '600' }}>
              <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>upload_file</span>
              <span>Upload PDF/DOCX</span>
              <input type="file" accept=".pdf,.docx,.txt" onChange={handleFileUpload} style={{ display: 'none' }} />
            </label>
          </div>
          <textarea
            id="resume-input"
            rows={9}
            className="field field-mono"
            style={{ border: 'none', borderRadius: 0, resize: 'vertical', fontSize: '12px', lineHeight: '1.6', background: 'transparent', padding: '1rem 1.25rem' }}
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste resume text or upload document..."
          />
        </div>

        {/* Job Description Input Card */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{ padding: '0.875rem 1.25rem', borderBottom: '1px solid var(--border-color)', backgroundColor: 'var(--bg-secondary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color: 'var(--apple-green)' }}>work</span>
              <span style={{ fontSize: '0.8125rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.04em', color: 'var(--text-primary)' }}>2. Target Job Description</span>
            </div>
            <button onClick={() => setJobDesc(SAMPLE_JD)} style={{ background: 'none', border: 'none', color: 'var(--apple-blue)', fontSize: '0.75rem', cursor: 'pointer', fontWeight: '600' }}>
              Load Sample Role
            </button>
          </div>
          <textarea
            id="job-desc-input"
            rows={9}
            className="field field-mono"
            style={{ border: 'none', borderRadius: 0, resize: 'vertical', fontSize: '12px', lineHeight: '1.6', background: 'transparent', padding: '1rem 1.25rem' }}
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            placeholder="Paste target job description..."
          />
        </div>
      </div>

      {/* 3. Analysis Results with Progressive Disclosure */}
      {results && (
        <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          
          {/* A. Hero Bottom-Line Banner (The Bottom Line & Primary Action) */}
          <div className="glass-card" style={{
            padding: '1.75rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '1.5rem',
            background: 'linear-gradient(135deg, rgba(21, 25, 33, 0.9) 0%, rgba(10, 132, 255, 0.08) 100%)',
            border: '1px solid rgba(10, 132, 255, 0.25)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1.75rem' }}>
              {/* Radial Dial */}
              <div style={{
                width: '96px',
                height: '96px',
                borderRadius: '50%',
                background: `conic-gradient(var(--apple-blue) 0% ${Math.round(results.ats_score || 88)}%, rgba(255, 255, 255, 0.08) ${Math.round(results.ats_score || 88)}% 100%)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '9px',
                boxShadow: '0 0 24px var(--apple-blue-glow)'
              }}>
                <div style={{
                  width: '78px',
                  height: '78px',
                  borderRadius: '50%',
                  backgroundColor: 'var(--bg-secondary)',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <span id="ats-score" style={{ fontSize: '1.625rem', fontWeight: '800', fontFamily: 'var(--font-mono)', color: 'var(--text-primary)' }}>
                    {Math.round(results.ats_score || 88)}%
                  </span>
                  <span style={{ fontSize: '9px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Match</span>
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.35rem' }}>
                  <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--text-primary)' }}>
                    {results.ats_score >= 80 ? 'Strong Candidate Alignment' : 'Optimization Recommended'}
                  </h3>
                  <span className={`status-pill ${results.ats_score >= 80 ? 'status-found' : 'status-partial'}`}>
                    {results.ats_score >= 80 ? 'Tier 1 Readiness' : 'Gap Detected'}
                  </span>
                </div>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                  Found <strong>{results.skill_matches?.length || 0} matched competencies</strong> and <strong>{results.missing_skills?.length || 0} missing target keywords</strong>.
                </p>
              </div>
            </div>

            {/* Primary Action Button */}
            <button
              id="bridge-tailor-btn"
              onClick={handleBridgeToBuilder}
              className="btn btn-primary"
              style={{ padding: '0.75rem 1.5rem', fontSize: '0.9375rem', boxShadow: '0 4px 20px var(--apple-blue-glow)' }}
            >
              <span className="material-symbols-outlined" style={{ fontSize: '1.25rem' }}>auto_fix</span>
              <span>1-Click Bridge &amp; Tailor Resume</span>
            </button>
          </div>

          {/* B. Apple Segmented Controls (Progressive Disclosure Tabs) */}
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div className="segmented-control">
              <button
                className={`segmented-item ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                🎯 Overview &amp; Top Fixes
              </button>
              <button
                className={`segmented-item ${activeTab === 'matrix' ? 'active' : ''}`}
                onClick={() => setActiveTab('matrix')}
              >
                📋 Keyword Match Matrix ({results.skill_matches?.length || 0})
              </button>
              <button
                className={`segmented-item ${activeTab === 'coaching' ? 'active' : ''}`}
                onClick={() => setActiveTab('coaching')}
              >
                ✍️ STAR Evidence Coaching
              </button>
            </div>
          </div>

          {/* C. Tab 1: Overview & Top 3 High-Impact Fixes (Simple & Clean) */}
          {activeTab === 'overview' && (
            <div className="fade-in" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
              
              {/* Top 3 Critical Keyword Fixes */}
              <div className="glass-card" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.875rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                    Top Priority Keywords to Add
                  </span>
                  <span className="status-pill status-missing">High Impact</span>
                </div>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                  Adding these 3 keywords to your experience section will generate the largest ATS score lift:
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '0.25rem' }}>
                  {(results.missing_skills?.slice(0, 3) || ['System Architecture', 'CI/CD Pipelines', 'GraphQL']).map((skill, idx) => (
                    <div key={idx} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '0.75rem 1rem',
                      borderRadius: '0.75rem',
                      backgroundColor: 'var(--bg-secondary)',
                      border: '1px solid var(--border-color)'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
                        <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--apple-orange)' }}></span>
                        <span style={{ fontWeight: '600', fontSize: '0.875rem', fontFamily: 'var(--font-mono)' }}>{skill}</span>
                      </div>
                      <button
                        onClick={handleBridgeToBuilder}
                        className="btn btn-ghost"
                        style={{ padding: '0.3rem 0.65rem', fontSize: '11px', color: 'var(--apple-blue)' }}
                      >
                        + Inject
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Subscores Diagnostics */}
              <div className="glass-card" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1.125rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.875rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                    Scoring Breakdown
                  </span>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>4 Weighted Pillars</span>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                      <span style={{ color: 'var(--text-primary)' }}>Keywords Match (40%)</span>
                      <span id="sub-keywords" style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', color: 'var(--apple-blue)' }}>
                        {results.subscores?.keywords || 36}/40
                      </span>
                    </div>
                    <div className="meter-container">
                      <div className="meter-fill meter-blue" style={{ width: `${((results.subscores?.keywords || 36) / 40) * 100}%` }}></div>
                    </div>
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                      <span style={{ color: 'var(--text-primary)' }}>Role Relevance (30%)</span>
                      <span id="sub-role" style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', color: 'var(--apple-green)' }}>
                        {results.subscores?.role_match || 26}/30
                      </span>
                    </div>
                    <div className="meter-container">
                      <div className="meter-fill meter-emerald" style={{ width: `${((results.subscores?.role_match || 26) / 30) * 100}%` }}></div>
                    </div>
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                      <span style={{ color: 'var(--text-primary)' }}>Experience Impact (20%)</span>
                      <span id="sub-exp" style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', color: 'var(--apple-orange)' }}>
                        {results.subscores?.experience_relevance || 18}/20
                      </span>
                    </div>
                    <div className="meter-container">
                      <div className="meter-fill meter-amber" style={{ width: `${((results.subscores?.experience_relevance || 18) / 20) * 100}%` }}></div>
                    </div>
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                      <span style={{ color: 'var(--text-primary)' }}>Formatting &amp; Quality (10%)</span>
                      <span id="sub-quality" style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', color: 'var(--text-secondary)' }}>
                        {results.subscores?.quality || 9}/10
                      </span>
                    </div>
                    <div className="meter-container">
                      <div className="meter-fill meter-blue" style={{ width: `${((results.subscores?.quality || 9) / 10) * 100}%` }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* D. Tab 2: Linear Tabular Keyword Matrix (For Power Users) */}
          {activeTab === 'matrix' && (
            <div className="fade-in glass-card" style={{ overflow: 'hidden' }}>
              <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
                <span style={{ fontSize: '0.875rem', fontWeight: '700', color: 'var(--text-primary)' }}>Complete Keyword Coverage Matrix</span>
                
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    onClick={() => setMatrixFilter('all')}
                    className={`segmented-item ${matrixFilter === 'all' ? 'active' : ''}`}
                    style={{ fontSize: '11px', padding: '0.25rem 0.6rem' }}
                  >
                    All ({(results.skill_matches?.length || 0) + (results.missing_skills?.length || 0)})
                  </button>
                  <button
                    onClick={() => setMatrixFilter('missing')}
                    className={`segmented-item ${matrixFilter === 'missing' ? 'active' : ''}`}
                    style={{ fontSize: '11px', padding: '0.25rem 0.6rem', color: 'var(--apple-red)' }}
                  >
                    Missing Only ({results.missing_skills?.length || 0})
                  </button>
                </div>
              </div>

              <table className="matrix-table">
                <thead>
                  <tr>
                    <th className="matrix-th">Target Skill / Keyword</th>
                    <th className="matrix-th">Status</th>
                    <th className="matrix-th">Context</th>
                    <th className="matrix-th" style={{ textAlign: 'right' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {matrixFilter !== 'missing' && results.skill_matches?.map((s, idx) => {
                    const skillName = typeof s === 'string' ? s : s.skill;
                    return (
                      <tr key={`matched-${idx}`} className="matrix-tr">
                        <td className="matrix-td">
                          <span style={{ fontWeight: '600', fontFamily: 'var(--font-mono)' }}>{skillName}</span>
                        </td>
                        <td className="matrix-td">
                          <span className="status-pill status-found">Verified Match</span>
                        </td>
                        <td className="matrix-td">
                          <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>In Resume Experience</span>
                        </td>
                        <td className="matrix-td" style={{ textAlign: 'right' }}>
                          <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', color: 'var(--apple-green)' }}>check_circle</span>
                        </td>
                      </tr>
                    );
                  })}

                  {results.missing_skills?.map((s, idx) => (
                    <tr key={`missing-${idx}`} className="matrix-tr">
                      <td className="matrix-td">
                        <span style={{ fontWeight: '600', fontFamily: 'var(--font-mono)', color: 'var(--apple-red)' }}>{s}</span>
                      </td>
                      <td className="matrix-td">
                        <span className="status-pill status-missing">Missing</span>
                      </td>
                      <td className="matrix-td">
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Required by Job Description</span>
                      </td>
                      <td className="matrix-td" style={{ textAlign: 'right' }}>
                        <button
                          onClick={handleBridgeToBuilder}
                          className="btn btn-ghost"
                          style={{ padding: '0.25rem 0.625rem', fontSize: '11px', color: 'var(--apple-blue)' }}
                        >
                          + Inject
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* E. Tab 3: STAR Bullet Coaching (Honest Evidence Quality) */}
          {activeTab === 'coaching' && (
            <div className="fade-in glass-card" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                <div>
                  <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                    STAR Framework Evidence Coaching
                  </h4>
                  <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                    Convert passive statements into quantifiable, evidence-based accomplishments.
                  </p>
                </div>
                <button onClick={() => openModal('bulletRewriter')} className="btn btn-primary" style={{ fontSize: '0.8125rem' }}>
                  Launch Rewriter Studio
                </button>
              </div>

              {/* Side-by-side Example */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', padding: '1rem', borderRadius: '0.75rem', backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border-color)' }}>
                <div style={{ borderRight: '1px solid var(--border-subtle)', paddingRight: '1rem' }}>
                  <div style={{ fontSize: '11px', color: 'var(--apple-red)', fontWeight: '700', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                    Weak / Unquantified Phrasing
                  </div>
                  <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontStyle: 'italic' }}>
                    "Responsible for building backend services and assisting with database migrations."
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '11px', color: 'var(--apple-green)', fontWeight: '700', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                    Quantified STAR Phrasing
                  </div>
                  <div style={{ fontSize: '0.8125rem', color: 'var(--text-primary)', fontWeight: '600' }}>
                    "Architected 12 Python microservices handling 15M daily requests, slashing p99 latency by 45%."
                  </div>
                </div>
              </div>

              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {results.recommendations?.map((r, idx) => (
                  <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', padding: '0.875rem 1.125rem', borderRadius: '0.75rem', backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border-color)', fontSize: '0.8125rem', color: 'var(--text-primary)' }}>
                    <span className="material-symbols-outlined" style={{ fontSize: '1.15rem', color: 'var(--apple-blue)', flexShrink: 0 }}>tips_and_updates</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
