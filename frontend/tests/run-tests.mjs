import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const FRONTEND_DIR = join(__dirname, '..');
const DIST_INDEX = join(FRONTEND_DIR, 'dist', 'index.html');

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

console.log('ResumeGPT React Frontend Test Suite');
console.log('Path:', FRONTEND_DIR);
console.log('');

console.log('  Build & Production Assets:');

await test('Vite build completes and produces dist/index.html', () => {
  const res = spawnSync('npm', ['run', 'build'], { cwd: FRONTEND_DIR, encoding: 'utf8', shell: true });
  assert(res.status === 0, `npm run build failed:\n${res.stderr || res.stdout}`);
  assert(existsSync(DIST_INDEX), 'dist/index.html was not created by Vite');
});

await test('Production dist/index.html has valid root container & module assets', () => {
  const html = readFileSync(DIST_INDEX, 'utf8');
  assert(html.includes('id="root"'), 'dist/index.html missing #root div');
  assert(html.includes('<script type="module"'), 'dist/index.html missing module script bundle');
  assert(html.includes('/assets/index-'), 'dist/index.html missing hashed bundle asset links');
});

console.log('\n  Services & API Layer:');

await test('Services layer exports required API wrappers', async () => {
  const { analyzeResume, quickAnalyze, rewriteBullet } = await import('../src/services/analyzeService.js');
  assert(typeof analyzeResume === 'function', 'analyzeResume is not a function');
  assert(typeof quickAnalyze === 'function', 'quickAnalyze is not a function');
  assert(typeof rewriteBullet === 'function', 'rewriteBullet is not a function');

  const { login, register, forgotPassword, changePassword, deleteAccount } = await import('../src/services/authService.js');
  assert(typeof login === 'function', 'login is not a function');
  assert(typeof register === 'function', 'register is not a function');
  assert(typeof forgotPassword === 'function', 'forgotPassword is not a function');
  assert(typeof changePassword === 'function', 'changePassword is not a function');
  assert(typeof deleteAccount === 'function', 'deleteAccount is not a function');

  const { exportDocx, exportPdf, generateCoverLetter, INDUSTRY_PRESETS } = await import('../src/services/builderService.js');
  assert(typeof exportDocx === 'function', 'exportDocx is not a function');
  assert(typeof exportPdf === 'function', 'exportPdf is not a function');
  assert(typeof generateCoverLetter === 'function', 'generateCoverLetter is not a function');
  assert(INDUSTRY_PRESETS.software !== undefined, 'INDUSTRY_PRESETS missing software');
  assert(INDUSTRY_PRESETS.data !== undefined, 'INDUSTRY_PRESETS missing data');
  assert(INDUSTRY_PRESETS.product !== undefined, 'INDUSTRY_PRESETS missing product');

  const { initiateCheckout, openCustomerPortal } = await import('../src/services/billingService.js');
  assert(typeof initiateCheckout === 'function', 'initiateCheckout is not a function');
  assert(typeof openCustomerPortal === 'function', 'openCustomerPortal is not a function');
});

console.log('\n  Component File Structure & Integrity:');

await test('All React Feature Pages exist with non-empty content', () => {
  const pages = [
    'src/pages/Dashboard/Dashboard.jsx',
    'src/pages/Analyzer/Analyzer.jsx',
    'src/pages/Builder/ResumeBuilder.jsx',
    'src/pages/JobTracker/JobTracker.jsx',
    'src/pages/CoverLetter/CoverLetterStudio.jsx',
    'src/pages/InterviewPrep/InterviewPrep.jsx',
    'src/pages/AtsSimulator/AtsSimulator.jsx'
  ];

  for (const page of pages) {
    const p = join(FRONTEND_DIR, page);
    assert(existsSync(p), `Missing page: ${page}`);
    const content = readFileSync(p, 'utf8');
    assert(content.length > 100, `Page is empty: ${page}`);
  }
});

await test('All React Modals & Hooks exist with non-empty content', () => {
  const components = [
    'src/components/layout/Sidebar.jsx',
    'src/components/layout/Header.jsx',
    'src/components/layout/NotificationPanel.jsx',
    'src/components/modals/AuthModal.jsx',
    'src/components/modals/AccountModal.jsx',
    'src/components/modals/PricingModal.jsx',
    'src/components/modals/PrivacyModal.jsx',
    'src/components/modals/TermsModal.jsx',
    'src/components/modals/BulletRewriterModal.jsx',
    'src/components/modals/AutoTailorModal.jsx',
    'src/components/modals/AddJobModal.jsx',
    'src/hooks/useAuth.jsx',
    'src/hooks/useJobs.jsx',
    'src/hooks/useToast.jsx',
    'src/App.jsx',
    'src/main.jsx',
    'src/index.css'
  ];

  for (const comp of components) {
    const p = join(FRONTEND_DIR, comp);
    assert(existsSync(p), `Missing component: ${comp}`);
    const content = readFileSync(p, 'utf8');
    assert(content.length > 50, `Component is empty: ${comp}`);
  }
});

console.log('\n--------------------------------------------------');
console.log(`${PASS.length + FAIL.length} tests, ${PASS.length} passed, ${FAIL.length} failed`);
if (FAIL.length > 0) {
  console.error('\nFailures:\n' + FAIL.map(f => '  - ' + f).join('\n'));
  process.exit(1);
} else {
  console.log('All tests passed.');
}