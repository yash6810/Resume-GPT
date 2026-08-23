import { request } from './api.js';

export async function initiateCheckout(plan = 'pro') {
  const res = await request('/billing/create-checkout-session', {
    method: 'POST',
    body: JSON.stringify({ plan }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Billing service unavailable' }));
    throw new Error(err.detail || 'Could not create checkout session');
  }

  const data = await res.json();
  if (data.checkout_url) {
    window.location.href = data.checkout_url;
  }
  return data;
}

export async function openCustomerPortal() {
  const res = await request('/billing/customer-portal', {
    method: 'POST',
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Portal unavailable' }));
    throw new Error(err.detail || 'Could not open customer portal');
  }

  const data = await res.json();
  if (data.portal_url) {
    window.location.href = data.portal_url;
  }
  return data;
}

export async function getBillingStatus() {
  const res = await request('/billing/status', { method: 'GET' });
  if (!res.ok) return null;
  return res.json();
}
