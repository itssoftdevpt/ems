import { useEffect, useState } from 'react';
import './App.css';

type TenantInfo = {
  id: string;
  name: string;
  logoUrl?: string;
};

type HealthStatus = { backend: 'up' | 'down'; message: string };

function App() {
  const [tenant, setTenant] = useState<TenantInfo | null>(null);
  const [status, setStatus] = useState<HealthStatus | null>(null);

  useEffect(() => {
    fetch('/api/tenant/context')
      .then((response) => (response.ok ? response.json() : Promise.reject()))
      .then(setTenant)
      .catch(() => setTenant(null));
  }, []);

  useEffect(() => {
    fetch('/api/health')
      .then((response) => (response.ok ? response.json() : Promise.reject()))
      .then(setStatus)
      .catch(() => setStatus({ backend: 'down', message: 'Backend unreachable' }));
  }, []);

  return (
    <div className="app">
      <header className="app__hero">
        <img className="app__logo" src={tenant?.logoUrl ?? '/favicon.svg'} alt={tenant?.name ?? 'EMS'} />
        <h1>Tenant Portal</h1>
        <p>Tenant aware interface for the tenant portal domain.</p>
      </header>
      <section className="app__card">
        <h2>Tenant context</h2>
        {tenant ? (
          <ul>
            <li><strong>ID:</strong> {tenant.id}</li>
            <li><strong>Name:</strong> {tenant.name}</li>
          </ul>
        ) : (
          <p className="muted">No tenant context loaded yet.</p>
        )}
      </section>
      <section className="app__card">
        <h2>Backend status</h2>
        {status ? (
          <p className={status.backend === 'up' ? 'status--ok' : 'status--error'}>
            {status.backend === 'up' ? 'Connected to EMS API' : 'API unavailable'} — {status.message}
          </p>
        ) : (
          <p className="muted">Checking connectivity…</p>
        )}
      </section>
    </div>
  );
}

export default App;
