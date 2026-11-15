# Deployment and environment secrets

## What goes where

| Variable | Used by | Secret? | Notes |
| --- | --- | --- | --- |
| `SECRET_KEY` | Backend | Yes | Signs JWTs. Generate a unique value; rotating it invalidates existing sessions. |
| `SHG_SERVICE_KEY` | Backend and AI service | Yes | Shared internal credential. Use the same random value in both services. |
| `POSTGRES_PASSWORD` | Docker Compose/PostgreSQL | Yes | Compose builds the backend database URL from this value. Use hex characters to avoid URL-escaping problems. |
| `LLM_API_KEY`, `VISION_API_KEY`, `OCR_API_KEY`, `SPEECH_API_KEY`, `TRANSLATION_API_KEY` | AI service | Yes, if used | Obtain from the corresponding provider; only configure keys for providers you enable. |
| `BACKEND_CORS_ORIGINS` | Backend | No | JSON array of exact browser origins, e.g. `["https://app.example.com"]`; no path or trailing slash. |
| `VITE_API_BASE_URL` | Frontend build | No | Public API URL, e.g. `https://api.example.com/api/v1`. Never put credentials in any `VITE_*` variable. |

Do not use the example values as production credentials. Keep `.env` files in your deployment secret manager or on the server, not in Git, a frontend build, or container image.

## Docker Compose deployment

1. Install Docker Engine with the Compose plugin and clone the repository onto the deployment host.
2. Create the Compose environment file and generate three independent values:

   ```powershell
   Copy-Item .env.example .env
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

   Run the Python command three times. Put one output in each of `POSTGRES_PASSWORD`, `SECRET_KEY`, and `SHG_SERVICE_KEY` in `.env`. Set `BACKEND_CORS_ORIGINS` to the exact HTTPS origin of the deployed frontend. Keep `POSTGRES_USER` and `POSTGRES_DB` as supplied unless you have a reason to change them.

3. If using a hosted AI provider, choose the corresponding provider name and place its credential in the matching AI key variable in `.env`. Leave unused provider credentials empty. Do not copy any server-side key into frontend settings.
4. Start the services:

   ```powershell
   docker compose config
   docker compose up --build -d
   docker compose ps
   ```

   `docker compose config` resolves environment values; do not paste its output into tickets or public logs. The backend applies Alembic migrations during startup. It does **not** create demo users or seed production data.
5. The API is bound to `127.0.0.1:8000` and the database and AI service have no public host ports. Put a TLS reverse proxy (or your hosting provider's private ingress) in front of the API and forward HTTPS traffic to the loopback API port. Do not expose ports 5432 or 8001 publicly. Configure the proxy's request-size limit consistently with `MAX_FILE_SIZE_MB`.
6. Deploy `frontend/dist` to a static host such as a CDN or static site service. In that host's build environment set:

   ```text
   VITE_API_BASE_URL=https://api.example.com/api/v1
   VITE_ENABLE_MOCK_FALLBACK=false
   VITE_APP_ENV=production
   ```

   Replace the example hostname. Rebuild the frontend after changing these values; Vite embeds `VITE_*` values into public JavaScript. From `frontend/`, run `npm ci` and `npm run build`, then publish `dist/`. Ensure the frontend's exact HTTPS origin is the backend's `BACKEND_CORS_ORIGINS` entry.

## Local key setup and rotation

For local development, copy each service template to its ignored local file (`backend/.env.example` to `backend/.env`, `ai-ml/.env.example` to `ai-ml/.env`) and set the same random `SHG_SERVICE_KEY` in both. Generate a different `SECRET_KEY` for the backend. Do not commit the resulting `.env` files.

If a key has been exposed, replace it in every service that uses it and restart/redeploy. Rotate `SECRET_KEY` separately from `SHG_SERVICE_KEY`: changing the JWT key signs users out, while changing the service key requires simultaneous backend/AI service updates. If a provider API key was exposed, revoke it with that provider and create a replacement.

## Before opening traffic

- Confirm `ENV=production`, `DEBUG=false`, and `AI_SERVICE_USE_MOCK_FALLBACK=false`; production configuration rejects development secrets, SQLite, non-HTTPS/wildcard/local CORS, and debug/mock settings.
- Public registration is disabled in production so visitors cannot choose privileged roles. Provision users through a trusted operator process. Do not run `backend/scripts/seed_data.py` or `backend/scripts/seed_full_demo.py` in production; those scripts create demo personas and credentials.
- Production sign-in uses the backend's real `/api/v1/auth/login/json` endpoint. Demo personas, mock user data, and preset tokens are development-only.
- Add HTTPS, backups, database monitoring, upload retention/access controls, and a process for applying migrations and rotating credentials.
- Review logs for accidental request or provider credential logging. Treat database backups and uploaded documents as sensitive data.

