import os
import warnings

# =============================
# ENV CONFIG
# =============================

os.environ["LITELLM_MODE"] = "client"
os.environ["LITELLM_DISABLE_LOGGING"] = "true"
os.environ["LITELLM_LOG"] = "ERROR"
os.environ["LITELLM_LOG_LEVEL"] = "ERROR"
os.environ["CREWAI_TRACING_ENABLED"] = "false"

warnings.filterwarnings("ignore")

# =============================
# IMPORTS
# =============================

from fastapi import FastAPI
from pydantic import BaseModel

from crewai import Crew
from agents.planner_agent import create_planner_agent
from tasks.planning_tasks import create_planning_task
from tools.resource_checker import ResourceChecker

# =============================
# FASTAPI APP
# =============================

app = FastAPI(
    title="Healthcare Planning Agent API"
)

# =============================
# REQUEST MODEL
# =============================

class PlanRequest(BaseModel):
    patient_name: str | None = None
    age: int | None = None
    condition: str | None = None
    priority: str | None = None
    requirements: str


# =============================
# CORE PLANNER FUNCTION
# =============================

def run_planner(goal: str):

    planner = create_planner_agent()

    planning_task = create_planning_task(planner, goal)

    crew = Crew(
        agents=[planner],
        tasks=[planning_task],
        verbose=False
    )

    result = crew.kickoff()

    checker = ResourceChecker()

    resource_status = []

    for line in str(result).split("\n"):

        line = line.strip()

        if not line:
            continue

        clean_line = line.replace("*", "")

        if clean_line.lower().startswith("step") and ":" in clean_line:

            status = checker.check_resources(clean_line)

            resource_status.append({
                "step": clean_line,
                "available": status
            })

    return {
        "summary": str(result),
        "resource_check": resource_status
    }


# =============================
# API ENDPOINT
# =============================

@app.post("/plan")
async def generate_plan(data: PlanRequest):

    result = run_planner(data.requirements)

    return result


# Optional health check
@app.get("/")
async def root():
    return {"status": "Healthcare Planning API running"}