def add_revenue_projection(df):
    df = df.copy()

    # Assumptions
    qualification_factor = 0.70   # 70% of debt qualifies
    commission_rate = 0.08        # 8% realistic commission

    df["qualified_debt"] = df["debt_amount"] * qualification_factor
    df["estimated_deal_value"] = df["qualified_debt"] * commission_rate

    df["expected_revenue"] = (
        df["estimated_deal_value"] * (df["conversion_score"] / 100)
    )

    return df
