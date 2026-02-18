import os
import warnings

# Disable LiteLLM / CrewAI Logs
os.environ["LITELLM_MODE"] = "client"
os.environ["LITELLM_DISABLE_LOGGING"] = "true"
os.environ["LITELLM_LOG"] = "ERROR"
os.environ["LITELLM_LOG_LEVEL"] = "ERROR"
os.environ["CREWAI_TRACING_ENABLED"] = "false"

warnings.filterwarnings("ignore")

# Imports
from crewai import Crew
from agents.planner_agent import create_planner_agent
from tasks.planning_tasks import create_planning_task
from tools.resource_checker import ResourceChecker


# Main Function
def main():

    print("\n=== Healthcare Planning Assistant ===\n")

    # Take input
    goal = input("Enter Healthcare Goal: ").strip()

    if not goal:
        print("❌ Goal cannot be empty.")
        return

    # Create Agent
    planner = create_planner_agent()

    # Create Task
    planning_task = create_planning_task(planner, goal)

    # Create Crew
    crew = Crew(
        agents=[planner],
        tasks=[planning_task],
        verbose=False
    )

    
    result = crew.kickoff()   #result

    # Print Generated Plan
    print("\n=== Generated Plan ===\n")
    print(result)

    # Resource Checking
    checker = ResourceChecker()

    print("\n=== Resource Check ===\n")

    for line in str(result).split("\n"):

        line = line.strip()

        if not line:
            continue

        # Remove markdown
        clean_line = line.replace("*", "")

        # Only check main steps
        if clean_line.lower().startswith("step") and ":" in clean_line:

            status = checker.check_resources(clean_line)

            print(f"{clean_line} -> {'Available' if status else 'Not Available'}")


# Run Program
if __name__ == "__main__":
    main()
