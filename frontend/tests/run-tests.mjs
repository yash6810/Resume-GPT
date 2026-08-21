import { readFileSync, writeFileSync } from 'node:fs';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const HTML_PATH = join(__dirname, '..', 'index.html');
const API_BASE = 'http://localhost:8000';

const PASS = [];
const FAIL = [];

async function test(label, fn) {
  try {
    await fn();
    PASS.push(label);
    console.log('  \x1b[32m✓\x1b[0m ' + label);
  } catch (err) {
    FAIL.push(label);
    console.error('  \x1b[31m✗ ' + label + '\x1b[0m');
    console.error('    ' + (err && err.stack ? err.stack : String(err)).split('\n').join('\n    '));
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg || 'Assertion failed');
}

// ---------------------------------------------------------------
// Inline script extraction + syntax checks
// ---------------------------------------------------------------
function extractInlineScripts(html) {
  const scripts = [];
  const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) scripts.push(m[1]);
  return scripts;
}

function nodeCheck(code) {
  const dir = mkdtempSync(join(tmpdir(), 'rgrept-'));
  try {
    const f = join(dir, 'inline.js');
    writeFileSync(f, code);
    const res = spawnSync('node', ['--check', f], { encoding: 'utf8' });
    if (res.status !== 0) throw new Error((res.stderr || '').trim() || 'node --check failed');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------
// jsdom helpers
// ---------------------------------------------------------------
const FAKE_ANALYZE = {
  ats_score: 82,
  subscores: { keywords: 30, role_match: 22, experience_relevance: 14, quality: 8 },
  skill_matches: [
    { skill: 'python', type: 'exact' },
    { skill: 'javascript', type: 'exact' },
    { skill: 'blockchain', type: 'semantic' }
  ],
  missing_skills: ['docker', 'aws'],
  recommendations: ['Add docker to your resume', 'Quantify achievements']
};

function makeFetch(routes, { failNetwork = false } = {}) {
  return async (url, opts = {}) => {
    if (failNetwork) throw new TypeError('Failed to fetch');
    const path = String(url).replace(API_BASE, '');
    const route = routes[path];
    if (route === undefined) {
      return new Response(JSON.stringify({ detail: 'not found: ' + path }), { status: 404, headers: { 'content-type': 'application/json' } });
    }
    if (typeof route === 'function') return route(opts);
    return new Response(JSON.stringify(route), { status: 200, headers: { 'content-type': 'application/json' } });
  };
}

async function loadApp(fetchMock, { seedStorage = true } = {}) {
  const html = readFileSync(HTML_PATH, 'utf8');
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', err => errors.push(err && err.detail ? err.detail : err));
  vc.on('error', (...args) => errors.push(...args));
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: vc,
    url: API_BASE + '/',
    beforeParse(window) {
      window.fetch = fetchMock;
      window.tailwind = {}; // stub the Tailwind CDN global used by the inline config
      if (seedStorage) {
        window.localStorage.setItem('resumegpt_jobs', JSON.stringify([{ id: 1, company: 'Acme', position: 'Engineer', status: 'applied', date: 'Jan 1', score: 80 }]));
      }
      if (typeof window.confirm !== 'function') window.confirm = () => true;
    }
  });
  await new Promise(r => setTimeout(r, 150));
  return { dom, window: dom.window, document: dom.window.document, errors };
}

// ---------------------------------------------------------------
// Suites
// ---------------------------------------------------------------
async function runSyntaxChecks() {
  console.log('\n  Syntax checks:');
  const html = readFileSync(HTML_PATH, 'utf8');
  const scripts = extractInlineScripts(html);

  await test('inline scripts present', () => {
    assert(scripts.length >= 2, 'expected at least 2 inline scripts (config + app)');
  });

  scripts.forEach((code, i) => {
    test('inline script #' + (i + 1) + ' passes node --check', () => nodeCheck(code));
  });
}

async function runJsdomTests() {
  console.log('\n  jsdom smoke tests:');

  await test('page loads without runtime errors', async () => {
    const { errors } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    assert(errors.length === 0, 'Runtime errors: ' + errors.map(e => (e && e.message) || e).join(' | '));
  });

  await test('dashboard renders jobs with counts and empty states', async () => {
    const { document } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    assert(document.getElementById('count-applied').textContent === '1', 'applied count should be 1');
    assert(document.getElementById('dash-applied').textContent === '1', 'dash applications = 1');
    assert(document.querySelectorAll('#col-applied .glass-card').length === 1, 'one applied card');
    assert(document.getElementById('col-offer').textContent.includes('No applications'), 'offer column shows empty state');
  });

  await test('showPage navigates between pages', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    window.showPage('analyzer');
    assert(document.getElementById('page-analyzer').classList.contains('active'), 'analyzer active');
    assert(!document.getElementById('page-dashboard').classList.contains('active'), 'dashboard inactive');
    window.showPage('builder');
    assert(document.getElementById('page-builder').classList.contains('active'), 'builder active');
  });

  await test('loadSampleResume fills the analyzer textarea', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    window.loadSampleResume();
    assert(document.getElementById('resume-input').value.includes('Alex Johnson'), 'sample resume loaded');
  });

  await test('runAnalysis maps /analyze response into the UI', async () => {
    const calls = [];
    const base = makeFetch({ '/health': { status: 'healthy' }, '/analyze': FAKE_ANALYZE });
    const wrapped = async (url, opts) => { calls.push({ url: String(url), opts }); return base(url, opts); };
    const { document, window } = await loadApp(wrapped);
    window.showPage('analyzer');
    window.loadSampleResume();
    document.getElementById('target-role').value = 'Senior Product Designer';
    await window.runAnalysis();
    await new Promise(r => setTimeout(r, 800)); // let the 600ms score count-up animation finish
    assert(parseInt(document.getElementById('ats-score').textContent, 10) === 82, 'ats-score renders 82');
    assert(document.getElementById('sub-keywords').textContent === '75%', 'keywords subscore = 75%');
    assert(document.getElementById('sub-exp').textContent === '70%', 'experience subscore = 70%');
    assert(document.getElementById('matched-skills').textContent.includes('python'), 'python matched pill');
    assert(!document.getElementById('matched-skills').textContent.includes('blockchain'), 'semantic match excluded from exact pills');
    assert(document.getElementById('missing-skills').textContent.includes('docker'), 'docker missing pill');
    assert(document.getElementById('recommendations-list').textContent.includes('Add docker'), 'recommendation shown');
    assert(document.getElementById('score-circle').style.stroke === '#16a34a', 'green ring for 82');
    const call = calls.find(c => c.url === API_BASE + '/analyze');
    assert(Boolean(call), 'fetch called /analyze at ' + API_BASE + ' (no /api prefix)');
    assert(JSON.parse(call.opts.body).resume_text.includes('Alex Johnson'), 'payload contains resume_text');
  });

  await test('runAnalysis falls back to demo results when the network fails', async () => {
    const { document, window } = await loadApp(makeFetch({}, { failNetwork: true }));
    window.showPage('analyzer');
    window.loadSampleResume();
    document.getElementById('target-role').value = 'Software Engineer';
    await window.runAnalysis();
    await new Promise(r => setTimeout(r, 150));
    const score = parseInt(document.getElementById('ats-score').textContent, 10);
    assert(!Number.isNaN(score) && score > 0, 'fallback produced a numeric score');
    assert(document.getElementById('api-dot-desktop').classList.contains('bg-amber-500'), 'offline indicator set');
  });

  await test('runAnalysis validates empty resume without calling the API', async () => {
    let analyzeCalls = 0;
    const base = makeFetch({ '/health': { status: 'healthy' } });
    const wrapped = async (url, opts) => { if (String(url).includes('/analyze')) analyzeCalls++; return base(url, opts); };
    const { document, window } = await loadApp(wrapped);
    window.showPage('analyzer');
    document.getElementById('resume-input').value = '';
    await window.runAnalysis();
    assert(analyzeCalls === 0, 'analyze endpoint not called on invalid input');
    assert(document.getElementById('resume-input').classList.contains('field-error'), 'resume input flagged');
    assert(document.querySelectorAll('#toast-container .toast').length >= 1, 'warning toast shown');
  });

  await test('interview prep maps categories and tips into the UI', async () => {
    const routes = {
      '/health': { status: 'healthy' },
      '/interview-prep': {
        technical: [{ question: 'Explain closures', tips: 'Talk about scope' }],
        behavioral: [{ question: 'Tell me about a conflict', tips: 'Use STAR' }],
        situational: [], company: [], provider: 'rule-based'
      }
    };
    const { document, window } = await loadApp(makeFetch(routes));
    window.showPage('aitools');
    window.openInterviewPrep();
    document.getElementById('prep-job-desc').value = 'Senior Engineer role at Acme';
    await window.generateQuestions();
    await new Promise(r => setTimeout(r, 80));
    const html = document.getElementById('prep-questions').innerHTML;
    assert(html.includes('Technical'), 'technical heading present');
    assert(html.includes('Explain closures'), 'technical question present');
    assert(html.includes('Tell me about a conflict'), 'behavioral question present');
    assert(html.includes('Use STAR'), 'tips rendered');
  });

  await test('salary calculation renders min/max/median and tips', async () => {
    const routes = {
      '/health': { status: 'healthy' },
      '/salary-insights': {
        min_salary: 95000, max_salary: 140000, median_salary: 112000, currency: 'USD',
        market_trend: 'growing', factors: ['Located in tech hub'], tips: ['Negotiate 10% higher']
      }
    };
    const { document, window } = await loadApp(makeFetch(routes));
    window.openSalaryCalc();
    document.getElementById('salary-title-input').value = 'Software Engineer';
    document.getElementById('salary-skills').value = 'Python, AWS';
    document.getElementById('salary-years').value = '4';
    await window.calculateSalary(new window.Event('submit'));
    await new Promise(r => setTimeout(r, 80));
    const html = document.getElementById('salary-result').innerHTML;
    assert(!document.getElementById('salary-result').classList.contains('hidden'), 'result visible');
    assert(html.includes('$95,000'), 'min salary shown');
    assert(html.includes('$140,000'), 'max salary shown');
    assert(html.includes('$112,000'), 'median shown');
    assert(html.includes('Tips'), 'tips section shown');
  });

  await test('add job persists to localStorage and renders in the correct column', async () => {
    const routes = { '/health': { status: 'healthy' }, '/auth/login': { access_token: 'tok', token_type: 'bearer' } };
    const { document, window } = await loadApp(makeFetch(routes), { seedStorage: false });
    window.showPage('tracker');
    document.getElementById('job-company').value = 'NewCo';
    document.getElementById('job-position').value = 'Backend Engineer';
    document.getElementById('job-description').value = 'Node + Postgres';
    document.getElementById('job-status').value = 'screening';
    document.getElementById('add-job-form').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
    await new Promise(r => setTimeout(r, 80));
    const stored = JSON.parse(window.localStorage.getItem('resumegpt_jobs') || '[]');
    assert(stored.length >= 1 && stored[0].company === 'NewCo', 'NewCo persisted as the newest job');
    assert(document.getElementById('col-screening').textContent.includes('NewCo'), 'card rendered in screening column');
    assert(document.getElementById('count-screening').textContent === '2', 'screening count includes seed + NewCo');
  });

  await test('add job validates required fields without persisting', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }), { seedStorage: false });
    window.showPage('tracker');
    document.getElementById('add-job-form').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
    assert(document.getElementById('job-company').classList.contains('field-error'), 'company flagged');
    assert(document.querySelectorAll('#toast-container .toast').length >= 1, 'warning toast shown');
    const stored = window.localStorage.getItem('resumegpt_jobs');
    assert(stored === null || JSON.parse(stored).length === 0, 'nothing persisted');
  });

  await test('modals open and Esc closes the top modal', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    window.showAddJobModal();
    assert(document.getElementById('modal-add-job').classList.contains('active'), 'add-job modal open');
    document.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    assert(!document.getElementById('modal-add-job').classList.contains('active'), 'modal closed on Esc');
  });

  await test('toasts render styled and auto-dismiss', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    window.showToast('Oops', 'error');
    window.showToast('Yay', 'success');
    await new Promise(r => setTimeout(r, 20));
    const toasts = document.querySelectorAll('#toast-container .toast');
    assert(toasts.length === 2, 'two toasts rendered');
    assert(toasts[0].className.includes('bg-red-600'), 'error toast styled');
    assert(toasts[1].className.includes('bg-green-600'), 'success toast styled');
    await new Promise(r => setTimeout(r, 4800));
    assert(document.querySelectorAll('#toast-container .toast').length === 0, 'toasts auto-dismissed');
  });

  await test('moveJob advances a card to the next stage', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }), { seedStorage: false });
    window.showPage('tracker');
    document.getElementById('job-company').value = 'MoveCo';
    document.getElementById('job-position').value = 'Dev';
    document.getElementById('job-status').value = 'applied';
    document.getElementById('add-job-form').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
    await new Promise(r => setTimeout(r, 50));
    const id = JSON.parse(window.localStorage.getItem('resumegpt_jobs'))[0].id;
    window.moveJob(id);
    assert(document.getElementById('col-screening').textContent.includes('MoveCo'), 'moved to screening');
  });

  await test('cover letter studio generates customized draft', async () => {
    const fakeCL = { cover_letter: 'Dear Hiring Team at Crossing Infotech,\n\nI am thrilled to apply for Data Analyst Intern...' };
    const { document, window } = await loadApp(makeFetch({
      '/health': { status: 'healthy' },
      '/cover-letter/generate': fakeCL
    }));
    window.openCoverLetterStudio();
    assert(document.getElementById('modal-cover-letter').classList.contains('active'), 'cover letter modal open');
    document.getElementById('cl-company').value = 'Crossing Infotech';
    document.getElementById('cl-position').value = 'Data Analyst Intern';
    document.getElementById('cl-job-desc').value = 'Looking for an intern skilled in Python, SQL, Excel, and Power BI';
    await window.generateCoverLetter();
    assert(!document.getElementById('cl-result-container').classList.contains('hidden'), 'result shown');
    assert(document.getElementById('cl-result-text').value.includes('Crossing Infotech'), 'contains company');
  });

  await test('auto-tailor updates builder summary and skills for target role', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    window.showPage('builder');
    document.getElementById('tailor-role').value = 'Data Analyst Intern';
    document.getElementById('tailor-jd').value = 'Requirements: Python, SQL, Excel, Power BI, Reporting, Data Analysis';
    window.executeAutoTailor();
    await new Promise(r => setTimeout(r, 450));
    const summary = document.getElementById('builder-summary').value;
    const skills = document.getElementById('builder-skills').value;
    assert(summary.includes('Data Analyst Intern'), 'summary tailored to role');
    assert(skills.includes('Python') || skills.includes('Sql') || skills.includes('Excel'), 'skills injected');
  });

  await test('ats diff card displays score delta and progress on consecutive analyses', async () => {
    let callCount = 0;
    const fetchStub = makeFetch({
      '/health': { status: 'healthy' },
      '/analyze': () => {
        callCount++;
        if (callCount === 1) {
          return new Response(JSON.stringify({
            ats_score: 60,
            subscores: { keywords: 20, role_match: 15, experience_relevance: 15, quality: 10 },
            skill_matches: [{ skill: 'python', type: 'exact' }],
            missing_skills: ['docker', 'kubernetes'],
            recommendations: ['Add docker']
          }), { status: 200, headers: { 'content-type': 'application/json' } });
        } else {
          return new Response(JSON.stringify({
            ats_score: 85,
            subscores: { keywords: 35, role_match: 25, experience_relevance: 15, quality: 10 },
            skill_matches: [{ skill: 'python', type: 'exact' }, { skill: 'docker', type: 'exact' }],
            missing_skills: ['kubernetes'],
            recommendations: ['Add kubernetes']
          }), { status: 200, headers: { 'content-type': 'application/json' } });
        }
      }
    });
    const { document, window } = await loadApp(fetchStub);
    window.loadSampleResume();
    await window.runAnalysis();
    assert(document.getElementById('ats-diff-card').classList.contains('hidden'), 'diff card hidden on first run');

    // Second run
    window.injectSkill('docker');
    await window.runAnalysis();
    assert(!document.getElementById('ats-diff-card').classList.contains('hidden'), 'diff card visible on second run');
    assert(document.getElementById('diff-delta-badge').textContent.includes('+25%'), 'diff delta shows lift');
    assert(document.getElementById('diff-prev-score').textContent === '60%', 'previous score is 60%');
    assert(document.getElementById('diff-curr-score').textContent === '85%', 'current score is 85%');
  });

  await test('checkUrlParams extracts role and description from URL query parameters', async () => {
    const { document, window } = await loadApp(makeFetch({ '/health': { status: 'healthy' } }));
    // Simulate query param values
    window.history.pushState({}, '', '?role=Staff+Frontend+Engineer&desc=Expertise+in+Vue+and+TypeScript');
    window.checkUrlParams();
    assert(document.getElementById('target-role').value === 'Staff Frontend Engineer', 'role extracted');
    assert(document.getElementById('job-desc-input').value.includes('Vue'), 'job desc extracted');
  });
}

// ---------------------------------------------------------------
// Runner
// ---------------------------------------------------------------
console.log('ResumeGPT frontend tests');
console.log('HTML: ' + HTML_PATH);

(async () => {
  await runSyntaxChecks();
  await runJsdomTests();

  const total = PASS.length + FAIL.length;
  console.log('\n' + '-'.repeat(50));
  console.log(`${total} tests, ${PASS.length} passed, ${FAIL.length} failed`);
  if (FAIL.length) {
    console.error('\nFailed tests:');
    FAIL.forEach(f => console.error('  - ' + f));
    process.exitCode = 1;
  } else {
    console.log('All tests passed.');
  }
})();