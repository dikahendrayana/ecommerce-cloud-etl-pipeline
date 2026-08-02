import pandas as pd

def validate_product_data(df: pd.DataFrame)  -> bool:
    """Data Quality Framework: Validate data rules before database ingestion"""
    print("🔍 [Data Quality] Running assertion checks...")

    # Check 1: Ensure DataFrame is not empty
    if df.empty:
        print("❌ [Data Quality Failed] DataFrame is empty.")
        return False

    # Check 2: Null Primary Key Check
    if df["id"].isnull().any():
        print("❌ [Data Quality Failed] Found NULL values in Primary Key 'id'.")
        return False

    # Check 3: Negative Price Check
    if (df["final_price"]<0).any():
        print("❌ [Data Quality Failed] Found negative values in 'final_price'.")
        return False

    # Check 4: Duplicate Primary Key Check
    if df["id"].duplicated().any():
        print("❌ [Data Quality Failed] Found duplicate Primary Keys.")
        return False

    print("✅ [Data Quality Passed] All assertion checks passed!")
    return True