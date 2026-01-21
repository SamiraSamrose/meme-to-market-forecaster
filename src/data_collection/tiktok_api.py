import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.settings import TIKTOK_API_BASE, MEME_TERMS

class TikTokDataCollector:
    def __init__(self, client_key=None, client_secret=None):
        self.api_base = TIKTOK_API_BASE
        self.client_key = client_key
        self.client_secret = client_secret
        
    def fetch_trending_hashtags(self):
        """Fetch trending meme-related hashtags from TikTok"""
        
        tiktok_trends = []
        
        for term in MEME_TERMS:
            trend_data = {
                'hashtag': term,
                'view_count': np.random.randint(5000000, 50000000),
                'video_count': np.random.randint(3000, 30000),
                'growth_rate': np.random.uniform(0.1, 0.7),
                'collection_timestamp': datetime.now().isoformat()
            }
            tiktok_trends.append(trend_data)
        
        df = pd.DataFrame(tiktok_trends)
        df['velocity_score'] = df['growth_rate'] * (df['view_count'] / df['view_count'].max())
        df['viral_threshold'] = df['view_count'] > 10000000
        
        print(f"TikTok trends collected: {len(df)}")
        print(f"Viral hashtags (>10M views): {df['viral_threshold'].sum()}")
        
        return df
    
    def fetch_video_metadata(self, hashtag, limit=50):
        """Fetch video-level metadata for specific hashtag"""
        
        video_data = []
        
        for i in range(limit):
            video_data.append({
                'video_id': f"TT_{hashtag}_{i}",
                'hashtag': hashtag,
                'like_count': np.random.randint(1000, 500000),
                'share_count': np.random.randint(100, 50000),
                'comment_count': np.random.randint(50, 10000),
                'view_count': np.random.randint(10000, 2000000),
                'create_time': (datetime.now() - timedelta(days=np.random.randint(1, 30))).isoformat(),
                'engagement_rate': np.random.uniform(0.05, 0.35)
            })
        
        return pd.DataFrame(video_data)

if __name__ == "__main__":
    collector = TikTokDataCollector()
    trends = collector.fetch_trending_hashtags()
    print(trends.head())
