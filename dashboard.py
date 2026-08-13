import streamlit as st
import pandas as pd
import sqlite3


# -----------------------------
# Database Connection
# -----------------------------

conn = sqlite3.connect("nextgen.db")


# -----------------------------
# Load Tables
# -----------------------------

applicants = pd.read_sql(
    "SELECT * FROM applicants",
    conn
)

interns = pd.read_sql(
    "SELECT * FROM interns",
    conn
)

scores = pd.read_sql(
    "SELECT * FROM hackathon_scores",
    conn
)


# -----------------------------
# Dashboard Title
# -----------------------------

st.title("NextGenLearners Program Performance Dashboard")

st.write(
    "Interactive dashboard for internship program performance analysis"
)


# -----------------------------
# Domain Filter
# -----------------------------

domain_list = ["All"] + sorted(
    applicants["domain"].unique().tolist()
)


selected_domain = st.selectbox(
    "Filter by Domain",
    domain_list
)


# Apply Filter

if selected_domain != "All":

    applicants_filtered = applicants[
        applicants["domain"] == selected_domain
    ]

    interns_filtered = interns[
        interns["domain"] == selected_domain
    ]

else:

    applicants_filtered = applicants
    interns_filtered = interns



# -----------------------------
# Program Overview Metrics
# -----------------------------

st.subheader("Program Overview")


col1, col2 = st.columns(2)


col1.metric(
    "Total Applicants",
    len(applicants_filtered)
)


completed_interns = len(
    interns_filtered[
        interns_filtered["completion_status"] == "Completed"
    ]
)


col2.metric(
    "Completed Interns",
    completed_interns
)



# -----------------------------
# Completion Rate Chart
# -----------------------------

st.subheader(
    "Completion Rate Per Domain"
)


completion_rate = pd.read_sql(
    """

    SELECT

    domain,

    COUNT(*) AS completed_count


    FROM interns


    WHERE completion_status = 'Completed'


    GROUP BY domain


    ORDER BY completed_count DESC;


    """,

    conn
)


st.bar_chart(
    completion_rate.set_index("domain")
)



# -----------------------------
# Average Hackathon Score
# -----------------------------

st.subheader(
    "Average Hackathon Score Per Domain"
)


average_score = pd.read_sql(
    """

    SELECT

    domain,

    ROUND(AVG(score),2) AS avg_score


    FROM hackathon_scores


    GROUP BY domain;


    """,

    conn
)


st.bar_chart(
    average_score.set_index("domain")
)



# -----------------------------
# Top 10 Leaderboard
# -----------------------------

st.subheader(
    "Top 10 Performers Leaderboard"
)


leaderboard = pd.read_sql(
    """

    SELECT

    i.intern_id,

    i.domain,

    h.score


    FROM interns i


    JOIN hackathon_scores h


    ON i.intern_id = h.intern_id


    ORDER BY h.score DESC


    LIMIT 10;


    """,

    conn
)


st.dataframe(
    leaderboard
)


# Close Connection

conn.close()