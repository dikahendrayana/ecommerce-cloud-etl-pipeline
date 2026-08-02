import requests
import pandas as pd

def extract_data():
    """First step : EXTRACT - Fetching raw data from E-commerce API"""
    print("1. 🔄 Fetch raw data from API...")
    url = "https://dummyjson.com/products"

    response = requests.get(url)


    #Check whether request success (Status Code 200)
    if response.status_code==200:
        data = response.json()
        #Fetching list 'products' from JSON's response
        raw_products = data.get("products", [])
        print(f"✅ Successfully fetched {len(raw_products)} raw records.\n")
        return raw_products
    else:
        print(f"❌ failed to fetch data. Status code: {response.status_code}")
        return[]

def transform_data(raw_products):
        """Step 2: TRANSFORM - Clean, filter, and process data using Pandas"""
        print("🧹 2. Cleaning and transforming data with Pandas...")

        #Convert list of JSON objects/dictionaries into Pandas DataFrame
        df = pd.DataFrame(raw_products)


        #a. Select relevant columns for the Data Warehouse schema
        selected_columns = ["id", "title", "category", "price", "discountPercentage", "stock"]
        df = df[selected_columns]

        #b. Business Logic: Calculate final price after discount & round to 2 decimal place
        df["final_price"] = df["price"] * (1 - df["discountPercentage"] / 100)
        df["final_price"] = df["final_price"].round(2)

        #c. Data Quality Check: Filter out out-of-stock items
        df_cleaned = df[df["stock"]>0].copy(0)

        #d. Standardize column names (snake_case convention)
        df_cleaned.rename(columns={
            "discountPercentage": "discount_pct",
            "title": "product_name"
        }, inplace=True)

        print("✅ Data cleaning complete!")
        print("\n--- Preview: Top 5 Cleaned Records ---")
        print(df_cleaned.head())
        print("-------------------------------------\n")

        return df_cleaned

def load_data(df_cleaned, file_name="products_clean.csv"):
    """Step 3: LOAD - Save cleaned data to a local CSV target"""
    print(f"💾 3. Exporting cleaned data to '{file_name}'...")

    #Save to CSV without exporting the default Pandas index
    df_cleaned.to_csv(file_name, index=False)
    print("🎉 Pipeline finished successfully! Data is ready for analysis. \n")


# --- MAIN EXECUTION PIPELINE ---
if  __name__ == "__main__":
    print("=== STARTING ETL PIPELINE ===\n")

    # Execute ETL Stages
    raw_data = extract_data()

    if raw_data:
        cleaned_data = transform_data(raw_data)
        load_data(cleaned_data)
    else:
        print("Pipeline aborted: Raw data payload is empty")