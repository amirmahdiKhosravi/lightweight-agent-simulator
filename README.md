# Lightweight Agent Simulator

A full-stack web application that simulates agentic AI reasoning without relying on LLMs or external APIs. It interprets natural-language tasks, routes them to deterministic tools via rule-based intent parsing, and returns a step-by-step execution trace — demonstrating the core mechanics behind frameworks like LangChain and Semantic Kernel in a transparent, dependency-free way.

## Table of Contents

- [How to Run the Project](#how-to-run-the-project)
- [Running Tests](#running-tests)
- [Tech Stack and Dependencies](#tech-stack-and-dependencies)
- [Design Decisions](#design-decisions)
- [Time Spent](#time-spent)
- [Production Considerations](#production-considerations)
- [Other Details](#other-details)
  - [Architecture Overview](#architecture-overview)
  - [Project Structure](#project-structure)
  - [API Reference](#api-reference)
  - [Adding a New Tool](#adding-a-new-tool)

## How to Run the Project

There is no need to start the frontend and backend separately — the project includes orchestration scripts that handle both with a single command.

### Prerequisites

- **npm path:** Node.js (v18+) and Python (3.10+)
- **Docker path:** Docker and Docker Compose

### Option 1: npm 

```bash
git clone https://github.com/amirmahdiKhosravi/lightweight-agent-simulator.git
cd lightweight-agent-simulator
npm install
npm run dev
```

`npm install` installs frontend dependencies and creates a Python virtualenv with backend dependencies. `npm run dev` starts both the API (port 8000) and the Vite dev server (port 5173) with hot reload.

Open **http://localhost:5173** in your browser.

### Option 2: Docker

```bash
git clone https://github.com/amirmahdiKhosravi/lightweight-agent-simulator.git
cd lightweight-agent-simulator
docker compose up
# or: docker-compose up
```

Open **http://localhost:5173**. The frontend container proxies `/api` requests to the backend container.

## Running Tests

**Local (with virtualenv):**

```bash
cd backend
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pytest tests/ -v
```

**Docker:**

```bash
docker compose run backend python -m pytest tests/ -v
```

## Tech Stack and Dependencies

| Layer         | Technology                   | Role                                            |
|---------------|------------------------------|-------------------------------------------------|
| Frontend      | React 19, Vite 7             | UI components and development tooling           |
| Styling       | Tailwind CSS 4               | Utility-first CSS framework                     |
| Backend       | Python 3.10+, FastAPI        | API server and request handling                 |
| Server        | Uvicorn                      | ASGI server for FastAPI                         |
| Database      | SQLite                       | Lightweight persistence for task history        |
| Validation    | Pydantic                     | Request/response schema validation              |
| Testing       | pytest                       | Backend unit and integration tests              |
| Orchestration | npm + concurrently           | Single-command startup for both services        |
| Containers    | Docker, Docker Compose       | Reproducible builds and deployment              |

Frontend dependencies are managed via `frontend/package.json`, and backend dependencies are listed in `backend/requirements.txt`. The root `package.json` ties everything together with orchestration scripts that install and run both layers.

## Assumptions and Tradeoffs

| Decision | Rationale |
|----------|-----------|
| **Deterministic Intent Parsing** | Provides zero-latency, 100% predictable tool routing. This flawlessly satisfies the "lightweight" constraint while perfectly mocking the interface of a semantic router, keeping the focus strictly on architectural design and execution flow. |
| **SQLite for persistence** | Zero configuration, no external services, and sufficient for a single-user demo. The DB file is created automatically on first run. |
| **Tool registry as a dictionary** | O(1) lookup by tool name. Adding a new tool is a one-line change to the registry. |
| **BaseTool ABC** | Enforces a consistent `execute(**kwargs)` interface across all tools, making the system extensible via the strategy pattern. |
| **Execution trace as a first-class concept** | The step-by-step trace is the core value of the project — it makes the agent's reasoning transparent and inspectable, mirroring what tools like LangSmith provide for production LLM agents. |
| **Synchronous Execution vs. WebSockets** | I chose standard REST (request/response) over WebSockets/SSE for the execution trace. While real-time streaming looks flashier, standard HTTP keeps the architecture lightweight, testable, and maintainable. |

## Time Spent

Approximately 6 hours, broken down into:

- Architecture & Scaffolding (1hr)
- Agent Domain Logic & Tools (2hrs)
- API & Persistence Layer (1hr)
- React Frontend & UI (1.5hrs)
- Dockerization, Testing & Documentation (1hr)

## Production Considerations and Improvements

This project intentionally keeps things lightweight to focus on the core agent pattern. In a production system, each layer would be replaced or augmented with battle-tested tools:

| Concern | This Project | Production Alternative |
|---------|-------------|----------------------|
| **Intent parsing** | Rule-based (regex/keywords) | LLM-backed via [LangChain](https://www.langchain.com/) or [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/) |
| **Agent orchestration** | Simple linear pipeline | [LangGraph](https://langchain-ai.github.io/langgraph/) for stateful multi-step graphs, or [AutoGen](https://microsoft.github.io/autogen/) for multi-agent collaboration |
| **Database** | SQLite (single file) | PostgreSQL, or a managed service like [Supabase](https://supabase.com/) |
| **Deployment** | Docker Compose | Kubernetes, AWS ECS, or Azure Container Apps |
| **Observability** | Execution trace in SQLite | [LangSmith](https://smith.langchain.com/) for LLM tracing, OpenTelemetry for general observability |
| **Guardrails** | None | Input validation, output filtering, and rate limiting to prevent misuse or unsafe tool execution |

**Azure-centric stack:** If your organization uses Azure, [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/) (C# or Python) integrates natively with Azure OpenAI, Azure AI Search, and Azure Cosmos DB, providing a production-grade equivalent of the patterns demonstrated here.

**Python-centric stack:** [LangChain](https://www.langchain.com/) for tool/chain abstractions + [LangGraph](https://langchain-ai.github.io/langgraph/) for complex agent workflows + [LangSmith](https://smith.langchain.com/) for tracing and evaluation form the most widely adopted open-source stack.

## Other Details

### Architecture Overview

The system follows a pipeline pattern: user input flows through a parser that determines intent, a router that selects the right tool, and a tool executor that returns a structured trace.

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (React + Vite)                                    │
│  User submits task ──► POST /api/tasks ──► Display trace    │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP (Vite proxy in dev)
┌──────────────────────────▼──────────────────────────────────┐
│  Backend (FastAPI)                                          │
│                                                             │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  Agent    │───►│ IntentParser │───►│ Tool Registry    │   │
│  │          │    │ (rule-based) │    │ (dict lookup)    │   │
│  └──────────┘    └──────────────┘    └────────┬─────────┘   │
│                                               │             │
│       ┌───────────────┬───────────────┬───────┘             │
│       ▼               ▼               ▼                     │
│  Calculator     WeatherMock     TextProcessor               │
│                                                             │
│  Result + execution trace ──► SQLite                        │
└─────────────────────────────────────────────────────────────┘
```

**Request flow:**

1. The user types a task in the React frontend (e.g. *"What is 5 + 3?"*)
2. The frontend sends a `POST /api/tasks` request to FastAPI
3. The `Agent` passes the input to `IntentParser`, which uses regex/keyword matching to determine which tool to call and with what arguments
4. The matched tool is retrieved from the tool registry (a dictionary for O(1) lookup) and executed
5. The result and a step-by-step execution trace are saved to SQLite and returned to the frontend
6. The frontend renders the result and the full trace for inspection

### Project Structure

```
lightweight-agent-simulator/
├── backend/
│   ├── main.py              # FastAPI app, routes, CORS, lifespan
│   ├── agent.py             # Orchestrates parser → tool → trace
│   ├── parser.py            # Rule-based intent classification
│   ├── tools.py             # BaseTool ABC + three tool implementations
│   ├── schemas.py           # Pydantic request/response models
│   ├── database.py          # SQLite persistence layer
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       ├── test_agent.py
│       ├── test_tools.py
│       └── test_parser.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main UI: input, result, trace, history sidebar
│   │   ├── api.js           # HTTP client (submitTask, getTaskHistory)
│   │   ├── main.jsx         # React entry point
│   │   ├── App.css
│   │   └── index.css        # Tailwind imports
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js       # Dev server + /api proxy to backend
│   └── Dockerfile
├── scripts/
│   ├── install-backend.js   # Creates virtualenv + pip install
│   └── start-backend.js     # Starts uvicorn via the virtualenv
├── package.json             # Root-level dev scripts
├── docker-compose.yml
└── README.md
```

### API Reference

| Method | Endpoint      | Description                          | Request Body                | Response                                              |
|--------|---------------|--------------------------------------|-----------------------------|-------------------------------------------------------|
| POST   | `/api/tasks`  | Submit a task for the agent to solve | `{ "task": "5 + 3" }`      | `{ final_output, execution_steps, tools_used, timestamp }` |
| GET    | `/api/tasks`  | Retrieve all past task results       | —                           | Array of task objects with the same fields plus `id`   |

### Adding a New Tool

The system is designed around a `BaseTool` abstract class, making it straightforward to extend with new capabilities.

**1. Define the tool** in `backend/tools.py`:

```python
class TranslatorTool(BaseTool):
    name = "TranslatorTool"
    description = "Translates text between languages."

    def execute(self, text: str = "", target_lang: str = "en", **kwargs) -> str:
        # Your implementation here
        return translated_text
```

**2. Register it** in `backend/agent.py`:

```python
from tools import CalculatorTool, WeatherMockTool, TextProcessorTool, TranslatorTool

class Agent:
    def __init__(self):
        self.tools = {
            "CalculatorTool": CalculatorTool(),
            "WeatherMockTool": WeatherMockTool(),
            "TextProcessorTool": TextProcessorTool(),
            "TranslatorTool": TranslatorTool(),       # new
        }
```

**3. Add a parsing rule** in `backend/parser.py` to route matching intents to your tool:

```python
if "translate" in text_lower:
    return {
        "tool": "TranslatorTool",
        "arguments": {"text": user_input, "target_lang": "fr"}
    }
```
