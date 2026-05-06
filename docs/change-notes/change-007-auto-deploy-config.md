# Change Note: Auto Deploy Config

## Metadata

- **ID:** CHANGE-007
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-06
- **Last Updated:** 2026-05-06

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a bounded deployment configuration update. It adds provider config files and minimal environment/static-export settings without changing product behavior or application workflows.

## Reason For Change

The project needs deploy-ready automation files for the backend on Render and the frontend on GitHub Pages.

## Scope

In scope:

- Add a Render Blueprint file for the FastAPI backend.
- Add a GitHub Actions workflow for frontend deployment to GitHub Pages.
- Configure frontend static export mode for GitHub Pages builds.
- Make backend CORS origins configurable for deployed frontend origins.
- Update README deployment instructions.

Out of scope:

- Running an actual Render deployment from this environment.
- Enabling GitHub Pages settings in the GitHub UI.
- Adding authentication, production database migration, or a managed database.

## Files Expected To Change

- `render.yaml`
- `.github/workflows/deploy-frontend.yml`
- `frontend/next.config.ts`
- `frontend/public/.nojekyll`
- `.gitignore`
- `backend/app/config.py`
- `backend/app/main.py`
- `backend/.env.example`
- `backend/app/tests/test_config.py`
- `README.md`
- `docs/workflow-index.md`
- `docs/change-notes/change-007-auto-deploy-config.md`

## Change Summary

Added:

- `render.yaml` for auto-deploying the backend from `main` to Render.
- `.github/workflows/deploy-frontend.yml` for GitHub Pages deployment.
- GitHub Pages static export configuration in `frontend/next.config.ts`.
- Configurable backend CORS origins through `CORS_ALLOWED_ORIGINS`.
- README deployment notes.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Render Blueprint fields were checked against current docs | Render Blueprint YAML reference reviewed |
| Render free service cannot persist local SQLite/vector files | Render free-service docs reviewed; `render.yaml` uses `plan: free` without a disk and reseeds demo data on startup |
| GitHub Pages workflow actions were checked against current docs | GitHub Pages custom workflow docs reviewed |
| Backend start command matches current app | `Get-Content backend\app\main.py` and `Get-Content backend\requirements.txt` |
| Frontend build command exists | `Get-Content frontend\package.json` |
| CORS setting has test coverage | `backend/app/tests/test_config.py` |

## Risk Level

- **Risk:** Medium
- **Reason:** Deployment configuration depends on external provider settings and URLs. Local build/test verification can prove syntax and app compatibility, but not a completed cloud deployment.

## Verification

- `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- `cd frontend; npm.cmd run lint`
- `cd frontend; $env:GITHUB_PAGES='true'; $env:GITHUB_REPOSITORY='jam398/ticket'; $env:NEXT_PUBLIC_API_BASE_URL='https://triagepilot-ai-backend.onrender.com'; npm.cmd run build`
- `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-06
- **Verdict:** PASS
- **Gate Decision:** Complete
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** Cloud provider setup still must be completed in Render and GitHub repository settings. The free Render backend is demo-only because local SQLite/vector files are ephemeral.
- **Checks Performed:** Inspected backend/frontend commands, checked provider docs, added deployment files, added configurable CORS, added static export config, updated README, ignored generated `frontend/out/`, ran local verification.
- **Evidence Reviewed:** `render.yaml`, `.github/workflows/deploy-frontend.yml`, `frontend/next.config.ts`, `backend/app/config.py`, `backend/app/main.py`, `frontend/package.json`, `backend/app/tests/test_config.py`, `README.md`.
- **Result:** PASS. Backend Pytest passed `44` tests, frontend lint passed, GitHub-Pages-style `next build` passed and produced `frontend/out/.nojekyll`, and workflow validation passed.
- **Carry-Forward Notes:** In GitHub repository settings, set Pages source to GitHub Actions if it is not already enabled. In Render Blueprint setup, provide `OPENAI_API_KEY` if live AI responses are desired. Set GitHub repository variable `NEXT_PUBLIC_API_BASE_URL` if the Render backend URL differs from the default. For durable cloud ticket data, a later paid disk or managed database migration is required.
