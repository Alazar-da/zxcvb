# Wind Generation Forecast & Day-Ahead Procurement Dashboard

Decision-time GB wind forecast intelligence for a power trading desk. The app selects the latest WINDFOR forecast published on or before the configurable D-1 decision cutoff, then compares it with actual FUELHH wind generation without lookahead leakage.

## Live application

Frontend: [https://frontend-delta-lime-63.vercel.app/](https://frontend-delta-lime-63.vercel.app/)

The frontend is deployed on Vercel. The backend can be run locally with Docker or deployed as a separate FastAPI service; set `VITE_API_URL` in Vercel to the public backend URL when deploying the API.

## Project structure

```text
inter/
├── backend/
│   ├── app/
│   │   ├── api/                 # API route package
│   │   ├── domain/
│   │   │   ├── metrics.py       # MAE, RMSE, bias, P90/P95 calculations
│   │   │   ├── models.py        # Pydantic response/domain models
│   │   │   └── selection.py      # Decision-cutoff vintage selection
│   │   ├── services/
│   │   │   ├── demo_data.py     # Reproducible January 2026 demo series
│   │   │   └── elexon.py        # Elexon BMRS client and local cache
│   │   └── main.py               # FastAPI application and REST endpoints
│   ├── tests/test_domain.py      # Core selection and metrics tests
│   ├── data/                     # Local cached/raw data location
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Backend container image
├── frontend/
│   ├── src/
│   │   ├── main.tsx             # React dashboard and API integration
│   │   └── styles.css           # Dashboard styling and responsive layout
│   ├── index.html               # Vite HTML entry point
│   ├── package.json              # Frontend scripts and dependencies
│   ├── tsconfig.json             # TypeScript configuration
│   ├── vite.config.ts            # Vite configuration
│   └── Dockerfile                # Frontend/Nginx image
├── docker-compose.yml            # Runs frontend and backend together
├── .gitignore                    # Generated files and dependencies excluded from Git
└── README.md                     # Project documentation
```

## Run locally with Docker

```bash
cd E:\inter
docker compose up --build
```

Open the dashboard at `http://localhost:5173`. The backend API is available at `http://localhost:8000`, with interactive OpenAPI documentation at `http://localhost:8000/docs`.

To stop the services, press `Ctrl+C`. Docker Desktop must be running before executing the compose command.

## Run locally without Docker

Start the backend in PowerShell:

```powershell
cd E:\inter\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In a second PowerShell window, start the frontend:

```powershell
cd E:\inter\frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

Run the backend tests from `backend` with:

```powershell
python -m pytest -q
```

## Architecture

`Elexon BMRS API -> ingestion/cache -> FastAPI domain services -> React/Vite dashboard`

The current first slice includes a reproducible January 2026 demo snapshot. It is labelled in the UI and is intentionally used to make the dashboard useful even when a live API snapshot is unavailable. `ElexonClient` is ready for cached historical WINDFOR/FUELHH ingestion; the production wiring should persist raw responses and configure `ELEXON_BASE_URL`.

Decision cutoff defaults to `11:00` Europe/London and can be changed with `DECISION_CUTOFF` and `DECISION_TIMEZONE`. Elexon’s documented historic wind endpoint accepts `from` and `to` datetime query parameters and returns `publishTime`, `startTime`, `settlementDate`, `settlementPeriod`, and `generation` fields.

## Deployment

The frontend is deployed to Vercel at [https://frontend-delta-lime-63.vercel.app/](https://frontend-delta-lime-63.vercel.app/). For a production deployment, deploy the FastAPI backend to Render, Railway, or another long-running Python service, then configure the Vercel environment variable `VITE_API_URL` with the backend URL.

## AI disclosure

This project was built with AI assistance for scaffolding, domain logic, tests, UI implementation, and documentation. Human review is required before using it for live procurement decisions.

