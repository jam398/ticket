# Change Note: Backend Dotenv OpenAI Configuration

## Metadata

- **ID:** CHANGE-001
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a narrow runtime configuration fix. It does not change product scope, architecture, AI output schema, ticket data behavior, or workflow rules, and it is directly verifiable through backend tests and a settings check that does not expose secrets.

## Reason For Change

The backend already has OpenAI-compatible settings and a deterministic fallback AI client, but it does not load `backend/.env`. A user-created `backend/.env` with `OPENAI_API_KEY` therefore leaves the running backend on the deterministic `RuleBasedAIClient`, producing repeated fallback-style answers.

## Scope

In scope:

- Load `backend/.env` before backend settings are read.
- Keep the existing no-key deterministic fallback behavior.
- Add focused tests for settings and AI client selection.
- Document the backend restart requirement after editing `.env`.
- Ignore local secret and runtime files.

Out of scope:

- Changing AI prompt design or output schema.
- Calling the live OpenAI API during verification.
- Reading, printing, or storing the user's API key.
- Changing frontend workflows.

## Files Expected To Change

- `backend/app/config.py`
- `backend/app/tests/conftest.py`
- `backend/app/tests/test_config.py`
- `backend/requirements.txt`
- `.gitignore`
- `README.md`
- `docs/workflow-index.md`
- `docs/change-notes/change-001-backend-dotenv-openai-config.md`

## Change Summary

`backend/app/config.py` now loads `backend/.env` before reading settings, and settings fields use default factories so a fresh `get_settings()` call reads the current environment. `backend/requirements.txt` now includes `python-dotenv`. Backend tests explicitly clear `OPENAI_API_KEY` in test setup so normal tests keep using deterministic fallback behavior even when a local `.env` contains a real key. Focused config tests verify environment reading and AI client selection. README setup notes now document `backend/.env` and the backend restart requirement. `.gitignore` now excludes local secrets and generated runtime files.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| `backend/.env` exists with expected environment variable names | `if (Test-Path backend\.env) { ... }` checked names only: `APP_NAME`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `LLM_MODEL`, `EMBEDDING_MODEL`, `DATABASE_URL`, `CHROMA_PATH`, `SIMILARITY_THRESHOLD` |
| Existing config does not load `.env` | `Get-Content backend\app\config.py` showed `os.getenv(...)` defaults and no dotenv loader |
| Existing AI client uses fallback unless a non-placeholder `OPENAI_API_KEY` is visible to settings | `Get-Content backend\app\services\ai_client.py` showed `get_ai_client()` returning `RuleBasedAIClient` when no real key is configured |
| New dotenv dependency is available | `cd backend; python -m pip install "python-dotenv>=1.0"` reported requirement already satisfied |
| Backend tests pass after config change | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 34 tests |
| Local settings now load a usable key without exposing it | Safe Python settings check printed `openai_key_loaded=True`, `ai_client=OpenAICompatibleAIClient`, and `llm_model=gpt-4.1-mini` |
| Workflow artifacts validate after the change note update | `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed |
| Local backend was restarted on the frontend-configured port | Restarted Python uvicorn for `app.main:app` on port `8002`; `Invoke-RestMethod http://127.0.0.1:8002/health` returned `status: ok` |

## Risk Level

- **Risk:** Low
- **Reason:** The change is limited to configuration loading and tests. Runtime behavior stays the same when no valid key is configured.

## Verification

- `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Safe settings check that reports only whether a non-placeholder key is loaded, not the key value.
- `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Complete
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None
- **Checks Performed:** Read workflow artifacts, SPEC-002, SPRINT-05, SPRINT-08, config, AI client, README, requirements, and environment variable names in `backend/.env` without reading values. Implemented dotenv loading, dependency update, tests, README note, and ignore rules. Ran backend tests, a safe runtime settings check, workflow validation, and backend restart/health verification.
- **Evidence Reviewed:** Files and commands listed in the evidence log.
- **Result:** PASS
- **Carry-Forward Notes:** None
