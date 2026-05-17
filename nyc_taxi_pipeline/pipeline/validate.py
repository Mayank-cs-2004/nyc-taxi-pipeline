def validate(df):
    print("[validate] Running checks...")
    issues = []

    null_counts = df.isnull().sum()
    nulls = null_counts[null_counts > 0]
    if not nulls.empty:
        issues.append(f"Nulls found: {nulls.to_dict()}")

    if (df["trip_distance"] < 0).any():
        issues.append("Negative trip distances found")

    if (df["fare_amount"] < 0).any():
        issues.append("Negative fare amounts found")

    if (df["passenger_count"] == 0).any():
        issues.append("Trips with 0 passengers found")

    for issue in issues:
        print(f"  [WARN] {issue}")

    print(f"[validate] Done. {len(issue)} issue(s) found.")
    return issues
