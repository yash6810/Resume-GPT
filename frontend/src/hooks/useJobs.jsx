import React, { createContext, useContext, useState, useEffect } from 'react';

const STORAGE_JOBS = 'resumegpt_jobs';

const INITIAL_DEMO_JOBS = [
  { id: 1, company: 'Acme Corp', position: 'Senior Frontend Engineer', status: 'applied', date: 'Jan 12, 2024', score: 88 },
  { id: 2, company: 'Globex', position: 'UX/UI Designer', status: 'applied', date: 'Jan 15, 2024', score: 64 },
  { id: 3, company: 'Initech', position: 'Product Manager', status: 'screening', date: 'Jan 18, 2024', score: 92 },
  { id: 4, company: 'Soylent Corp', position: 'UI Engineer', status: 'interview', date: 'Jan 20, 2024', score: 85 },
  { id: 5, company: 'Massive Dynamic', position: 'Lead Designer', status: 'offer', date: 'Jan 22, 2024', score: 98 },
];

const STAGE_ORDER = ['applied', 'screening', 'interview', 'offer'];

const JobsContext = createContext(null);

export function JobsProvider({ children }) {
  const [jobs, setJobs] = useState(() => {
    try {
      const raw = localStorage.getItem(STORAGE_JOBS);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.warn('Jobs localStorage error:', e);
    }
    return INITIAL_DEMO_JOBS;
  });

  const [lastScore, setLastScore] = useState(null);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_JOBS, JSON.stringify(jobs));
    } catch (e) {
      console.warn('Could not save jobs:', e);
    }
  }, [jobs]);

  const addJob = (job) => {
    const newEntry = {
      id: Date.now(),
      date: 'Just now',
      score: lastScore || 88,
      status: 'applied',
      ...job,
    };
    setJobs((prev) => [newEntry, ...prev]);
    return newEntry;
  };

  const deleteJob = (id) => {
    setJobs((prev) => prev.filter((j) => j.id !== id));
  };

  const moveJob = (id) => {
    setJobs((prev) =>
      prev.map((j) => {
        if (j.id === id) {
          const currentIndex = STAGE_ORDER.indexOf(j.status);
          const nextStage = STAGE_ORDER[Math.min(currentIndex + 1, STAGE_ORDER.length - 1)];
          return { ...j, status: nextStage };
        }
        return j;
      })
    );
  };

  const setJobStatus = (id, newStatus) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === id ? { ...j, status: newStatus } : j))
    );
  };

  // Funnel & Dashboard metrics
  const appliedCount = jobs.filter((j) => j.status === 'applied').length;
  const screeningCount = jobs.filter((j) => j.status === 'screening').length;
  const interviewCount = jobs.filter((j) => j.status === 'interview').length;
  const offerCount = jobs.filter((j) => j.status === 'offer').length;
  const totalJobs = jobs.length;
  const callbacks = screeningCount + interviewCount + offerCount;
  const callbackRate = totalJobs > 0 ? Math.round((callbacks / totalJobs) * 100) : 0;

  return (
    <JobsContext.Provider
      value={{
        jobs,
        addJob,
        deleteJob,
        moveJob,
        setJobStatus,
        lastScore,
        setLastScore,
        metrics: {
          totalJobs,
          appliedCount,
          screeningCount,
          interviewCount,
          offerCount,
          callbackRate,
        },
      }}
    >
      {children}
    </JobsContext.Provider>
  );
}

export function useJobs() {
  const ctx = useContext(JobsContext);
  if (!ctx) throw new Error('useJobs must be used within a JobsProvider');
  return ctx;
}
