from google.cloud import bigquery
import pandas as pd
from datetime import datetime
from config.settings import PROJECT_ID, DATASET_ID, BIGQUERY_CONFIG, MEME_TERMS

class RedditDataCollector:
    def __init__(self):
        self.client = bigquery.Client(project=PROJECT_ID)
        self.dataset_id = DATASET_ID
        
    def extract_reddit_comments(self, limit=50000):
        """Extract meme-related Reddit comments with temporal patterns"""
        
        meme_pattern = "|".join([f"'{term}'" for term in MEME_TERMS])
        
        query = f"""
        WITH meme_keywords AS (
          SELECT 
            created_utc,
            body,
            score,
            subreddit,
            author,
            EXTRACT(DATE FROM TIMESTAMP_SECONDS(created_utc)) as date,
            EXTRACT(HOUR FROM TIMESTAMP_SECONDS(created_utc)) as hour
          FROM `fh-bigquery.reddit_comments.2024_*`
          WHERE 
            (LOWER(body) LIKE '%hodl%' 
            OR LOWER(body) LIKE '%diamond hands%'
            OR LOWER(body) LIKE '%to the moon%'
            OR LOWER(body) LIKE '%buy the dip%'
            OR LOWER(body) LIKE '%ape%'
            OR LOWER(body) LIKE '%stonk%'
            OR LOWER(body) LIKE '%skibidi%'
            OR LOWER(body) LIKE '%rizz%'
            OR LOWER(body) LIKE '%sigma%'
            OR LOWER(body) LIKE '%based%')
            AND LENGTH(body) > 20
            AND LENGTH(body) < 500
          LIMIT {limit}
        )
        SELECT 
          date,
          hour,
          subreddit,
          body,
          score,
          CASE 
            WHEN REGEXP_CONTAINS(LOWER(body), r'(buy|invest|hold|long|bullish|calls)') THEN 1
            ELSE 0
          END as financial_intent,
          CASE 
            WHEN REGEXP_CONTAINS(LOWER(body), r'(lol|lmao|haha|jk|joking|ironic)') THEN 1
            ELSE 0
          END as ironic_marker,
          LENGTH(body) as text_length
        FROM meme_keywords
        ORDER BY created_utc DESC
        """
        
        print(f"Executing BigQuery extraction for Reddit meme data...")
        df = self.client.query(query).to_dataframe()
        print(f"Extracted {len(df)} Reddit comments")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"Unique subreddits: {df['subreddit'].nunique()}")
        
        return df
    
    def save_to_bigquery(self, df, table_name):
        """Save processed data to BigQuery"""
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
        )
        
        job = self.client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        job.result()
        
        print(f"Data saved to {table_id}")
        return table_id

if __name__ == "__main__":
    collector = RedditDataCollector()
    reddit_df = collector.extract_reddit_comments()
    collector.save_to_bigquery(reddit_df, "reddit_meme_raw")
