import os

# Google Cloud Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
DATASET_ID = "meme_market_intelligence"
BUCKET_NAME = "meme-market-storage"

# BigQuery Configuration
BIGQUERY_CONFIG = {
    "dataset_id": DATASET_ID,
    "location": "US",
    "reddit_table": "fh-bigquery.reddit_comments",
    "batch_size": 50000
}

# Vertex AI Configuration
VERTEX_AI_CONFIG = {
    "model_name": "gemini-1.5-pro",
    "location": LOCATION,
    "batch_size": 100
}

# API Endpoints
TIKTOK_API_BASE = "https://open.tiktokapis.com/v2"
KNOWYOURMEME_URL = "https://knowyourmeme.com"

# Analysis Parameters
SEMANTIC_THRESHOLDS = {
    "high_ici": 0.8,
    "medium_ici": 0.5,
    "low_ici": 0.3,
    "toxicity_threshold": 2,
    "lookalike_threshold": 0.7
}

# Meme Terms to Track
MEME_TERMS = [
    "hodl", "diamond hands", "to the moon", "stonks", 
    "ape together strong", "buy the dip", "skibidi", 
    "rizz", "sigma", "based"
]

# Feature Configuration
FEATURE_COLUMNS = [
    "seriousness_threshold",
    "irony_collapse_index",
    "lookalike_score",
    "financial_intent",
    "ironic_marker",
    "financial_words",
    "urgency_words",
    "caps_ratio",
    "exclamation_count",
    "text_length"
]

# Export Configuration
EXPORT_CONFIG = {
    "sheets_format": "csv",
    "storage_path": "exports/",
    "max_rows": 10000
}
