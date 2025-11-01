import { Component } from 'react';

type TenantInfo = {
  id: string;
  name: string;
  logoUrl?: string;
};

type HealthStatus = { backend: 'up' | 'down'; message: string };

type AppState = {
  tenant: TenantInfo | null;
  status: HealthStatus | null;
};

class App extends Component<Record<string, never>, AppState> {
  state: AppState = {
    tenant: null,
    status: null
  };

  componentDidMount(): void {
    this.loadTenantContext();
    this.loadHealthStatus();
  }

  private loadTenantContext = (): void => {
    fetch('/api/tenant/context')
      .then((response) => (response.ok ? response.json() : Promise.reject()))
      .then((tenant: TenantInfo) => this.setState({ tenant }))
      .catch(() => this.setState({ tenant: null }));
  };

  private loadHealthStatus = (): void => {
    fetch('/api/health')
      .then((response) => (response.ok ? response.json() : Promise.reject()))
      .then((status: HealthStatus) => this.setState({ status }))
      .catch(() =>
        this.setState({
          status: { backend: 'down', message: 'Backend unreachable' }
        })
      );
  };

  render(): JSX.Element {
    const { tenant, status } = this.state;
    const statusClass = status?.backend === 'up' ? 'text-emerald-600' : 'text-rose-600';

    return (
      <div className="flex min-h-screen flex-col items-center bg-gradient-to-br from-slate-50 via-white to-indigo-50 px-4 py-10 text-slate-900 md:py-16">
        <header className="mb-10 max-w-3xl text-center">
          <img
            className="mx-auto mb-4 h-20 w-20 rounded-full border border-indigo-100 bg-white object-contain p-2 shadow-sm"
            src={tenant?.logoUrl ?? '/favicon.svg'}
            alt={tenant?.name ?? 'EMS'}
          />
          <h1 className="text-3xl font-semibold tracking-tight text-slate-900 md:text-4xl">Student Experience</h1>
          <p className="mt-3 text-base text-slate-600 md:text-lg">Tenant aware interface for the student experience domain.</p>
        </header>
        <section className="mb-6 w-full max-w-3xl rounded-2xl bg-white p-8 shadow-xl ring-1 ring-slate-100">
          <h2 className="text-lg font-semibold text-slate-900">Tenant context</h2>
          {tenant ? (
            <ul className="mt-3 space-y-2 text-left text-sm text-slate-700">
              <li>
                <span className="font-medium text-slate-900">ID:</span> {' '}
                {tenant.id}
              </li>
              <li>
                <span className="font-medium text-slate-900">Name:</span> {' '}
                {tenant.name}
              </li>
            </ul>
          ) : (
            <p className="mt-3 text-sm text-slate-500">No tenant context loaded yet.</p>
          )}
        </section>
        <section className="w-full max-w-3xl rounded-2xl bg-white p-8 shadow-xl ring-1 ring-slate-100">
          <h2 className="text-lg font-semibold text-slate-900">Backend status</h2>
          {status ? (
            <p className={`mt-3 text-sm font-medium ${statusClass}`}>
              {status.backend === 'up' ? 'Connected to EMS API' : 'API unavailable'} — {status.message}
            </p>
          ) : (
            <p className="mt-3 text-sm text-slate-500">Checking connectivity…</p>
          )}
        </section>
      </div>
    );
  }
}

export default App;
