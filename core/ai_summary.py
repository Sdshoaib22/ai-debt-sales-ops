import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# 1️⃣ AI CUSTOMER INSIGHT
# -----------------------------
def generate_customer_insight(row):

    prompt = f"""
You are a financial risk analyst.

Analyze this lead and provide:

1. Income stability analysis
2. Debt burden evaluation
3. Likelihood to repay
4. Risk level (Low / Medium / High)
5. Short summary assessment

Lead Data:
Name: {row.get('first_name')} {row.get('last_name')}
City: {row.get('city')}
Debt Amount: {row.get('debt_amount')}
Income: {row.get('income_monthly')}
Priority: {row.get('priority')}
Conversion Score: {row.get('conversion_score')}%
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content


# -----------------------------
# 2️⃣ AI CALL STRATEGY
# -----------------------------
def generate_call_strategy(row):

    prompt = f"""
You are a senior debt consolidation sales strategist.

Generate:

1. Best opening line
2. Likely objection
3. Emotional leverage angle
4. Urgency strategy
5. Closing recommendation

Lead Data:
Name: {row.get('first_name')} {row.get('last_name')}
Debt Amount: {row.get('debt_amount')}
Income: {row.get('income_monthly')}
Priority: {row.get('priority')}
Conversion Score: {row.get('conversion_score')}%
Expected Revenue: {row.get('expected_revenue')}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content

