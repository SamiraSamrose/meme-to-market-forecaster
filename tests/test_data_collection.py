import unittest
from src.data_collection.bigquery_reddit import RedditDataCollector
from src.data_collection.google_trends import GoogleTrendsCollector
from src.data_collection.tiktok_api import TikTokDataCollector

class TestDataCollection(unittest.TestCase):
    
    def test_reddit_collector_initialization(self):
        collector = RedditDataCollector()
        self.assertIsNotNone(collector.client)
        
    def test_trends_collector_initialization(self):
        collector = GoogleTrendsCollector()
        self.assertIsNotNone(collector.pytrends)
        
    def test_tiktok_collector_initialization(self):
        collector = TikTokDataCollector()
        self.assertIsNotNone(collector.api_base)

if __name__ == '__main__':
    unittest.main()
