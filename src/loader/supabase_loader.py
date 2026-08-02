from supabase import create_client, Client
from config.settings import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def upsert_to_supabase(df_cleaned):
    """Upsert clean DataFrame records into Supabase PostgreSQL"""
    print("💾 [Load] Upserting records into Supabase Data Warehouse...")
    records = df_cleaned.to_dict(orient="records")

    try:
        response = supabase.table("products").upsert(records).execute()
        rows_count = len(records)
        print(f"🎉 [Load] Successfully upserted {rows_count} records.")
        return rows_count
    except  Exception as e:
        print(f"❌ [Load Error] Database operation failed: {e}")
        return 0