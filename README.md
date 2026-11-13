# supply-chain-inventory-optimization

AI-powered supply chain demand forecasting, inventory optimization, and shortage mitigation system.

## Repository status

Phase 1 has been completed: the repository was inspected, the development toolchain was confirmed, the folder structure was created, and the project foundation was established.

## Environment validation

The following tools were verified in the local environment:
- Python 3.14.4
- pip 26.0.1
- Node.js v24.21.0
- npm 11.19.0
- Git configured for the repository and connected to origin/main

## Project structure

```text
supply-chain-inventory-optimization/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── __init__.py
│   ├── models/
│   ├── generators/
│   ├── forecasting/
│   ├── optimization/
│   ├── validation/
│   ├── routes/
│   ├── services/
│   └── tests/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── data/
│   ├── generated/
│   ├── ground_truth/
│   └── validation/
├── documentation/
│   └── PROJECT_PLAN.md
├── scripts/
├── .env.example
├── .gitignore
├── README.md
└── .git/
```

## Development roadmap

1. Phase 1: Repository inspection and project setup.
2. Phase 2: Database models and relationships.
3. Phase 3: Synthetic data generation.
4. Phase 4: Data validation and ground truth.
5. Phase 5: Demand forecasting.
6. Phase 6: Inventory projection and shortage detection.
7. Phase 7: Supplier and purchase order management.
8. Phase 8: Mitigation recommendation engine.
9. Phase 9: Flask REST APIs.
10. Phase 10: React dashboard.
11. Phase 11: Integration testing and bug fixing.
12. Phase 12: Documentation and GitHub submission.

## Phase 1 deliverables

- Confirmed baseline workspace and project metadata.
- Created modular backend/frontend folder structure for future implementation.
- Added environment config template for MySQL and application settings.
- Created a development plan for the full project lifecycle.
- Established a minimal backend health endpoint and a frontend scaffold.

## Phase 2 deliverables

- Added the full SQLAlchemy model layer for products, locations, inventory, demand forecasts, suppliers, lead times, purchase orders, production plans, shortages, and mitigations.
- Included explicit relationship tables for many-to-many supplier coverage and inventory event history.
- Documented the schema and relationship design in the project documentation.
- Verified model creation and relationship integrity with pytest.

## Phase 3 deliverables

- Implemented a deterministic synthetic data generator using seed 20261022.
- Added realistic generation for SKUs, locations, suppliers, inventory levels, weekly demand, purchase orders, supplier capacity, and lead times.
- Built CLI support for both sample and full dataset generation modes.
- Added data output files under the generated and ground-truth folders.
- Validated generation logic and anomaly support through pytest.

## Phase 4 deliverables

- Implemented data validation checks for required files, inventory balance, forecast rows, purchase orders, and supplier capacity.
- Added business-rule validation utilities for capacity and demand constraints.
- Built reconciliation logic to summarize inventory, demand, and purchase-order totals.
- Added a validation runner script and saved validation artifacts under the data/validation folder.
- Verified validation behavior and reconciliation output with pytest.

## Phase 5 deliverables

- Added a demand forecasting module using a linear-regression-with-seasonality approach for short-term weekly forecasts.
- Implemented forecast evaluation metrics including MAPE and WAPE.
- Built CSV-based forecasting utilities that work on generated demand datasets.
- Verified the forecasting logic and evaluation metrics with pytest.

## Phase 6 deliverables

- Added an inventory projection engine that evaluates current stock against forecast demand and inbound stock.
- Added shortage detection that flags projected coverage gaps against safety stock and prioritizes risk.
- Built a lightweight operational model for planning projected balance and shortage severity.
- Verified the inventory projection and shortage detection logic with pytest.

## Phase 7 deliverables

- Added a supplier optimization engine that scores alternative suppliers on lead time, capacity, rating, and quantity recommendations.
- Added purchase-order generation logic that converts shortage recommendations into planned POs.
- Exposed an operational service layer for supplier recommendation workflows.
- Verified supplier ranking and purchase-order conversion with pytest.

## Phase 8 deliverables

- Added a mitigation recommendation engine that produces ranked actions for projected shortages.
- Included alternate supplier, expedite, and production reallocation options with cost and impact scoring.
- Verified mitigation-generation behavior with dedicated phase tests.

## Phase 9 deliverables

- Added working Flask API routes for dashboard summary, inventory, supplier, forecast, purchase-order, shortage, and mitigation views.
- Wired the API to the generated data files and optimization logic so the backend is operational and testable.
- Added API-level validation checks with pytest for the service endpoints.
- Confirmed the application exposes a working health and API root endpoint.

## Phase 10 deliverables

- Built a Vite + React dashboard shell integrating Bootstrap styling and a KPI summary layout.
- Add data cards and tables for inventory, demand forecasts, and projected shortages.
- Connected the frontend to the Flask backend for summary and dataset views.
- Verified the dashboard compiles successfully with a production build.

## Phase 11 deliverables

- Executed the backend verification suite against the full app flow and confirmed all 19 tests pass.
- Smoke-tested the Flask app factory and live API endpoints for health and dashboard summaries.
- Reproduced and resolved the environment-specific dependency installation issue by moving the project into a repo-local virtual environment.
- Confirmed the application is stable across backend logic, API exposure, and frontend build integration.

## Phase 12 deliverables

- Finalized the project documentation and phase-by-phase status in the repository README.
- Documented the final implementation plan and phase completion timeline in the project documentation.
- Validated the repository state and confirmed the backend and frontend layers are working together cleanly.
- Prepared the repository for handoff and GitHub submission by ensuring the project structure, scripts, and environment notes are organized and review-ready.

## Final repository state

The supply-chain inventory optimization project is now in a complete, validated prototype state with:
- a modular Flask backend powering the data and optimization workflows,
- a deterministic synthetic data pipeline and validation layer,
- a forecasting and shortage optimization engine,
- supplier and mitigation recommendation logic,
- a working React dashboard frontend,
- and end-to-end project documentation ready for handoff.

## Phase 13 deliverables

- Added a repo-local project startup script so the backend and frontend can be launched together with a single command.
- Documented the runtime entry points for the Flask API and React dashboard.
- Preserved the validated backend and frontend expectations while making local startup more repeatable.
- Kept the repository ready for local execution without repeating manual environment setup steps.

## Phase 14 deliverables

- Added Docker configuration for the backend, frontend, and combined local deployment workflow.
- Created a docker-compose setup to run the API and dashboard together with a single command.
- Added container-friendly environment configuration to support a smoother production-style deployment flow.
- Documented the deployment path for future handoff, testing, and packaging work.

## Local deployment

For the local MySQL installation, configure `.env` with `DB_HOST=127.0.0.1`,
`DB_PORT=3306`, `DB_NAME=supply_chain_db`, `DB_USER`, and `DB_PASSWORD`. Keep the
password in `.env`; do not commit it. Apply the checked-in migrations from the
repository root:

```powershell
.\.venv\Scripts\flask.exe --app backend.app db upgrade
```

The database health endpoint is `GET /health/database`; it returns HTTP 200
when the configured database answers `SELECT 1` and HTTP 503 when unavailable.
The app does not create tables at startup. API routes remain CSV-backed at this
stage; migrating those services to database records is a later step.

For an optional isolated Docker deployment, set `DB_ROOT_PASSWORD` in `.env` and
run `docker compose up --build`. This starts a separate MySQL container.

Backend tests use the explicit `TestingConfig` with in-memory SQLite.

## MySQL initialization verification

- Connected through Flask-SQLAlchemy/PyMySQL to `supply_chain_db` on MySQL 8.0.46.
- Applied initial revision `e8c6f1813610`; all 11 required entity tables and the `sku_supplier` and `inventory_events` support tables exist.
- Confirmed `flask db check` reports no pending changes and a repeated `flask db upgrade` leaves schema and row counts unchanged.
- Verified `GET /health/database` returns HTTP 200 with `{"status":"ok","database":{"status":"connected","dialect":"mysql"}}`.
- Before the initial migration, the database contained no application tables or application records. The migration does not drop tables; its downgrade is disabled to prevent accidental data deletion.

## Phase 15 deliverables

- Added a GitHub Actions CI workflow to validate the backend test suite and frontend production build on each push and pull request.
- Established a repeatable release gate to keep the repository in a checked, working state after future updates.
- Prepared the project for a cleaner collaborative handoff with automated validation requirements.
- Documented the project’s final automation path for code quality and deployment readiness.

## Phase 16 deliverables

- Added a release validation script to confirm the repo is structurally complete and passes key project checks before release.
- Encapsulated backend and frontend verification into a reusable project-level validation entry point.
- Finalized the project’s production-readiness workflow for handoff, QA, and future code changes.
- Kept the repository aligned with a stable, review-ready release pipeline.

## Release validation

To run the project release check from the repo root:

```bash
python scripts/release_check.py
```

This verifies the expected project files exist and runs the backend test suite plus the frontend production build.

## Phase 17 deliverables

- Added production-oriented security defaults for Flask session handling and response headers.
- Hardened the API layer with explicit `X-Content-Type-Options`, `X-Frame-Options`, and `Referrer-Policy` headers.
- Added environment-aware HSTS support for production deployments and ensured the app can accept configured CORS origins.
- Verified the hardened configuration with dedicated backend tests.

## Phase 18 deliverables

- Added a lightweight monitoring endpoint exposing runtime health, environment, timestamp, uptime, and Python version metadata.
- Configured application logging to emit structured standard logs to the console for easier local and deployment diagnostics.
- Exposed monitoring data through the backend API for future operational dashboards and health checks.
- Verified the observability layer with focused backend tests.

## Phase 19 deliverables

- Added stronger frontend resilience for API failures with a readable warning banner and refresh action.
- Improved API integration by centralizing request-error messages and surfacing them to the dashboard UI.
- Kept the dashboard usable during transient backend downtime without leaving users with a blank or broken loading state.
- Prepared the frontend for smoother operational use during local demos and review sessions.

## Phase 20 deliverables

- Added a dashboard export endpoint that delivers a CSV snapshot of key operational inventory data.
- Enabled the frontend dashboard to export the current view as a CSV file from the UI.
- Improved the operational workflow by making the dashboard easier to share with stakeholders and support teams.
- Verified the export path and API metadata with dedicated backend tests.

## Frontend-backend integration verification

- Verified the live Flask API at `http://localhost:5000` from the running frontend browser.
- Confirmed dashboard summary, inventory (125 rows), suppliers (10 rows), forecasts (1,000 rows), purchase orders (100 rows), shortages (115 rows), and mitigations (345 rows) return successful responses.
- Confirmed dashboard KPIs match the summary API payload and the risk chart is derived from shortage severities.
- Verified Refresh data sends requests to the API and refreshes the displayed dashboard records.
- Verified the export action requests the backend and receives a 200 attachment response with a 125-record CSV containing inventory, forecast totals, and projected shortage fields.
- Aligned dashboard, shortage, mitigation, and export projections so they include generated purchase-order inbound quantities consistently.
- Generated dataset values are currently CSV-backed prototype data. The operational API routes are not yet reading live records from the SQLAlchemy database.

## Completion status

MySQL connectivity, the initial schema migration, and the database health check
are complete and verified. Database seeding and migration of the existing
CSV-backed API/frontend workflows to SQLAlchemy remain in progress.
