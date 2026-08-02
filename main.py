from src.ingestion.scraper import fetch_raw_products
from src.transformation.cleaner import transform_products
from src.transformation.data_quality import validate_product_data
from src.loader.supabase_loader import upsert_to_supabase
from src.notification.wa_notifier import send_pipeline_report

def run_pipeline():
    print("=== STARTING MODULAR DATA PIPELINE ===\n")

    # 1. EXTRACT
    raw_data = fetch_raw_products()
    if not raw_data:
        send_pipeline_report(status="FAILED", total_rows=0, error_message="Empty rows")
        return

    # 2. TRANSFORM
    cleaned_df = transform_products(raw_data)

    # 3. DATA QUALITY CHECKS
    is_valid = validate_product_data
    if not is_valid:
        send_pipeline_report(status="FAILED", total_rows=0, error_message="Data Quality Assertion failed")
        return

    # 4. LOAD
    rows_upserted = upsert_to_supabase(cleaned_df)

    # 5. NOTIFY
    if rows_upserted > 0:
        send_pipeline_report(status="SUCCESS", total_rows=rows_upserted)
    else:
        send_pipeline_report(status="FAILED", total_rows=0, error_message="Database ingestion failed")

if __name__ == "__main__":
    run_pipeline()