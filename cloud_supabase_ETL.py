import os
import requests
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
TARGET_PHONE_NUMBER = os.getenv("TARGET_PHONE_NUMBER")

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL,SUPABASE_KEY)


def extract_data():
    """Step 1: EXTRACT - Fetch raw dproduct data from E-Commerce API"""
    print("🔄 1. Fetching raw data from API...")
    url = "https://dummyjson.com/products"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        raw_products = data.get("products", [])
        print(f"✅ Successfully fetched {len(raw_products)} raw records. \n")
        return raw_products
    else:
        print(f"❌ Failed to fetch data. Status code: {response.status_code}")
        return[]

def transform_data(raw_products):
    """Step 2: TRANSFORM - Clean, filter, and process data using Pandas"""
    print("🧹 2. Cleaning and transforming data with Pandas...")

    df = pd.DataFrame(raw_products)

    selected_columns = [
        "id",
        "title",
        "category",
        "price",
        "discountPercentage",
        "stock",
    ]
    df = df[selected_columns]

    # Calculate final price
    df["final_price"] = df["price"] * (1-df["discountPercentage"] / 100)
    df["final_price"] = df["final_price"].round(2)

    # Filter out out-of-stock items
    df_cleaned =  df[df["stock"]>0].copy()


    # Standardize column names matching Supabase schema
    df_cleaned.rename(
        columns={"discountPercentage": "discount_pct", "title": "product_name"},
        inplace=True,
    )

    print("✅ Data cleaning complete!\n")
    return df_cleaned


def load_to_supabase(df_cleaned):
    """Step 3: LOAD - Upsert cleaned data directly into Supabase PostgreSQL"""
    print("💾 3. Upserting data into Supabase Data Warehouse...")

    # Convert DataFrame records into a list of dictionaries for SQL ingestion
    records = df_cleaned.to_dict(orient="records")

    try:
        #'upsert' insert new records and updates existing ones based on primary key ('id')
        response = supabase.table("products").upsert(records).execute()
        rows_inserted = len(records)
        print(
            f"🎉 Successfully ingester {rows_inserted} into Supabase 'products' table! \n"
        )
        return rows_inserted
    except Exception as e:
        print(f"❌ Database insertion Error: {e}\n")
        return 0

def send_whatsapp_alert(inserted_count):
    """Step 4: ALERTING - Send pipeline summary report via Fonnte WhatsApp API"""
    print("📲 4. Sending execution status report to WhatsApp...")

    if not FONNTE_TOKEN or not TARGET_PHONE_NUMBER:
        print("⚠️ WhatsApp alert skipped: Fonnte token or phone number missing in .env")
        return

    url = "https://api.fonnte.com/send"
    headers = {"Authorization": FONNTE_TOKEN}

    message = (
        f"📊 *DATA PIPELINE EXECUTION REPORT*\n"
        f"-----------------------------------\n"
        f"✅ Status: SUCCESS\n"
        f"📦 Destination: Supabase DB (products)\n"
        f"📈 Total Rows Processed: {inserted_count}\n"
        f"-----------------------------------\n"
        f"🤖 Automated via Python ETL Pipeline"
    )      

    payload = {
        "target": TARGET_PHONE_NUMBER, 
        "message": message
    }

    try:
        res = requests.post(url,  headers=headers, data=payload)
        print(f"🔍 Fonnte Raw Response: {res.text}")
    except Exception as e:
        print(f"❌ WhatsApp API Error: {e}")

# --- MAIN EXECUTION PIPELINE ---
if __name__  == "__main__":
    print("=== STARTING ETL PIPELINE (CLOUD & ALERTING) ===\n")

    raw_data =  extract_data()

    if raw_data:
        cleaned_data = transform_data(raw_data)
        rows_processed = load_to_supabase(cleaned_data)

        if rows_processed > 0:
            send_whatsapp_alert(rows_processed)
    else:
        print("Pipeline aborted: Raw data payload is empty")
