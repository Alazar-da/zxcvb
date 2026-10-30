# Wind Generation Forecast & Day-Ahead Procurement Dashboard

Decision-time GB wind forecast intelligence for a power trading desk. The app selects the latest WINDFOR forecast published on or before the configurable D-1 decision cutoff, then compares it with actual FUELHH wind generation without lookahead leakage.

## Run locally

```bash
docker compose up --build
```

Open `http://localhost:5173`; API docs are at `http://localhost:8000/docs`.

Without Docker: from `backend`, install `requirements.txt` and run `uvicorn app.main:app --reload`; from `frontend`, run `npm install && npm run dev`.

## Architecture

`Elexon BMRS API -> ingestion/cache -> FastAPI domain services -> React/Vite dashboard`

The current first slice includes a reproducible January 2026 demo snapshot. It is labelled in the UI and is intentionally used to make the dashboard useful even when a live API snapshot is unavailable. `ElexonClient` is ready for cached historical WINDFOR/FUELHH ingestion; the production wiring should persist raw responses and configure `ELEXON_BASE_URL`.

Decision cutoff defaults to `11:00` Europe/London and can be changed with `DECISION_CUTOFF` and `DECISION_TIMEZONE`. Elexon’s documented historic wind endpoint accepts `from` and `to` datetime query parameters and returns `publishTime`, `startTime`, `settlementDate`, `settlementPeriod`, and `generation` fields.

## Deployment

Deploy the frontend container/static build to Vercel and the FastAPI backend to Render (simple long-running web service). Set `VITE_API_URL` in Vercel to the Render URL. Deployment URLs are intentionally left as configuration until accounts are connected.

## AI disclosure

This project was built with AI assistance for scaffolding, domain logic, tests, UI implementation, and documentation. Human review is required before using it for live procurement decisions.

