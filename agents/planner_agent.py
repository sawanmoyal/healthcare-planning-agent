import os
from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

def create_planner_agent():

    groq_key = os.getenv("GROQ_API_KEY")

    llm = LLM(
        model="groq/llama-3.1-8b-instant",
        api_key=groq_key,
        temperature=0.2,
        max_tokens=600
    )

    agent = Agent(
        role="Clinical Healthcare Planner Agent",

        goal="""
        You are a clinical planning assistant.

        IMPORTANT RULES:
        1. Always focus ONLY on the user's given healthcare goal.
        2. Never change the disease or condition.
        3. Never introduce unrelated illnesses.
        4. Base every step strictly on the input goal.

        Your task is to:
        - Analyze the given condition.
        - Break it into medical steps.
        - Include diagnosis, treatment, monitoring, and follow-up.
        - Identify dependencies.
        - Create a timeline.
        """,

backstory="""
You are an expert healthcare operations planner.
You decompose high-level medical goals into dependent tasks.
For each step, mention which previous step it depends on.
You generate optimized healthcare schedules.
""",

        llm=llm,
        verbose=False,
        allow_delegation=False
    )

    return agent
