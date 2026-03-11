# Lightweight Agent Simulator

A full-stack web app that simulates agentic reasoning and tool execution: interpret user tasks, route them to deterministic tools, and return a step-by-step execution trace.

## Prerequisites

- **npm path:** Node.js (v18+) and Python (3.10+) on your machine.
- **Docker path:** Docker and Docker Compose.

## Quick start (npm)

From the repo root:

```bash
git clone <your-repo-url>
cd lightweight-agent-simulator
npm install
npm run dev
```

Then open **http://localhost:5173** in your browser. The root `npm install` installs frontend dependencies and creates a backend virtualenv + installs Python dependencies. `npm run dev` starts both the API (port 8000) and the Vite dev server (port 5173).

## Quick start (Docker)

From the repo root:

```bash
git clone <your-repo-url>
cd lightweight-agent-simulator
docker compose up
```

Then open **http://localhost:5173**. The frontend proxies `/api` to the backend container.

## Run tests

**With npm / local backend:**

```bash
cd backend
python -m pytest tests/ -v
```

(Use the project virtualenv: `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\activate` on Windows.)

**With Docker:**

```bash
docker compose run backend python -m pytest tests/ -v
```

## Which to use?

- **npm:** Best for day-to-day development (hot reload, single backend process, no Docker).
- **Docker:** Best when you want a consistent environment or prefer not to install Node/Python locally.

## API and overrides

- The API runs at **http://localhost:8000** by default.
- To point the frontend at a different API (e.g. when not using the Vite proxy), set `VITE_API_URL` in `frontend/.env`.
