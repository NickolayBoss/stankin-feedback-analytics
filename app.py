"""Read-only Streamlit dashboard for the synthetic feedback analytics demo."""
import os
import pandas as pd
import psycopg
import streamlit as st

st.set_page_config(page_title="STANKIN Feedback Intelligence", page_icon="📊", layout="wide")
st.title("STANKIN Feedback Intelligence")
st.caption("Independent portfolio demo · synthetic records · not an official university service")

@st.cache_data(ttl=60)
def query(sql: str) -> pd.DataFrame:
    with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=5) as conn:
        return pd.read_sql_query(sql, conn)

try:
    overview = query("SELECT * FROM kpi_overview").iloc[0]
    departments = query("SELECT * FROM department_performance ORDER BY tickets DESC")
    trends = query("""
        SELECT date_trunc('week', created_at AT TIME ZONE 'Europe/Moscow')::date AS week,
               category, count(*) AS tickets
        FROM feedback GROUP BY 1, 2 ORDER BY 1
    """)
    backlog = query("""
        SELECT category, count(*) AS open_tickets,
               count(*) FILTER (WHERE created_at < now() - interval '72 hours') AS overdue
        FROM feedback WHERE status <> 'resolved'
        GROUP BY category ORDER BY open_tickets DESC
    """)
except (psycopg.Error, KeyError, IndexError) as exc:
    st.error("Database unavailable. Start Docker Compose and check DATABASE_URL.")
    st.code(str(exc))
    st.stop()

a, b, c, d = st.columns(4)
a.metric("Total feedback", int(overview["total"]))
b.metric("Resolved (%)", f'{overview["resolution_pct"]:.1f}%')
c.metric("Response SLA · answered (%)", f'{overview["answered_within_24h_pct"]:.1f}%')
d.metric("Median response (hours)", f'{overview["median_response_hours"]:.1f}')

st.subheader("Weekly volume by category")
if not trends.empty:
    pivot = trends.pivot(index="week", columns="category", values="tickets").fillna(0)
    st.line_chart(pivot)
st.subheader("Department performance")
st.dataframe(departments, use_container_width=True, hide_index=True)
st.subheader("Unresolved backlog")
st.bar_chart(backlog.set_index("category")[["open_tickets", "overdue"]])
st.caption("SLA denominator excludes unanswered tickets. Synthetic data is not representative.")
