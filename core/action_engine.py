def assign_action(row):
    priority = row.get("priority")
    score = row.get("conversion_score", 0)

    if priority == "HOT" and score >= 70:
        return "🚨 Call Immediately (Within 1 Hour)"

    if priority == "HOT":
        return "📞 Call Today"

    if priority == "WARM" and score >= 60:
        return "📅 Follow Up Within 24 Hours"

    if priority == "WARM":
        return "📆 Follow Up This Week"

    return "🕒 Low Priority - Nurture"

def add_action_labels(df):
    df = df.copy()
    df["recommended_action"] = df.apply(assign_action, axis=1)
    return df
