# Production deployment: Render + Vercel

This project has three services: a public FastAPI backend, a private AI service, and a Vite/React frontend. Deploy the backend, AI service, and managed PostgreSQL database on Render; deploy the frontend on Vercel. Use the same Git branch for all deployments (the current prepared branch is `deployment-security`; alternatively, merge it into your chosen production branch first).

## Required settings and keys

| Variable | Set on | Secret? | Value / where to get it |
| --- | --- | --- | --- |
| `DATABASE_URL` | Render backend | Yes | Internal connection URL from the Render PostgreSQL database's **Connect** panel. Use the internal URL, not the external one. |
| `SECRET_KEY` | Render backend | Yes | Generate a fresh random value (at least 32 characters). It signs user JWTs; never reuse `SHG_SERVICE_KEY`. |
| `SHG_SERVICE_KEY` | Render backend and AI service | Yes | Generate a second fresh random value (at least 32 characters); enter the exact same value in both services. It authenticates backend-to-AI requests. |
| `AI_SERVICE_BASE_URL` | Render backend | No | AI service's private address from Render **Connect** (for example, `http://<private-hostname>:8001`). Keep both Render services in the same workspace and region. |
| `BACKEND_CORS_ORIGINS` | Render backend | No | JSON array containing the exact Vercel production origin, e.g. `["https://your-app.vercel.app"]`. No path or trailing slash. |
| `VITE_API_BASE_URL` | Vercel frontend | No | Public backend URL plus `/api/v1`, e.g. `https://your-backend.onrender.com/api/v1`. |
| `LLM_API_KEY` | Render AI service | Yes, optional | Only needed for the external Groq LLM. Create a key in the [Groq Console](https://console.groq.com/keys) and set `LLM_PROVIDER=groq`. The current integration calls Groq's API endpoint. |

Generate the two application secrets in PowerShell; run this block once for each key and keep the two outputs different:

```powershell
$bytes = New-Object byte[] 32
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$rng.GetBytes($bytes)
[BitConverter]::ToString($bytes).Replace("-", "").ToLowerInvariant()
$rng.Dispose()
```

Paste generated secrets directly into Render's service environment settings. Do not put them in Git, `vercel.json`, a `VITE_*` variable, or this document. The frontend settings are public build-time values, not secrets.

The current AI service uses local implementations for vision, OCR, speech, and translation; their `VISION_API_KEY`, `OCR_API_KEY`, `SPEECH_API_KEY`, and `TRANSLATION_API_KEY` settings are not required to deploy and do not currently configure external providers. Leave them unset. The external LLM is optional; the default local LLM requires no provider key.

## 1. Create the Render PostgreSQL database

1. In the [Render Dashboard](https://dashboard.render.com/), choose **New > PostgreSQL**.
2. Choose a database name and region. Use the same region for the backend and AI service.
3. Wait until the database is available. From its **Connect** panel, copy the **Internal Database URL**. Treat this URL like a password.
4. Do not expose the database publicly for the application. The backend connects to it over Render's private network.

## 2. Deploy the private AI service on Render

1. Choose **New > Private Service**, connect the GitHub repository, and select the production branch.
2. Set **Language** to **Docker**, **Root Directory** to `ai-ml`, and **Dockerfile Path** to `Dockerfile`. Choose the same Render region as the database and backend.
3. Add these environment variables in the service's **Environment** page:

   ```text
   APP_ENV=production
   DEBUG=false
   SHG_SERVICE_KEY=<the generated shared service key>
   CORS_ORIGINS=[]
   LLM_PROVIDER=local
   ```

   `SHG_SERVICE_KEY` must exactly match the backend value. To use Groq instead of the local LLM, set `LLM_PROVIDER=groq` and add `LLM_API_KEY` from the Groq Console. Do not add a provider key to Vercel.
4. Deploy and wait for the service to become healthy. In **Connect**, copy its private service address; the AI server listens on port `8001`. Do not make this service public.

## 3. Deploy the public backend on Render

1. Choose **New > Web Service**, connect the same repository and production branch.
2. Set **Language** to **Docker**, **Root Directory** to `backend`, and **Dockerfile Path** to `Dockerfile`. Use the same region as the database and AI service.
3. Set the following environment variables:

   ```text
   ENV=production
   DEBUG=false
   ALLOW_PUBLIC_REGISTRATION=false
   DATABASE_URL=<Render PostgreSQL Internal Database URL>
   SECRET_KEY=<the generated backend-only JWT key>
   SHG_SERVICE_KEY=<the same key entered on the AI service>
   AI_SERVICE_BASE_URL=http://<AI private hostname>:8001
   AI_SERVICE_USE_MOCK_FALLBACK=false
   BACKEND_CORS_ORIGINS=["https://your-app.vercel.app"]
   ```

   Replace the placeholders. Render may show the AI private address as `hostname:8001`; use that hostname with `http://` and port `8001` in `AI_SERVICE_BASE_URL` (do not append the port twice). `BACKEND_CORS_ORIGINS` must be valid JSON and contain the final Vercel production origin. Add your custom frontend domain here too if you use one.
4. Set the Render health check path to `/health`. The backend container uses Render's `PORT` value and falls back to port `8000` locally. Its startup command applies database migrations; it does not create demo users.
5. Deploy and verify `https://<backend-service>.onrender.com/health` returns a healthy response.

**Uploaded files:** Render's service filesystem is ephemeral by default. If users will upload files, attach a persistent disk to the backend at `/app/uploads` (and keep `UPLOAD_DIR=/app/uploads`), or implement durable object storage before production. Render persistent disks require a compatible paid service plan and affect scaling options.

## 4. Deploy the frontend on Vercel

1. In the [Vercel Dashboard](https://vercel.com/dashboard), import the same GitHub repository and select the production branch.
2. Set **Root Directory** to `frontend` and use the Vite settings:
   - Build command: `npm run build`
   - Output directory: `dist`
   - Install command: `npm ci`
3. Add these environment variables for the **Production** environment:

   ```text
   VITE_API_BASE_URL=https://<backend-service>.onrender.com/api/v1
   VITE_ENABLE_MOCK_FALLBACK=false
   VITE_APP_ENV=production
   ```

   These values are included in public frontend assets. Never add database credentials, JWT keys, the service key, or provider API keys to Vercel or any `VITE_*` variable.
4. Deploy the frontend, then copy its final production origin (or configure a custom domain). Update Render's `BACKEND_CORS_ORIGINS` to that exact HTTPS origin and redeploy the backend if necessary.
5. Confirm the application loads, sign-in calls the backend, and protected routes still work when refreshed directly. The repository includes `frontend/vercel.json` so Vercel serves the SPA entry point for client-side routes.

## 5. Production checks

- Confirm backend `/health` is healthy and Vercel's production deployment is ready.
- Test login and a normal API request from the deployed frontend. CORS errors usually mean the Vercel origin is missing or misspelled in `BACKEND_CORS_ORIGINS`.
- Check Render logs for migration or database errors; do not post logs containing connection URLs or secrets publicly.
- Public registration is disabled. Production has no seeded demo users; arrange a trusted operator process to provision the first account before opening the site to users. Do not run `backend/scripts/seed_data.py` or `backend/scripts/seed_full_demo.py` in production.
- Configure database backups, monitoring, upload retention/access controls, and a credential rotation process. Use a production-capable service plan and review current Render/Vercel limits for your expected traffic.

## Docker Compose deployment

1. Install Docker Engine with the Compose plugin and clone the repository onto the deployment host.
2. Create the Compose environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

   Generate fresh values for `POSTGRES_PASSWORD`, `SECRET_KEY`, and `SHG_SERVICE_KEY`; each must be different. Set `BACKEND_CORS_ORIGINS` to the exact HTTPS origin of the deployed frontend. Keep `POSTGRES_USER` and `POSTGRES_DB` as supplied unless you have a reason to change them.
3. Start the services:

   ```powershell
   docker compose config
   docker compose up --build -d
   docker compose ps
   ```

   `docker compose config` resolves environment values; do not paste its output into tickets or public logs. The backend applies Alembic migrations during startup. It does **not** create demo users or seed production data.
4. Compose binds the API to `127.0.0.1:8000`; the database and AI service have no public host ports. Put a TLS reverse proxy (or private ingress) in front of the API. Do not expose ports 5432 or 8001 publicly. Configure the proxy's request-size limit consistently with `MAX_FILE_SIZE_MB`.
5. Build and publish the frontend with `npm ci` and `npm run build` from `frontend/`. Set `VITE_API_BASE_URL`, `VITE_ENABLE_MOCK_FALLBACK=false`, and `VITE_APP_ENV=production` in the frontend build environment, then publish `frontend/dist`. Ensure the frontend's exact HTTPS origin is in `BACKEND_CORS_ORIGINS`.

## Local key setup and rotation

For local development, copy each service template to its ignored local file (`backend/.env.example` to `backend/.env`, `ai-ml/.env.example` to `ai-ml/.env`) and set the same random `SHG_SERVICE_KEY` in both. Generate a different `SECRET_KEY` for the backend. Do not commit the resulting `.env` files.

If a key has been exposed, replace it in every service that uses it and restart/redeploy. Rotate `SECRET_KEY` separately from `SHG_SERVICE_KEY`: changing the JWT key signs users out, while changing the service key requires simultaneous backend/AI service updates. If a provider API key was exposed, revoke it with that provider and create a replacement.

## Provider documentation

- [Render Docker services](https://render.com/docs/docker), [private services](https://render.com/docs/private-services), [private networking](https://render.com/docs/private-network), [environment variables](https://render.com/docs/configure-environment-variables), and [PostgreSQL connection details](https://render.com/docs/postgresql-creating-connecting)
- [Vercel Vite deployment](https://vercel.com/docs/frameworks/frontend/vite) and [Vercel environment variables](https://vercel.com/docs/environment-variables)

