-- Semantic scores table
CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.semantic_scores` (
  meme_id STRING,
  text STRING,
  meme_seriousness_threshold FLOAT64,
  irony_collapse_index FLOAT64,
  processing_timestamp TIMESTAMP,
  financial_keywords_count INT64,
  humor_keywords_count INT64
);

-- Visual metadata table (external)
CREATE OR REPLACE EXTERNAL TABLE `{PROJECT_ID}.{DATASET_ID}.visual_metadata`
OPTIONS (
  format = 'JSON',
  uris = ['gs://{BUCKET_NAME}/visual_metadata/*.json']
);

-- TikTok trends table
CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.tiktok_trends` (
  hashtag STRING,
  view_count INT64,
  video_count INT64,
  growth_rate FLOAT64,
  velocity_score FLOAT64,
  viral_threshold BOOL,
  collection_timestamp TIMESTAMP
);

-- Google Trends Alpha table
CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.google_trends_alpha` (
  keyword STRING,
  date DATE,
  search_velocity FLOAT64,
  velocity_ma_3 FLOAT64,
  velocity_ma_7 FLOAT64,
  acceleration FLOAT64,
  jerk FLOAT64,
  momentum FLOAT64,
  top_region STRING,
  rising_queries_count INT64,
  ingestion_timestamp TIMESTAMP
);

-- Brand safety alerts table
CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.brand_safety_alerts` (
  alert_id STRING,
  meme_id STRING,
  alert_type STRING,
  ici_score FLOAT64,
  toxicity_score FLOAT64,
  recommended_action STRING,
  estimated_campaign_exposure STRING,
  alert_timestamp TIMESTAMP,
  associated_keywords ARRAY<STRING>
);
