import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
    TARGET_PHONE_NUMBER = os.getenv("TARGET_PHONE_NUMBER")
    API_URL = "https://dummyjson.com/products"

config = Config()