from crewai import Task


def create_planning_task(agent, goal):

    description = f"""
    You are given this healthcare goal:

    "{goal}"

    Your job is to:

    1. First identify the main medical condition from the goal.
    2. Focus ONLY on that condition.
    3. Generate a clinical plan specific to it.
    4. Include:
       - Symptoms assessment
       - Diagnosis
       - Treatment
       - Medication
       - Monitoring
       - Follow-up
    5. Avoid generic healthcare workflows.
    6. Do NOT include unrelated diseases.

    Output format:

    Step 1: ...
    Step 2: ...
    Step 3: ...
    Step 4: ...
    Step 5: ...

    Make sure every step relates to "{goal}".
    """

    return Task(
        description=description,
        agent=agent,
        expected_output="A disease-specific clinical execution plan"
    )
