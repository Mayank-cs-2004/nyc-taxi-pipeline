def validate(df):
    """Check data quality using Spark SQL"""
    print("[validate] Running checks...")
    issues = []
    
    # Check for nulls
    null_counts = df.select([(df[col].isNull().cast("int").alias(col)) for col in df.columns])
    null_summary = null_counts.describe().collect()
    
    for col in df.columns:
        null_count = df.filter(df[col].isNull()).count()
        if null_count > 0:
            issues.append(f"Nulls in {col}: {null_count:,}")
    
    # Check for negative values (where applicable)
    if "trip_distance" in df.columns:
        neg_distance = df.filter(df["trip_distance"] < 0).count()
        if neg_distance > 0:
            issues.append(f"Negative trip distances: {neg_distance:,}")
    
    if "fare_amount" in df.columns:
        neg_fare = df.filter(df["fare_amount"] < 0).count()
        if neg_fare > 0:
            issues.append(f"Negative fares: {neg_fare:,}")
    
    if "passenger_count" in df.columns:
        zero_passengers = df.filter(df["passenger_count"] == 0).count()
        if zero_passengers > 0:
            issues.append(f"Zero passenger trips: {zero_passengers:,}")
    
    for issue in issues:
        print(f"  [WARN] {issue}")
    
    print(f"[validate] Done. {len(issues)} issue(s) found.")
    return issues
