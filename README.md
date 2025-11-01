# EMS Multi-tenant SaaS Platform

This repository contains a Django-based, schema-level multi-tenant implementation for a national education management system. It is structured around `django-tenants` and targets a SaaS deployment where each subscribing school receives an isolated PostgreSQL schema while sharing the same application codebase.

## Key Features

- **Tenant Provisioning** – Public schema hosts management groups, administrative hierarchies (national → region → district → circuit → school), tenant records, and schema-aware domains.
- **Role-aware Authentication** – Custom user model with parent, student, teaching staff, non-teaching staff, and administrator roles. DRF token authentication powers staff/student portals.
- **Tenant Customisation** – School profiles, branding options, and module toggles per tenant support logo uploads, themes, and feature gating.
- **Student Management** – Admissions, guardianship links, attendance, records, transfers, and document storage with RBAC enforced at the API layer.
- **Academic Management** – Curricula, sections, academic levels, classrooms, subject allocations, lesson plans, and syllabus tracking for shared curricula.
- **Human Resources** – Staff profiles, transfers, performance tracking, certifications, leave workflows, attendance, and substitute assignments.
- **Fees & Finance** – Fee structures (shared and independent), schedules, invoicing, payments, scholarships, discount policies, and bank accounts tied to jurisdictions.
- **Communications & Calendar** – Announcements, secure messaging threads, notification preferences, calendar events, academic calendars, and global holidays.
- **Reporting & Analytics** – Cross-tenant aggregation utilities for student and staff counts plus snapshot storage for repeatable dashboards.
- **Student Transfers** – Public-schema workflow to co-ordinate inter-tenant transfers with confirmation code validation.

## Technology Stack

- Python 3.11+
- Django 4.2
- Django Rest Framework
- django-tenants (PostgreSQL backend)

## Local Development

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure environment variables (see `.env.example`) and ensure PostgreSQL is available. The project expects the `django_tenants.postgresql_backend` engine.

3. Run database migrations:

   ```bash
   python manage.py migrate_schemas --shared
   python manage.py migrate_schemas --tenant
   ```

4. Create the public domain/tenant entries using the tenancy APIs or Django admin.

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Frontend workspaces

The repository also ships with a `frontend/` directory that hosts independent Vite + React + TypeScript single-page applications for each major EMS module (tenant portal, students, academics, HR, fees, communications, calendars, and reporting). Every workspace has its own `package.json`, TypeScript configuration, and development server so teams can iterate in parallel.

To work with a specific module:

```bash
cd frontend/<module>
npm install
npm run dev
```

Each workspace proxies API calls under `/api` to the Django backend running on `http://localhost:8000`, allowing the frontend and backend stacks to run side-by-side.

## API Overview

The project exposes versionless REST endpoints grouped by responsibility:

- `api/tenancy/` – Tenant provisioning, administrative hierarchies, transfer workflows, and aggregated metrics.
- `api/auth/` – Token-based login (`POST /login/`) and profile inspection (`GET /me/`).
- `api/tenant/` – Tenant-specific branding, module toggles, and school profile management.
- `api/students/` – Student CRUD, portal summaries, attendance, and document management.
- `api/academics/` – Curricula, subjects, classrooms, lesson plans, and syllabus progress.
- `api/hr/` – Staff administration, transfers, leave, attendance, and performance.
- `api/fees/` – Fee structures, schedules, invoices, payments, and scholarships.
- `api/communications/` – Announcements, secure messaging, notification preferences, and calendar events.
- `api/calendars/` – Academic calendars, terms, holidays, and event bookings.
- `api/reporting/` – Saved report snapshots and real-time multi-tenant metrics.

All endpoints require authentication unless otherwise stated (e.g., tenant branding lookup). Role-based permission checks are defined in each module to honour the jurisdictional requirements described in the specification.

## Testing

Execute the Django test suite (shared schema) with:

```bash
python manage.py test
```

> **Note:** Running the tests requires PostgreSQL and all Python dependencies installed locally.
