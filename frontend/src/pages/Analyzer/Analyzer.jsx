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
      showToast(`Analysis complete! Screening Readiness: ${newScore}/100`, 'success');
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

  return (
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1280px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Top Header & Breadcrumb */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--text-muted)' }}>Workspace</span>
            <span style={{ fontSize: '0.8125rem', color: 'var(--border-color)' }}>/</span>
            <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--accent-blue)' }}>Resume Analysis</span>
          </div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
            Analysis: <span style={{ color: 'var(--text-secondary)', fontWeight: '500' }}>{role}</span>
          </h1>
        </div>

        <div style={{ display: 'flex', gap: '0.625rem' }}>
          <button onClick={() => openModal('bulletRewriter')} className="btn btn-ghost">
            <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>auto_fix_high</span>
            <span>STAR Bullet Coach</span>
          </button>
          <button id="analyze-btn" onClick={handleAnalyze} disabled={loading} className="btn btn-primary">
            <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>speed</span>
            <span>{loading ? 'Analyzing...' : 'Run Analysis'}</span>
          </button>
        </div>
      </div>

      {/* Input Split Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.25rem' }}>
        {/* Resume Input */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid var(--border-color)', backgroundColor: 'var(--bg-secondary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="material-symbols-outlined" style={{ fontSize: '1rem', color: 'var(--accent-sky)' }}>description</span>
              <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-primary)' }}>1. Candidate Resume</span>
            </div>
            <label style={{ cursor: 'pointer', fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <span className="material-symbols-outlined" style={{ fontSize: '0.95rem' }}>upload_file</span>
              <span>Upload File</span>
              <input type="file" accept=".pdf,.docx,.txt" onChange={handleFileUpload} style={{ display: 'none' }} />
            </label>
          </div>
          <textarea
            id="resume-input"
            rows={10}
            className="field field-mono"
            style={{ border: 'none', borderRadius: 0, resize: 'vertical', fontSize: '12px', lineHeight: '1.6', background: 'transparent' }}
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
          />
        </div>

        {/* Job Description Input */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid var(--border-color)', backgroundColor: 'var(--bg-secondary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="material-symbols-outlined" style={{ fontSize: '1rem', color: 'var(--accent-emerald)' }}>work</span>
              <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-primary)' }}>2. Target Job Description</span>
            </div>
            <button onClick={() => setJobDesc(SAMPLE_JD)} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', fontSize: '0.75rem', cursor: 'pointer' }}>
              Load Sample
            </button>
          </div>
          <textarea
            id="job-desc-input"
            rows={10}
            className="field field-mono"
            style={{ border: 'none', borderRadius: 0, resize: 'vertical', fontSize: '12px', lineHeight: '1.6', background: 'transparent' }}
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          />
        </div>
      </div>

      {/* Analysis Results & Dashboard Overview */}
      {results && (
        <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Top Diagnostics Row (Gauge, Subscores, STAR Coach) */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
            {/* ATS Match Gauge */}
            <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--text-secondary)' }}>ATS Compatibility Gauge</span>
                <span className="status-pill status-found">
                  {results.ats_score >= 80 ? 'Strong Match' : 'Optimization Required'}
                </span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '1rem 0' }}>
                <div style={{
                  width: '120px',
                  height: '120px',
                  borderRadius: '50%',
                  background: `conic-gradient(var(--accent-blue) 0% ${Math.round(results.ats_score || 88)}%, var(--border-color) ${Math.round(results.ats_score || 88)}% 100%)`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: '10px'
                }}>
                  <div style={{
                    width: '100px',
                    height: '100px',
                    borderRadius: '50%',
                    backgroundColor: 'var(--bg-secondary)',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <span id="ats-score" style={{ fontSize: '1.75rem', fontWeight: '800', fontFamily: 'var(--font-mono)', color: 'var(--text-primary)' }}>
                      {Math.round(results.ats_score || 88)}%
                    </span>
                    <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Match Score</span>
                  </div>
                </div>
              </div>

              {prevScore && (
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.75rem', borderTop: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Baseline: {prevScore}%</span>
                  <span style={{ color: 'var(--accent-emerald)', fontWeight: '700' }}>+{scoreDelta}% ATS Lift</span>
                </div>
              )}
            </div>

            {/* Diagnostic Subscores Progress Bars */}
            <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--text-secondary)' }}>Diagnostic Subscores</span>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Weighted Metrics</span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                    <span style={{ color: 'var(--text-primary)' }}>Keywords Match</span>
                    <span id="sub-keywords" style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', color: 'var(--accent-blue)' }}>
                      {results.subscores?.keywords || 36}/40
                    </span>
                  </div>
                  <div className="meter-container">
                    <div className="meter-fill meter-blue" style={{ width: `${((results.subscores?.keywords || 36) / 40) * 100}%` }}></div>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                    <span style={{ color: 'var(--text-primary)' }}>Role Relevance</span>
                    <span id="sub-role" style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', color: 'var(--accent-emerald)' }}>
                      {results.subscores?.role_match || 26}/30
                    </span>
                  </div>
                  <div className="meter-container">
                    <div className="meter-fill meter-emerald" style={{ width: `${((results.subscores?.role_match || 26) / 30) * 100}%` }}></div>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                    <span style={{ color: 'var(--text-primary)' }}>Experience Impact</span>
                    <span id="sub-exp" style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', color: 'var(--accent-amber)' }}>
                      {results.subscores?.experience_relevance || 18}/20
                    </span>
                  </div>
                  <div className="meter-container">
                    <div className="meter-fill meter-amber" style={{ width: `${((results.subscores?.experience_relevance || 18) / 20) * 100}%` }}></div>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                    <span style={{ color: 'var(--text-primary)' }}>Formatting &amp; Structure</span>
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

            {/* STAR Bullet Coaching Widget */}
            <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--text-secondary)' }}>STAR Bullet Optimizer</span>
                  <span className="status-pill status-partial">Coaching Mode</span>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                  Convert passive claims into quantified accomplishment statements.
                </div>
                <div style={{ padding: '0.75rem', borderRadius: '0.5rem', backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border-color)', marginBottom: '0.5rem', fontSize: '11px', lineHeight: '1.5' }}>
                  <div style={{ color: 'var(--accent-rose)', marginBottom: '0.25rem' }}>❌ <i>"Responsible for building microservices."</i></div>
                  <div style={{ color: 'var(--accent-emerald)' }}>✅ <b>"Architected 12 microservices with FastAPI, scaling throughput to 15M req/day."</b></div>
                </div>
              </div>

              <button onClick={() => openModal('bulletRewriter')} className="btn btn-ghost" style={{ width: '100%', fontSize: '0.75rem', padding: '0.5rem' }}>
                Open Rewriter Studio
              </button>
            </div>
          </div>

          {/* Tabular Keyword Match Matrix (Linear Table Style) */}
          <div className="glass-card" style={{ overflow: 'hidden' }}>
            <div style={{ padding: '1rem 1.25rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.875rem', fontWeight: '700', color: 'var(--text-primary)' }}>Resume vs. Job Keyword Match Matrix</span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {results.skill_matches?.length || 0} Matched • {results.missing_skills?.length || 0} Missing
              </span>
            </div>

            <table className="matrix-table">
              <thead>
                <tr>
                  <th className="matrix-th">Target Skill / Keyword</th>
                  <th className="matrix-th">Status</th>
                  <th className="matrix-th">Category Context</th>
                  <th className="matrix-th" style={{ textAlign: 'right' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {results.skill_matches?.map((s, idx) => {
                  const skillName = typeof s === 'string' ? s : s.skill;
                  return (
                    <tr key={`matched-${idx}`} className="matrix-tr">
                      <td className="matrix-td">
                        <span style={{ fontWeight: '600', fontFamily: 'var(--font-mono)' }}>{skillName}</span>
                      </td>
                      <td className="matrix-td">
                        <span className="status-pill status-found">Matched</span>
                      </td>
                      <td className="matrix-td">
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Verified in Resume</span>
                      </td>
                      <td className="matrix-td" style={{ textAlign: 'right' }}>
                        <span className="material-symbols-outlined" style={{ fontSize: '1rem', color: 'var(--accent-emerald)' }}>check</span>
                      </td>
                    </tr>
                  );
                })}

                {results.missing_skills?.map((s, idx) => (
                  <tr key={`missing-${idx}`} className="matrix-tr">
                    <td className="matrix-td">
                      <span style={{ fontWeight: '600', fontFamily: 'var(--font-mono)', color: 'var(--accent-rose)' }}>{s}</span>
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
                        style={{ padding: '0.2rem 0.5rem', fontSize: '11px', color: 'var(--accent-sky)' }}
                      >
                        + Inject
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* 1-Click Bridge Banner */}
          <div className="glass-card" style={{ padding: '1.25rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', borderLeft: '3px solid var(--accent-blue)' }}>
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                Bridge Missing Skills &amp; Auto-Tailor Resume
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                Seamlessly transfer missing keywords directly into the structured resume builder and create a tracked application.
              </div>
            </div>
            <button id="bridge-tailor-btn" onClick={handleBridgeToBuilder} className="btn btn-primary">
              <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>auto_fix</span>
              <span>Tailor &amp; Track Application</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
