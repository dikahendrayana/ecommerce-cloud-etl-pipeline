import requests
from config.settings import config

def fetch_raw_products():
    """Fetch raw product payload from the E-Commerce API"""
    print("🔄 [Extract] Fetching raw data from API...")
    response = requests.get(config.API_URL)

    if response.status_code == 200:
        raw_data = response.json().get("products",[])
        print(f"✅ [Extract] Successfully fetched {len(raw_data)} raw records.")
        return raw_data
    else:
        print(f"❌ [Extract] API Request failed with status code: {response.status_code}")
        return[]
    