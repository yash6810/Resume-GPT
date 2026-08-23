import React, { useState } from 'react';
import { initiateCheckout } from '../../services/billingService';
import { useToast } from '../../hooks/useToast';

export function PricingModal({ isOpen, onClose }) {
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();

  if (!isOpen) return null;

  const handleUpgrade = async (plan) => {
    setLoading(true);
    try {
      await initiateCheckout(plan);
    } catch (err) {
      showToast(err.message || 'Billing service is initializing', 'info');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(10px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1rem'
    }}>
      <div className="glass-card" style={{
        width: '100%',
        maxWidth: '800px',
        borderRadius: '1.25rem',
        padding: '2.5rem',
        position: 'relative'
      }}>
        <button
          onClick={onClose}
          style={{ position: 'absolute', top: '1.25rem', right: '1.25rem', background: 'none', border: 'none', color: '#94a3b8', fontSize: '1.25rem', cursor: 'pointer' }}
        >
          ✕
        </button>

        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#f8fafc', letterSpacing: '-0.025em' }}>
            Elevate Your Job Search with <span style={{ color: '#38bdf8' }}>ResumeGPT Pro</span>
          </h2>
          <p style={{ fontSize: '0.875rem', color: '#94a3b8', marginTop: '0.5rem' }}>
            Land 3x more interview callbacks with unlimited ATS tailoring, AI bullet rewriting, and platform parser simulation.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          {/* Free Tier */}
          <div className="glass-card" style={{ padding: '1.5rem', borderRadius: '1rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#f8fafc' }}>Starter</div>
              <div style={{ fontSize: '2rem', fontWeight: '800', color: '#fff', margin: '0.75rem 0' }}>
                $0 <span style={{ fontSize: '0.875rem', color: '#64748b', fontWeight: '400' }}>/ forever</span>
              </div>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.875rem', color: '#94a3b8' }}>
                <li>✓ 3 ATS Resume Scans / month</li>
                <li>✓ Standard Keyword Matcher</li>
                <li>✓ Basic Resume Builder & Export</li>
                <li>✕ No Multi-Platform Simulators</li>
                <li>✕ No 1-Click Auto-Tailoring</li>
              </ul>
            </div>
            <button className="btn btn-ghost" onClick={onClose} style={{ marginTop: '1.5rem', width: '100%' }}>
              Current Plan
            </button>
          </div>

          {/* Pro Tier */}
          <div className="glass-card" style={{
            padding: '1.5rem',
            borderRadius: '1rem',
            border: '2px solid #38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.05)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            position: 'relative'
          }}>
            <div style={{
              position: 'absolute',
              top: '-12px',
              right: '1.5rem',
              backgroundColor: '#0284c7',
              color: '#fff',
              fontSize: '10px',
              fontWeight: '800',
              padding: '0.2rem 0.6rem',
              borderRadius: '9999px',
              letterSpacing: '0.05em'
            }}>
              MOST POPULAR
            </div>
            <div>
              <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#38bdf8' }}>ResumeGPT Pro</div>
              <div style={{ fontSize: '2rem', fontWeight: '800', color: '#fff', margin: '0.75rem 0' }}>
                $19 <span style={{ fontSize: '0.875rem', color: '#94a3b8', fontWeight: '400' }}>/ month</span>
              </div>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.875rem', color: '#e2e8f0' }}>
                <li>✓ <strong>Unlimited</strong> ATS Scans & Tailoring</li>
                <li>✓ <strong>1-Click Bridge & Auto-Tailor</strong> to any JD</li>
                <li>✓ Multi-Platform Simulators (Greenhouse, Lever, Workday)</li>
                <li>✓ Unlimited DOCX & PDF High-ATS Exports</li>
                <li>✓ Full Application Pipeline & Funnel Tracking</li>
              </ul>
            </div>
            <button
              disabled={loading}
              onClick={() => handleUpgrade('pro')}
              className="btn btn-primary"
              style={{ marginTop: '1.5rem', width: '100%', padding: '0.75rem' }}
            >
              {loading ? 'Connecting Stripe...' : 'Upgrade to Pro Now'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
