from sqlalchemy import create_engine, text

DB_URL = "sqlite:///leads.db"

engine = create_engine(DB_URL, future=True)


# ----------------------------------------------------
# Initialize Database
# ----------------------------------------------------
def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            email TEXT,
            city TEXT,
            debt_amount REAL,
            income_monthly REAL,
            priority TEXT,
            conversion_score REAL,
            expected_revenue REAL,
            recommended_action TEXT,
            assigned_agent TEXT,
            status TEXT,
            created_at TEXT,
            last_updated TEXT,
            ai_insight TEXT,
            ai_strategy TEXT,
            ai_sms TEXT,
            ai_email TEXT
        );
        """))


# ----------------------------------------------------
# Insert or Update Lead
# ----------------------------------------------------
def upsert_lead(lead: dict):

    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO leads (
            lead_id, first_name, last_name, phone, email, city,
            debt_amount, income_monthly, priority, conversion_score,
            expected_revenue, recommended_action, assigned_agent,
            status, created_at, last_updated,
            ai_insight, ai_strategy, ai_sms, ai_email
        ) VALUES (
            :lead_id, :first_name, :last_name, :phone, :email, :city,
            :debt_amount, :income_monthly, :priority, :conversion_score,
            :expected_revenue, :recommended_action, :assigned_agent,
            :status, :created_at, :last_updated,
            :ai_insight, :ai_strategy, :ai_sms, :ai_email
        )
        ON CONFLICT(lead_id) DO UPDATE SET
            first_name=excluded.first_name,
            last_name=excluded.last_name,
            phone=excluded.phone,
            email=excluded.email,
            city=excluded.city,
            debt_amount=excluded.debt_amount,
            income_monthly=excluded.income_monthly,
            priority=excluded.priority,
            conversion_score=excluded.conversion_score,
            expected_revenue=excluded.expected_revenue,
            recommended_action=excluded.recommended_action,
            assigned_agent=excluded.assigned_agent,
            status=excluded.status,
            last_updated=excluded.last_updated,
            ai_insight=COALESCE(excluded.ai_insight, leads.ai_insight),
            ai_strategy=COALESCE(excluded.ai_strategy, leads.ai_strategy),
            ai_sms=COALESCE(excluded.ai_sms, leads.ai_sms),
            ai_email=COALESCE(excluded.ai_email, leads.ai_email);
        """), lead)


# ----------------------------------------------------
# Fetch All Leads
# ----------------------------------------------------
def fetch_all_leads():
    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT * FROM leads ORDER BY last_updated DESC")
        ).mappings().all()

        return [dict(r) for r in rows]


# ----------------------------------------------------
# Update Specific Field (Safe)
# ----------------------------------------------------
def update_field(lead_id: str, field: str, value):

    allowed_fields = {
        "status",
        "ai_insight",
        "ai_strategy",
        "ai_sms",
        "ai_email"
    }

    if field not in allowed_fields:
        raise ValueError("Field update not allowed")

    with engine.begin() as conn:
        conn.execute(
            text(f"""
            UPDATE leads
            SET {field} = :value,
                last_updated = datetime('now')
            WHERE lead_id = :lead_id
            """),
            {"value": value, "lead_id": lead_id}
        )
