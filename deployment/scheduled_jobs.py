from src.brand_safety.monitoring import BrandSafetyMonitor
from src.data_collection.knowyourmeme_scraper import KnowYourMemeCollector
from datetime import datetime

class ScheduledJobs:
    def __init__(self):
        self.monitor = BrandSafetyMonitor()
        self.kym_collector = KnowYourMemeCollector()
        
    def hourly_weaponized_meme_check(self):
        """Run hourly check for weaponized memes"""
        
        print(f"\n[{datetime.now()}] Running hourly weaponized meme check...")
        
        patterns = self.kym_collector.fetch_weaponized_patterns()
        
        print(f"Weaponized patterns identified: {len(patterns)}")
        
        return patterns
    
    def daily_brand_safety_report(self, df):
        """Generate daily brand safety report"""
        
        print(f"\n[{datetime.now()}] Generating daily brand safety report...")
        
        alerts = self.monitor.setup_monitoring(df)
        
        print(f"Critical alerts generated: {len(alerts)}")
        
        return alerts

if __name__ == "__main__":
    jobs = ScheduledJobs()
    patterns = jobs.hourly_weaponized_meme_check()
    print(patterns)
