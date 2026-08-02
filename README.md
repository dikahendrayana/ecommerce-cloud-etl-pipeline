# 🛒 Automated E-Commerce Cloud ETL Pipeline

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/dikahendrayana/ecommerce-cloud-etl-pipeline/daily_etl.yml?branch=main&label=ETL%20Pipeline&style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg?style=flat-square)
![Database](https://img.shields.io/badge/database-Supabase%20%28PostgreSQL%29-green.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square)

An automated, cloud-based end-to-end Data Engineering pipeline built with **Python**, **Pandas**, and **Supabase (PostgreSQL)**, scheduled and orchestrated via **GitHub Actions**. 

This pipeline ingests e-commerce transaction data, performs data cleaning and transformation, loads it into a cloud data warehouse using idempotent `upsert` logic, and dispatches automated execution status reports directly to **WhatsApp**.

---

## 🏗️ System Architecture

```text
┌────────────────────────────────┐
│  E-Commerce Data Source        │
│  (REST API / Data Generator)   │
└───────────────┬────────────────┘
                │
                ▼ (1. Extract)
┌────────────────────────────────┐
│  Python Ingestion Service      │
└───────────────┬────────────────┘
                │
                ▼ (2. Transform)
┌────────────────────────────────┐
│  Pandas Data Processing        │
│  - Data Cleaning & Normalization
│  - Schema Validation           │
└───────────────┬────────────────┘
                │
                ▼ (3. Load)
┌────────────────────────────────┐
│  Supabase Data Warehouse       │
│  - PostgreSQL Engine           │
│  - Idempotent Upsert Strategy  │
└───────────────┬────────────────┘
                │
                ▼ (4. Monitor & Alert)
┌────────────────────────────────┐
│  Fonnte WhatsApp API           │
│  - Automated Execution Summary │
└────────────────────────────────┘
```

# ✨ Key Features & Engineering Highlights
- **Automated Cloud Orchestration**: Scheduled via GitHub Actions (cron) to run daily with zero manual intervention required.
- **Idempotent Upsert Strategy**: Configured primary key constraints on Supabase (PostgreSQL) to handle updates and insertions gracefully, preventing duplicate rows across execution cycles.
- **Modular Pipeline Architecture**: Clean separation of concerns with dedicated modules for extraction (Extract), transformation (Transform), loading (Load), and alerting (Notification).
- **Real-time Alerting System**: Integrated with Fonnte API to send automated WhatsApp notifications detailing execution statistics (records processed, errors, timestamps).
- **Production Credentials Management**: Strictly isolated using GitHub Repository Secrets and .env environment variables to protect sensitive API keys and database parameters.

# 🛠️ Tech Stack & Tools

| Component | Technology | Usage |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Core business logic & orchestration |
| **Data Processing** | Pandas | Data cleaning & structural transformation |
| **Data Warehouse** | Supabase (PostgreSQL) | Cloud database for structured e-commerce datasets |
| **Orchestration** | GitHub Actions | Scheduled cloud execution runner |
| **Alerting System** | Fonnte API | WhatsApp dispatch for operational monitoring |

---

# 📂 Project Structure

```text
ecommerce-cloud-etl-pipeline/
├── .github/
│   └── workflows/
│       └── daily_etl.yml       # GitHub Actions CI/CD pipeline definition
├── src/
│   ├── extract/                # Data extraction logic
│   ├── transform/              # Data cleaning and Pandas transformations
│   ├── loader/                 # Supabase database loader (Upsert)
│   ├── notification/           # WhatsApp alerting logic (Fonnte API)
│   └── config.py               # Environment configuration loader
├── main.py                     # Main execution entry point
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

```
# 🚀 Local Setup & Installation
git clone [https://github.com/dikahendrayana/ecommerce-cloud-etl-pipeline.git](https://github.com/dikahendrayana/ecommerce-cloud-etl-pipeline.git)
cd ecommerce-cloud-etl-pipeline

2. Setup Environment Variables
Create a .env file in the root directory and populate it with your credentials:
SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)
SUPABASE_KEY=your-supabase-anon-or-service-role-key
FONNTE_TOKEN=your-fonnte-api-token
TARGET_PHONE_NUMBER=0812XXXXXXXX

3. Install Dependencies & Run

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install required packages
pip install -r requirements.txt
# Run pipeline locally
python main.py

# 📈 Roadmap & Upcoming Enhancements
[x] Initial cloud pipeline setup with GitHub Actions & Supabase.
[x] Automated WhatsApp notification integration upon workflow completion.
[ ] Dynamic Data Generator Integration: Transition from static REST endpoints to a dynamic synthetic event streaming generator using Faker to simulate daily transactions.
[ ] Data Quality Framework: Implement schema validation prior to the database loading phase.
[ ] BI Dashboard Integration: Connect Supabase PostgreSQL instance to Metabase / Looker Studio for real-time sales reporting.

# 👤 Author
**Dika Hendrayana**
GitHub: @dikahendrayana
LinkedIn: **Dika Hendrayana**
Developed as part of a continuous learning path in Data Engineering & Cloud Data Architecture.
