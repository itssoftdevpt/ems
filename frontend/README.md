# EMS Frontend Workspaces

The EMS frontend is organized as a set of focused Vite + React + TypeScript workspaces. Each domain-specific SPA is co-located with the backend so developers can run both stacks side-by-side.

## Getting started

Install dependencies for a module by changing into its directory and running `npm install`. Alternatively, enable npm workspaces from this folder to install everything at once.

## Available modules

- `tenant-portal` – shared login shell that hydrates tenant branding.
- `students` – student and guardian experiences.
- `academics` – curriculum, timetable, and grading workflows.
- `hr` – staff administration workspace.
- `fees` – finance and billing flows.
- `communications` – announcements and messaging surfaces.
- `calendars` – event planning and academic calendar tooling.
- `reporting` – dashboards and analytics explorer.
