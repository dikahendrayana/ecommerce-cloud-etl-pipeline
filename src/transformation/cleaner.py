import pandas as pd

def transform_products(raw_products):
    """Clean and transform raw product records using Pandas"""
    print("🧹 [Transform] Processing raw records with Pandas...")
    df = pd.DataFrame(raw_products)

    selected_columns = ["id", "title", "price", "discountPercentage", "stock"]
    df=df[selected_columns]

    df["final_price"]  = (df["price"] * (1 - df["discountPercentage"] / 100)).round(2)
    df_cleaned = df[df["stock"] > 0].copy()

    df_cleaned.rename(columns={
        "discountPercentage": "discount_pct",
        "title": "product_name"
    }, inplace=True)

    print("✅ [Transform] Data transformation completed successfully.")
    return df_cleaned