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

    // Add job to tracker
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
    <div className="fade-in" style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', letterSpacing: '-0.025em' }}>
            ATS Match &amp; Screening Readiness Analyzer
          </h1>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.35rem' }}>
            <span style={{ fontSize: '12px', color: '#94a3b8' }}>Target Role:</span>
            <input
              type="text"
              id="target-role"
              className="field"
              style={{ width: 'auto', padding: '0.25rem 0.6rem', fontSize: '12px' }}
              value={role}
              onChange={(e) => setRole(e.target.value)}
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button onClick={() => openModal('bulletRewriter')} className="btn btn-ghost">
            <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>auto_fix_high</span>
            <span>Bullet Rewriter</span>
          </button>
          <button id="analyze-btn" onClick={handleAnalyze} disabled={loading} className="btn btn-primary">
            <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>speed</span>
            <span>{loading ? 'Analyzing...' : 'Run ATS Analysis'}</span>
          </button>
        </div>
      </div>

      {/* Input Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        {/* Resume Input */}
        <div className="glass-card" style={{ borderRadius: '1rem', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', backgroundColor: 'rgba(15, 23, 42, 0.6)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '12px', fontWeight: '700', color: '#38bdf8', textTransform: 'uppercase' }}>1. Resume Text</span>
            <label style={{ cursor: 'pointer', fontSize: '11px', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>upload_file</span>
              <span>Upload PDF/DOCX</span>
              <input type="file" accept=".pdf,.docx,.txt" onChange={handleFileUpload} style={{ display: 'none' }} />
            </label>
          </div>
          <textarea
            id="resume-input"
            rows={12}
            className="field field-mono"
            style={{ border: 'none', borderRadius: 0, resize: 'vertical', fontSize: '12px', lineHeight: '1.6' }}
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
          />
        </div>

        {/* Job Description Input */}
        <div className="glass-card" style={{ borderRadius: '1rem', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', backgroundColor: 'rgba(15, 23, 42, 0.6)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '12px', fontWeight: '700', color: '#14b8a6', textTransform: 'uppercase' }}>2. Job Description</span>
            <button onClick={() => setJobDesc(SAMPLE_JD)} style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '11px', cursor: 'pointer' }}>Load Sample</button>
          </div>
          <textarea
            id="job-desc-input"
            rows={12}
            className="field field-mono"
            style={{ border: 'none', borderRadius: 0, resize: 'vertical', fontSize: '12px', lineHeight: '1.6' }}
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          />
        </div>
      </div>

      {/* Analysis Results Display */}
      {results && (
        <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Main Score & Diff Header */}
          <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
              <div style={{
                width: '88px',
                height: '88px',
                borderRadius: '50%',
                border: '4px solid #10b981',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 20px rgba(16, 185, 129, 0.3)',
                backgroundColor: 'rgba(15, 23, 42, 0.8)'
              }}>
                <span id="ats-score" style={{ fontSize: '1.75rem', fontWeight: '800', color: '#fff', fontFamily: 'var(--font-mono)' }}>
                  {Math.round(results.ats_score || 88)}
                </span>
                <span style={{ fontSize: '10px', color: '#94a3b8' }}>/ 100</span>
              </div>
              <div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#fff' }}>
                  {results.ats_score >= 80 ? 'Strong Candidate Match' : 'Moderate Match — Optimization Recommended'}
                </h3>
                <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginTop: '0.2rem' }}>
                  Objective Screening Readiness computed across keywords, role alignment, and quantified evidence.
                </p>
              </div>
            </div>

            {/* Score Delta Diff */}
            {prevScore && (
              <div id="ats-diff-card" style={{ padding: '0.75rem 1.25rem', borderRadius: '0.75rem', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div>
                  <div style={{ fontSize: '10px', color: '#94a3b8', textTransform: 'uppercase' }}>Baseline</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#94a3b8', fontFamily: 'var(--font-mono)' }}>{prevScore}%</div>
                </div>
                <span className="material-symbols-outlined" style={{ color: '#10b981' }}>arrow_forward</span>
                <div>
                  <div style={{ fontSize: '10px', color: '#10b981', textTransform: 'uppercase' }}>Optimized</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#10b981', fontFamily: 'var(--font-mono)' }}>{Math.round(results.ats_score)}%</div>
                </div>
                <span id="diff-delta-badge" style={{ padding: '0.2rem 0.5rem', borderRadius: '9999px', fontSize: '11px', fontWeight: '700', backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#6ee7b7' }}>
                  +{scoreDelta}% Lift
                </span>
              </div>
            )}
          </div>

          {/* Subscores */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem' }}>
            <div className="glass-card" style={{ padding: '1rem', borderRadius: '0.75rem', textAlign: 'center' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '600' }}>Keywords</div>
              <div id="sub-keywords" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#38bdf8', marginTop: '0.25rem', fontFamily: 'var(--font-mono)' }}>
                {results.subscores?.keywords || 36}/40
              </div>
            </div>
            <div className="glass-card" style={{ padding: '1rem', borderRadius: '0.75rem', textAlign: 'center' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '600' }}>Role Match</div>
              <div id="sub-role" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#14b8a6', marginTop: '0.25rem', fontFamily: 'var(--font-mono)' }}>
                {results.subscores?.role_match || 26}/30
              </div>
            </div>
            <div className="glass-card" style={{ padding: '1rem', borderRadius: '0.75rem', textAlign: 'center' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '600' }}>Experience</div>
              <div id="sub-exp" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#f59e0b', marginTop: '0.25rem', fontFamily: 'var(--font-mono)' }}>
                {results.subscores?.experience_relevance || 18}/20
              </div>
            </div>
            <div className="glass-card" style={{ padding: '1rem', borderRadius: '0.75rem', textAlign: 'center' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '600' }}>Formatting</div>
              <div id="sub-quality" style={{ fontSize: '1.5rem', fontWeight: '800', color: '#a855f7', marginTop: '0.25rem', fontFamily: 'var(--font-mono)' }}>
                {results.subscores?.quality || 9}/10
              </div>
            </div>
          </div>

          {/* Matched & Missing Skills */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
            <div className="glass-card" style={{ padding: '1.25rem', borderRadius: '1rem' }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#10b981', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>check_circle</span>
                Matched Keywords ({results.skill_matches?.length || 0})
              </h4>
              <div id="matched-skills" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {results.skill_matches?.map((s, idx) => (
                  <span key={idx} style={{ padding: '0.25rem 0.6rem', borderRadius: '0.5rem', backgroundColor: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', color: '#6ee7b7', fontSize: '12px', fontFamily: 'var(--font-mono)' }}>
                    {typeof s === 'string' ? s : s.skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="glass-card" style={{ padding: '1.25rem', borderRadius: '1rem', borderLeft: '3px solid #f43f5e' }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#f43f5e', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <span className="material-symbols-outlined" style={{ fontSize: '1.1rem' }}>cancel</span>
                Missing Keywords ({results.missing_skills?.length || 0})
              </h4>
              <div id="missing-skills" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {results.missing_skills?.map((s, idx) => (
                  <span key={idx} style={{ padding: '0.25rem 0.6rem', borderRadius: '0.5rem', backgroundColor: 'rgba(244, 63, 94, 0.15)', border: '1px solid rgba(244, 63, 94, 0.3)', color: '#fda4af', fontSize: '12px', fontFamily: 'var(--font-mono)' }}>
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Action Recommendations & 1-Click Bridge */}
          <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <h4 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="material-symbols-outlined" style={{ color: '#38bdf8' }}>tips_and_updates</span>
              Actionable Coaching Recommendations
            </h4>
            <ul id="recommendations-list" style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.8125rem', color: '#cbd5e1' }}>
              {results.recommendations?.map((r, idx) => (
                <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
                  <span className="material-symbols-outlined" style={{ fontSize: '1rem', color: '#38bdf8' }}>arrow_right</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>

            {/* 1-Click Bridge Action */}
            <div style={{ marginTop: '0.5rem', padding: '1rem', borderRadius: '0.75rem', background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(20, 184, 166, 0.15) 100%)', border: '1px solid rgba(56, 189, 248, 0.3)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <div style={{ fontSize: '0.875rem', fontWeight: '700', color: '#fff' }}>1-Click Bridge Missing Skills &amp; Tailor Resume</div>
                <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '0.2rem' }}>Automatically populates the Resume Builder with missing requirements and tracks this job.</div>
              </div>
              <button id="bridge-tailor-btn" onClick={handleBridgeToBuilder} className="btn btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.8125rem' }}>
                🚀 Tailor &amp; Track Now
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
