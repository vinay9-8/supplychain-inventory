# Project Development Plan

This repository is being developed in phases so that each part can be validated before the next one is built.

## Phase 1: Repository inspection and setup
- Inspect the existing repo and confirm the current state.
- Validate local tooling and dependencies.
- Create the project structure and base configuration files.
- Document the project roadmap and environment requirements.

## Phase 2: Database models and relationships
- Create SQLAlchemy models for SKUs, locations, inventory, suppliers, demand, purchase orders, production plans, shortages, and mitigation options.
- Document entity relationships and lifecycle fields.

## Phase 3: Synthetic data generation
- Generate realistic supply chain datasets for SKUs, locations, suppliers, production, inventory, and demand.
- Use fixed seed 20261022 and deterministic IDs.

## Phase 4: Validation and ground truth
- Validate synthetic data quality and define checks for business rules.
- Store ground-truth validation results and exception logs.

## Phase 5: Demand forecasting
- Build forecasting logic for weekly demand using time series methods.
- Evaluate forecast quality with metrics such as MAPE and WAPE.

## Phase 6: Inventory projection and shortage detection
- Model budgets, lead times, inbound shipments, and projected inventory.
- Detect upcoming shortages and prioritize risk.

## Phase 7: Supplier and purchase order management
- Manage supplier capacity, lead times, and PO generation logic.
- Reconcile inbound stock and delivery exceptions.

## Phase 8: Mitigation recommendation engine
- Recommend substitute products, expediting, reorder actions, and route shifts.
- Score mitigation options by cost and urgency.

## Phase 9: Flask REST APIs
- Expose dashboard and operational endpoints for frontend consumption.
- Add health checks and data retrieval endpoints.

## Phase 10: React dashboard
- Build a dashboard for inventory, forecast, suppliers, and shortage analysis.
- Add charts and operational summaries.

## Phase 11: Integration testing and bug fixing
- Verify end-to-end functionality with pytest.
- Fix issues across backend, database, and frontend integration.
- Confirm dashboard, API, and synthetic-data workflows operate together cleanly.

## Phase 12: Documentation and GitHub submission
- Finalize documentation and API references.
- Validate all support scripts and prepare the final repository state.
- Confirm the repo is ready for review, handoff, and submission to GitHub.
- Capture final project status in the main repository documentation and verification notes.

## Phase 13: Local runtime orchestration and handoff
- Add a single-command startup flow for backend and frontend services.
- Simplify the local developer runbook for project launch and testing.
- Keep the project launch process consistent with the verified repo setup and validation steps.
- Package the completed implementation for review and repository handoff.

## Phase 14: Deployment readiness and container packaging
- Add container definitions for the Flask backend and React frontend.
- Provide a docker-compose workflow for combined local deployment.
- Prepare the repo for simpler handoff, provision, and production-style testing.
- Document the final deployment path for repository-level review.

## Phase 15: CI/CD and release automation
- Add an automated validation workflow for backend tests and frontend build checks.
- Establish a GitHub-based quality gate for future repository changes.
- Improve release confidence and collaborative handoff readiness.
- Keep the project prepared for an ongoing engineering workflow after submission.

## Phase 16: Release validation and production readiness
- Add a project-level release check script for final validation.
- Confirm repository completeness and key validation gates before release.
- Prepare the project for QA and final handoff in a repeatable manner.
- Keep the engineering workflow ready for future upgrades and merges.

## Phase 17: Security hardening and production defaults
- Harden the Flask app with production-safe security headers and cookie policies.
- Add configurable CORS settings for controlled frontend integration.
- Ensure production mode can enforce browser security controls like HSTS.
- Verify the hardened configuration with focused backend tests.

## Phase 18: Monitoring and operational observability
- Expose runtime metrics for uptime, environment, and service health.
- Configure console logging for easier local and deployment troubleshooting.
- Add a lightweight operational API surface for ongoing observability work.
- Verify the monitoring layer with focused backend tests.

## Phase 19: Frontend resilience and operational UX
- Improve dashboard resilience when the backend is temporarily unavailable.
- Add user-facing error handling and refresh controls for smoother operations.
- Keep the dashboard informative during transient API issues and loading states.
- Validate the frontend behavior through build checks and project-level QA.

## Phase 20: Reporting and export readiness
- Provide a CSV export endpoint for dashboard-level operational reporting.
- Add a user-triggered export action in the frontend dashboard UI.
- Make the project easier to share with stakeholders during reviews and operational check-ins.
- Verify the reporting workflow with backend API tests and project validation.
