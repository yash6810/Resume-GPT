import React, { useState } from 'react';
import { ToastProvider } from './hooks/useToast';
import { AuthProvider } from './hooks/useAuth';
import { JobsProvider } from './hooks/useJobs';
import { ThemeProvider } from './hooks/useTheme';

import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { NotificationPanel } from './components/layout/NotificationPanel';

import { Dashboard } from './pages/Dashboard/Dashboard';
import { Analyzer } from './pages/Analyzer/Analyzer';
import { ResumeBuilder } from './pages/Builder/ResumeBuilder';
import { JobTracker } from './pages/JobTracker/JobTracker';
import { CoverLetterStudio } from './pages/CoverLetter/CoverLetterStudio';
import { InterviewPrep } from './pages/InterviewPrep/InterviewPrep';
import { AtsSimulator } from './pages/AtsSimulator/AtsSimulator';

import { AuthModal } from './components/modals/AuthModal';
import { AccountModal } from './components/modals/AccountModal';
import { PricingModal } from './components/modals/PricingModal';
import { PrivacyModal } from './components/modals/PrivacyModal';
import { TermsModal } from './components/modals/TermsModal';
import { BulletRewriterModal } from './components/modals/BulletRewriterModal';
import { AutoTailorModal } from './components/modals/AutoTailorModal';
import { AddJobModal } from './components/modals/AddJobModal';

export function AppContent() {
  const [activePage, setActivePage] = useState('dashboard');
  const [activeModal, setActiveModal] = useState(null);
  const [modalParam, setModalParam] = useState(null);
  const [notifsOpen, setNotifsOpen] = useState(false);

  const openModal = (modalName, param = null) => {
    setActiveModal(modalName);
    setModalParam(param);
  };

  const closeModal = () => {
    setActiveModal(null);
    setModalParam(null);
  };

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', overflow: 'hidden', backgroundColor: 'var(--bg-primary)' }}>
      {/* Sidebar */}
      <Sidebar activePage={activePage} setActivePage={setActivePage} openModal={openModal} />

      {/* Main Content Area */}
      <div style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden', position: 'relative' }}>
        <Header openModal={openModal} toggleNotifs={() => setNotifsOpen(!notifsOpen)} />
        <NotificationPanel isOpen={notifsOpen} onClose={() => setNotifsOpen(false)} />

        {/* Scrollable Page Body */}
        <main style={{ flex: 1, overflowY: 'auto' }}>
          {activePage === 'dashboard' && <Dashboard setActivePage={setActivePage} openModal={openModal} />}
          {activePage === 'analyzer' && <Analyzer setActivePage={setActivePage} openModal={openModal} />}
          {activePage === 'builder' && <ResumeBuilder openModal={openModal} />}
          {activePage === 'tracker' && <JobTracker openModal={openModal} />}
          {activePage === 'coverletter' && <CoverLetterStudio />}
          {activePage === 'interview' && <InterviewPrep />}
          {activePage === 'simulator' && <AtsSimulator />}
        </main>
      </div>

      {/* Modals */}
      <AuthModal isOpen={activeModal === 'auth'} onClose={closeModal} initialTab={modalParam || 'login'} />
      <AccountModal isOpen={activeModal === 'account'} onClose={closeModal} />
      <PricingModal isOpen={activeModal === 'pricing'} onClose={closeModal} />
      <PrivacyModal isOpen={activeModal === 'privacy'} onClose={closeModal} />
      <TermsModal isOpen={activeModal === 'terms'} onClose={closeModal} />
      <BulletRewriterModal isOpen={activeModal === 'bulletRewriter'} onClose={closeModal} />
      <AutoTailorModal
        isOpen={activeModal === 'autoTailor'}
        onClose={closeModal}
        onApplyTailoring={(role, jd) => {
          console.log('Applied auto-tailoring for', role);
        }}
      />
      <AddJobModal isOpen={activeModal === 'addJob'} onClose={closeModal} />
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <AuthProvider>
          <JobsProvider>
            <AppContent />
          </JobsProvider>
        </AuthProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}
