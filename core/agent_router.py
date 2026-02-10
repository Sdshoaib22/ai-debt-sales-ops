def assign_agents(df):
    agents = ["Agent_Ali", "Agent_Sara", "Agent_David", "Agent_Omar"]
    df = df.copy()

    # Separate by priority
    hot = df[df["priority"] == "HOT"]
    warm = df[df["priority"] == "WARM"]
    cold = df[df["priority"] == "COLD"]

    def distribute(leads):
        for i, idx in enumerate(leads.index):
            df.loc[idx, "assigned_agent"] = agents[i % len(agents)]

    distribute(hot)
    distribute(warm)
    distribute(cold)

    return df
