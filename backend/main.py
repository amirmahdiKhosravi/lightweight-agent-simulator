from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import TaskRequest, AgentResponse
from agent import Agent
import database

# Use lifespan to initialize the database when the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = FastAPI(title="Lightweight Agent Simulator API", lifespan=lifespan)

# Critical: Allow React to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate our core agent logic
agent_controller = Agent()

@app.post("/api/tasks", response_model=AgentResponse)
def execute_agent_task(request: TaskRequest):
    """
    Receives a task, runs the agentic pipeline, saves to DB, and returns the trace.
    """
    # 1. Run the agent logic
    result = agent_controller.execute_task(request.task)
    
    # 2. Save the results to SQLite
    database.save_task(
        user_input=request.task,
        final_output=result["final_output"],
        tools_used=result["tools_used"],
        execution_steps=result["execution_steps"]
    )
    
    # 3. Return the payload to the frontend
    return result

@app.get("/api/tasks")
def get_task_history():
    """
    Retrieves the history of all executed tasks.
    """
    return database.get_all_tasks()
