class ResourceChecker:

    def __init__(self):

        # Structured Dummy Healthcare Resources
        self.resources = {

            # Medical
            "assessment": ["assessment", "needs assessment", "evaluation"],
            "diagnosis": ["diagnosis", "diagnostic", "testing"],
            "laboratory": ["lab", "laboratory", "blood test", "urine test"],
           "medication": ["medication", "medicine", "drug", "insulin", "metformin", "tablet"],
            "monitoring": ["monitor", "tracking", "follow-up", "checkup"],
            "treatment": ["therapy", "treatment", "intervention"],

            # Planning & Management
            "planning": ["plan", "strategy", "framework", "roadmap"],
            "management": ["management", "project", "coordination"],
           "scheduling": [
    "schedule",
    "scheduling",
    "scheduler",
    "timeline",
    "calendar",
    "patient flow",
    "queue",
    "appointment",
    "booking"
],
"systems": [
    "system",
    "software",
    "platform",
    "application",
    "dashboard",
    "tool"
],

            "review": ["review", "evaluation", "audit"],

            # Staff
            "doctors": ["doctor", "physician", "specialist"],
            "nurses": ["nurse", "caretaker"],
            "staff": ["staff", "team", "workforce"],

            # Education & Lifestyle
            "education": ["education", "training", "awareness"],
            "lifestyle": ["diet", "exercise", "fitness", "stress"],

            # Infrastructure
            "equipment": ["equipment", "machine", "device"],
            "records": ["records", "ehr", "documentation"],
            "communication": ["communication", "meeting", "discussion"]
        }


    def check_resources(self, task):

        task_lower = task.lower()

        # Search in all categories
        for category in self.resources:
            for keyword in self.resources[category]:
                if keyword in task_lower:
                    return True

        return False
