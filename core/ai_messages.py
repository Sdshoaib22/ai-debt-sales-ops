import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sms(row):
    prompt = f"""
You are a debt consolidation agent. Write a short, friendly SMS (max 320 chars).
Goal: Get the person to reply YES and confirm a time to talk.

Include:
- First name
- One benefit
- Soft CTA (ask for best time today)
- No pressure, no shame

Lead:
Name: {row.get('first_name')}
Debt: {row.get('debt_amount')}
Income: {row.get('income_monthly')}
Priority: {row.get('priority')}
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return res.choices[0].message.content.strip()

def generate_email(row):
    prompt = f"""
You are a debt consolidation agent. Write a professional email.
Goal: Book a 10–15 min call.

Must include:
- Subject line
- Short intro
- 2-3 bullets of benefits (lower payment, simplify, reduce stress)
- Clear CTA + 2 time options
- Warm, non-judgmental tone

Lead:
Name: {row.get('first_name')} {row.get('last_name')}
City: {row.get('city')}
Debt: {row.get('debt_amount')}
Income: {row.get('income_monthly')}
Priority: {row.get('priority')}
Conversion Score: {row.get('conversion_score')}%
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return res.choices[0].message.content.strip()
