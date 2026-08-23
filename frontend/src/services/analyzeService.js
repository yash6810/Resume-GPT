import { request, getApiBase, getAuthToken } from './api.js';

export async function analyzeResume(resumeText, jobDescription) {
  const res = await request('/analyze', {
    method: 'POST',
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(err.detail || 'Resume analysis failed');
  }

  return res.json();
}

export async function quickAnalyze(resumeText, jobDescription) {
  const res = await request('/analyze/quick', {
    method: 'POST',
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  });

  if (!res.ok) {
    throw new Error('Quick analysis failed');
  }

  return res.json();
}

export async function parseResumeFile(file) {
  const base = getApiBase();
  const token = getAuthToken();
  const formData = new FormData();
  formData.append('resume', file);
  formData.append('file', file);

  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${base}/parse`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload parse failed' }));
    throw new Error(err.detail || 'Resume parsing failed');
  }

  return res.json();
}

export async function rewriteBullet(bullet, targetKeywords) {
  const res = await request('/rewrite', {
    method: 'POST',
    body: JSON.stringify({
      bullet,
      target_keywords: targetKeywords || [],
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Rewrite failed' }));
    throw new Error(err.detail || 'Bullet rewrite failed');
  }

  return res.json();
}
