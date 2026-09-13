import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from database import DB_NAME

st.set_page_config(
    page_title="Campus Maintenance System",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 Campus Maintenance Complaint & Tracking System")

st.write(
    "Register, track and analyze campus maintenance complaints."
)

st.success("Streamlit application is working!")

st.subheader("📊 Dashboard")

connection = sqlite3.connect(DB_NAME)

complaints = pd.read_sql_query(
    "SELECT * FROM complaints",
    connection
)

maintenance = pd.read_sql_query(
    "SELECT * FROM maintenance",
    connection
)

connection.close()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Complaints", len(complaints))

with col2:
    pending = len(complaints[complaints["status"] == "Pending"])
    st.metric("Pending", pending)

with col3:
    resolved = len(complaints[complaints["status"] == "Resolved"])
    st.metric("Resolved", resolved)

st.subheader("📋 Complaint Records")

if not complaints.empty:
    st.dataframe(
        complaints[
            [
                "complaint_id",
                "student_name",
                "category",
                "building",
                "priority",
                "status",
                "date"
            ]
        ],
        use_container_width=True
    )
else:
    st.info("No complaints registered yet.")