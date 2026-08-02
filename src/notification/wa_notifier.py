import requests
from config.settings import config

def send_pipeline_report(status: str, total_rows: int, error_message: str = ""):
    """Send execution summary notification via Fonnte WhatsApp API"""
    print("📲 [Notification] Dispatching WhatsApp report...")

    if not config.FONNTE_TOKEN or not config.TARGET_PHONE_NUMBER:
        print("⚠️ [Notification Skipped] Missing Fonnte credentials in .env")
        return

    headers = {"Authorization": config.FONNTE_TOKEN}

    if status == "SUCCESS":
        message = (
            f"📊 *DATA PIPELINE REPORT [SUCCESS]*\n"
            f"-----------------------------------\n"
            f"✅ Status: PASSED ALL DQ CHECKS\n"
            f"📦 Destination: Supabase DB (products)\n"
            f"📈 Total Rows Processed: {total_rows}\n"
            f"-----------------------------------\n"
            f"🤖 Automated Modular ETL Pipeline"
        )
    else:
        message = (
            f"🚨 *DATA PIPELINE ALERT [FAILED]*\n"
            f"-----------------------------------\n"
            f"❌ Status: DATA QUALITY FAILURE / ERROR\n"
            f"⚠️ Details: {error_message}\n"
            f"-----------------------------------\n"
            f"🤖 Automated Modular ETL Pipeline"
        )

    payload = {"target": config.TARGET_PHONE_NUMBER, "message": message}

    try:
        res = requests.post("https://api.fonnte.com/send", headers=headers, data=payload)
        print("✅ [Notification] WhatsApp alert dispatched successfully.")
    except Exception as e:
        print (f"❌ [Notification Error] Failed to send WA message: {e}")