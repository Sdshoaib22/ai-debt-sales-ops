import streamlit as st
import pandas as pd
from core.clean import normalize
from core.dedup import deduplicate
from core.scoring import add_priority
from core.revenue_engine import calculate_revenue
from core.crm_connector import push_to_crm
from core.ai_summary import generate_customer_insight, generate_call_strategy
from core.db import log_activity

st.set_page_config(page_title="AI Debt Sales Operations", layout="wide")

st.title("🚀 AI Debt Sales Operations System")

uploaded_file = st.file_uploader("Upload lead Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is None:
    st.info("Upload an Excel file to start analysis.")
    st.stop()

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_excel(uploaded_file)

df = normalize(df)
df = deduplicate(df)
df = add_priority(df)

# -----------------------
# DASHBOARD METRICS
# -----------------------
st.subheader("📊 Lead Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Leads", len(df))
col2.metric("🔥 HOT", len(df[df["priority"] == "HOT"]))
col3.metric("🌤 WARM", len(df[df["priority"] == "WARM"]))
col4.metric("❄ COLD", len(df[df["priority"] == "COLD"]))

# -----------------------
# REVENUE FORECAST
# -----------------------
st.subheader("💰 Revenue Forecast")

total_revenue, avg_per_lead = calculate_revenue(df)

r1, r2 = st.columns(2)
r1.metric("Total Expected Revenue", f"${total_revenue:,.2f}")
r2.metric("Average Expected Per Lead", f"${avg_per_lead:,.2f}")

# -----------------------
# CRM EXPORT
# -----------------------
st.subheader("📤 CRM Export")

if st.button("Push HOT Leads to CRM"):
    hot_leads = df[df["priority"] == "HOT"]
    push_to_crm(hot_leads)
    st.success(f"{len(hot_leads)} HOT leads pushed to CRM.")

# -----------------------
# AI INSIGHTS SECTION
# -----------------------
st.subheader("🤖 AI Lead Intelligence")

for index, row in df.iterrows():
    with st.container():
        st.markdown("---")
        colA, colB = st.columns([2, 1])

        with colA:
            st.markdown(f"### {row.get('first_name','')} {row.get('last_name','')}")
            st.write(f"📍 City: {row.get('city','')}")
            st.write(f"💰 Debt: ${row.get('debt_amount','')}")
            st.write(f"💵 Income: ${row.get('income_monthly','')}")
            st.write(f"🔥 Priority: {row.get('priority','')}")

        with colB:
            insight_btn = st.button(f"Generate Insight {index}")
            call_btn = st.button(f"Call Strategy {index}")

        if insight_btn:
            with st.spinner("Generating AI insight..."):
                insight = generate_customer_insight(row)
                st.success(insight)
                log_activity("insight_generated", row)

        if call_btn:
            with st.spinner("Generating call strategy..."):
                strategy = generate_call_strategy(row)
                st.info(strategy)
                log_activity("call_strategy_generated", row)


