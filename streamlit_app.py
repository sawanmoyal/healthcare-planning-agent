"""
Streamlit Frontend for Healthcare Planning Agent

Features:
- Sidebar Navigation
- Input Form with validation
- API calls to FastAPI backend
- Loading indicators
- Error handling
- Structured results display
"""

import streamlit as st
import httpx
import pandas as pd
import json
import time

# ============================
# CONFIG
# ============================

st.set_page_config(
    page_title="Healthcare Planning Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "http://localhost:8000"  # change if deployed

# ============================
# SESSION STATE INIT
# ============================

if "results" not in st.session_state:
    st.session_state.results = None

if "settings" not in st.session_state:
    st.session_state.settings = {
        "backend_url": BACKEND_URL
    }

# ============================
# API CLIENT FUNCTIONS
# ============================

def call_planning_agent(payload):
    """
    Calls FastAPI backend endpoint.
    Update endpoint path according to your API.
    """

    url = f"{st.session_state.settings['backend_url']}/plan"

    try:
        with httpx.Client(timeout=60) as client:

            response = client.post(url, json=payload)

            response.raise_for_status()

            return response.json()

    except httpx.RequestError as e:
        st.error(f"Connection error: {e}")
        return None

    except httpx.HTTPStatusError as e:
        st.error(f"API Error: {e.response.text}")
        return None


# ============================
# SIDEBAR NAVIGATION
# ============================

st.sidebar.title("🧠 Healthcare Agent")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Input Form", "Results", "Settings"]
)

# ============================
# HOME PAGE
# ============================

if page == "Home":

    st.title("🏥 Healthcare Planning Agent")

    st.markdown("""
    Welcome to the AI Healthcare Planner.

    This interface allows you to:

    - Enter patient data
    - Submit planning requests
    - View AI-generated healthcare plans
    """)

    st.info("Use the sidebar to start.")

# ============================
# INPUT FORM PAGE
# ============================

elif page == "Input Form":

    st.title("📝 Patient Input")

    with st.form("planner_form"):

        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input("Patient Name *")
            age = st.number_input("Age *", min_value=0, max_value=120)

        with col2:
            condition = st.text_input("Medical Condition *")
            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"]
            )

        requirements = st.text_area(
            "Planning Requirements / Goal *",
            placeholder="Example: Create treatment plan..."
        )

        submit = st.form_submit_button("Generate Plan")

    # FORM SUBMISSION
    if submit:

        # Validation
        if not patient_name or not condition or not requirements:
            st.warning("Please fill all required fields.")
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
# RESULTS PAGE
# ============================

elif page == "Results":

    st.title("📊 Agent Results")

    if not st.session_state.results:
        st.warning("No results yet. Generate a plan first.")
    else:

        result = st.session_state.results

        tabs = st.tabs(["Summary", "Structured Data", "Charts", "Raw JSON"])

        # --- Summary Tab
        with tabs[0]:

            if "summary" in result:
                st.subheader("Plan Summary")
                st.write(result["summary"])

        # --- Structured Data Tab
        with tabs[1]:

            if "steps" in result:
                df = pd.DataFrame(result["steps"])
                st.dataframe(df, use_container_width=True)

        # --- Charts Tab
        with tabs[2]:

            if "steps" in result:
                df = pd.DataFrame(result["steps"])

                if "duration" in df.columns:
                    st.bar_chart(df["duration"])

        # --- Raw JSON Tab
        with tabs[3]:
            st.json(result)

# ============================
# SETTINGS PAGE
# ============================

elif page == "Settings":

    st.title("⚙️ Settings")

    backend_url = st.text_input(
        "Backend URL",
        value=st.session_state.settings["backend_url"]
    )

    if st.button("Save Settings"):
        st.session_state.settings["backend_url"] = backend_url
        st.success("Settings saved.")