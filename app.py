import streamlit as st
import pandas as pd
from datetime import datetime

from core.ingest import load_excel
from core.clean import normalize
from core.dedup import deduplicate
from core.scoring import add_priority
from core.ml_model import add_ml_score
from core.action_engine import add_action_labels
from core.agent_router import assign_agents
from core.revenue_engine import add_revenue_projection

from core.ai_summary import generate_customer_insight, generate_call_strategy
from core.ai_messages import generate_sms, generate_email

from core.crm_connector import push_to_crm
from core.db import init_db, upsert_lead, fetch_all_leads, update_field
from core.id_utils import make_lead_id

st.set_page_config(page_title="AI Debt Sales Ops", layout="wide")

st.title("🚀 AI Debt Sales Operations System")

init_db()

# ---------------------------------------------------------
# Upload Required Before Showing Anything
# ---------------------------------------------------------
file = st.file_uploader("Upload lead Excel file (.xlsx)", type=["xlsx", "xls"])

if not file:
    st.info("📂 Please upload an Excel file to begin.")
    st.stop()

# ---------------------------------------------------------
# Process Uploaded File
# ---------------------------------------------------------
try:
    df = load_excel(file)
except:
    st.error("Error reading Excel file.")
    st.stop()

df_clean = normalize(df)
df_clean = deduplicate(df_clean)
df_clean = add_priority(df_clean)
df_clean = add_ml_score(df_clean)
df_clean = add_action_labels(df_clean)
df_clean = assign_agents(df_clean)
df_clean = add_revenue_projection(df_clean)

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for _, r in df_clean.iterrows():

    lead_id = make_lead_id(
        r.get("email"),
        r.get("phone"),
        r.get("first_name"),
        r.get("last_name")
    )

    upsert_lead({
        "lead_id": lead_id,
        "first_name": r.get("first_name"),
        "last_name": r.get("last_name"),
        "phone": r.get("phone"),
        "email": r.get("email"),
        "city": r.get("city"),
        "debt_amount": float(r.get("debt_amount") or 0),
        "income_monthly": float(r.get("income_monthly") or 0),
        "priority": r.get("priority"),
        "conversion_score": float(r.get("conversion_score") or 0),
        "expected_revenue": float(r.get("expected_revenue") or 0),
        "recommended_action": r.get("recommended_action"),
        "assigned_agent": r.get("assigned_agent"),
        "status": "Open",
        "created_at": now_str,
        "last_updated": now_str,
        "ai_insight": None,
        "ai_strategy": None,
        "ai_sms": None,
        "ai_email": None
    })

# ---------------------------------------------------------
# Fetch Fresh Data (Only After Upload)
# ---------------------------------------------------------
db_leads = fetch_all_leads()

if len(db_leads) == 0:
    st.warning("No leads available.")
    st.stop()

df_clean = pd.DataFrame(db_leads)

# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
st.subheader("📊 Lead Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", len(df_clean))
col2.metric("🔥 HOT", len(df_clean[df_clean["priority"] == "HOT"]))
col3.metric("🌤 WARM", len(df_clean[df_clean["priority"] == "WARM"]))
col4.metric("❄ COLD", len(df_clean[df_clean["priority"] == "COLD"]))

st.divider()

# ---------------------------------------------------------
# REVENUE FORECAST
# ---------------------------------------------------------
st.subheader("💰 Revenue Forecast")

colA, colB = st.columns(2)
colA.metric("Total Expected Revenue",
            f"${round(df_clean['expected_revenue'].sum(),2)}")

colB.metric("Average Expected Per Lead",
            f"${round(df_clean['expected_revenue'].mean(),2)}")

st.divider()

# ---------------------------------------------------------
# LEAD CARDS
# ---------------------------------------------------------
st.subheader("📇 Lead Details")

for idx, row in df_clean.iterrows():

    with st.container():

        colA, colB = st.columns([3,1])
        lead_id = row["lead_id"]

        with colA:
            st.markdown(f"### {row['first_name']} {row['last_name']}")
            st.write(f"Debt: ${row['debt_amount']}")
            st.write(f"Income: ${row['income_monthly']}")
            st.write(f"Expected Revenue: ${round(row['expected_revenue'],2)}")
            st.write(f"Assigned Agent: {row['assigned_agent']}")

            # Status update
            new_status = st.selectbox(
                "Update Status",
                ["Open","Contacted","Closed","Lost"],
                index=["Open","Contacted","Closed","Lost"].index(row["status"]),
                key=f"status_{lead_id}"
            )

            if new_status != row["status"]:
                update_field(lead_id, "status", new_status)
                st.rerun()

            # AI Insight
            st.markdown("### 🤖 AI Customer Insight")

            if row["ai_insight"]:
                st.info(row["ai_insight"])

            if st.button("Generate Insight", key=f"insight_{lead_id}"):
                insight = generate_customer_insight(row)
                update_field(lead_id, "ai_insight", insight)
                st.rerun()

            # AI Strategy
            st.markdown("### 📞 AI Call Strategy")

            if row["ai_strategy"]:
                st.info(row["ai_strategy"])

            if st.button("Generate Strategy", key=f"strategy_{lead_id}"):
                strategy = generate_call_strategy(row)
                update_field(lead_id, "ai_strategy", strategy)
                st.rerun()

            # SMS
            st.markdown("### 📱 AI SMS Draft")

            if row["ai_sms"]:
                st.text_area("Saved SMS", row["ai_sms"], height=120, key=f"sms_{lead_id}")

            if st.button("Generate SMS", key=f"sms_gen_{lead_id}"):
                sms = generate_sms(row)
                update_field(lead_id, "ai_sms", sms)
                st.rerun()

            # Email
            st.markdown("### 📧 AI Email Draft")

            if row["ai_email"]:
                st.text_area("Saved Email", row["ai_email"], height=220, key=f"email_{lead_id}")

            if st.button("Generate Email", key=f"email_gen_{lead_id}"):
                email = generate_email(row)
                update_field(lead_id, "ai_email", email)
                st.rerun()

        with colB:
            if row["priority"] == "HOT":
                st.error("HOT")
            elif row["priority"] == "WARM":
                st.warning("WARM")
            else:
                st.info("COLD")

        st.divider()


