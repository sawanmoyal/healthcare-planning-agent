"""
Streamlit Frontend for Healthcare Planning Agent
Compatible with new FastAPI main.py
"""

import streamlit as st
import httpx
import pandas as pd

# ============================
# CONFIG
# ============================

st.set_page_config(
    page_title="Healthcare Planning Agent",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

# ============================
# SESSION STATE
# ============================

if "results" not in st.session_state:
    st.session_state.results = None

# ============================
# API FUNCTIONS
# ============================

def check_backend():
    """Check if backend is alive"""
    try:
        r = httpx.get(f"{BACKEND_URL}/", timeout=5)
        return r.status_code == 200
    except:
        return False


def call_planning_agent(payload):

    url = f"{BACKEND_URL}/plan"

    try:
        response = httpx.post(url, json=payload, timeout=300)

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        st.error(f"❌ Connection error: {e}")
        st.info("Make sure FastAPI backend is running: uvicorn main:app --reload")
        return None

    except httpx.HTTPStatusError as e:
        st.error(f"❌ API Error: {e.response.text}")
        return None


# ============================
# SIDEBAR
# ============================

st.sidebar.title("🧠 Healthcare Agent")

# Backend status indicator
if check_backend():
    st.sidebar.success("Backend Connected")
else:
    st.sidebar.error("Backend NOT running")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Input Form", "Results"]
)

# ============================
# HOME
# ============================

if page == "Home":

    st.title("🏥 Healthcare Planning Agent")

    st.markdown("""
    Generate AI-powered healthcare plans using CrewAI.

    Steps:

    1️⃣ Enter patient details  
    2️⃣ Submit planning goal  
    3️⃣ View generated plan
    """)

# ============================
# INPUT FORM
# ============================

elif page == "Input Form":

    st.title("📝 Patient Input")

    with st.form("planner_form"):

        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=0, max_value=120)

        with col2:
            condition = st.text_input("Medical Condition")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])

        requirements = st.text_area(
            "Healthcare Goal *",
            placeholder="Example: 1 week hypertension plan"
        )

        submit = st.form_submit_button("Generate Plan")

    if submit:

        if not requirements:
            st.warning("Healthcare goal is required.")
        else:

            payload = {
                "patient_name": patient_name,
                "age": age,
                "condition": condition,
                "priority": priority,
                "requirements": requirements
            }

            with st.spinner("AI Agent thinking..."):

                result = call_planning_agent(payload)

                if result:
                    st.session_state.results = result
                    st.success("Plan generated successfully!")

# ============================
# RESULTS
# ============================

elif page == "Results":

    st.title("📊 Agent Results")

    result = st.session_state.results

    if not result:
        st.warning("No results yet. Generate a plan first.")
    else:

        tabs = st.tabs(["Summary", "Resource Check", "Raw JSON"])

        # SUMMARY
        with tabs[0]:

            st.subheader("Generated Plan")

            st.write(result.get("summary", "No summary available"))

        # RESOURCE CHECK
        with tabs[1]:

            resource_data = result.get("resource_check", [])

            if resource_data:
                df = pd.DataFrame(resource_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No resource check data.")

        # RAW JSON
        with tabs[2]:

            st.json(result)