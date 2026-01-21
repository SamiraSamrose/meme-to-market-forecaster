import pandas as pd
from datetime import datetime
from config.settings import SEMANTIC_THRESHOLDS

class BrandSafetyMonitor:
    def __init__(self):
        self.monitoring_config = {
            'ici_threshold': SEMANTIC_THRESHOLDS['high_ici'],
            'toxicity_threshold': SEMANTIC_THRESHOLDS['toxicity_threshold'],
            'lookalike_threshold': SEMANTIC_THRESHOLDS['lookalike_threshold'],
            'alert_window_hours': 24
        }
        
    def setup_monitoring(self, df):
        """Configure monitoring alerts for Google Ads managers"""
        
        alert_candidates = df[
            (df['irony_collapse_index'] > self.monitoring_config['ici_threshold']) &
            (df['toxicity_score'] >= self.monitoring_config['toxicity_threshold'])
        ]
        
        alerts = []
        
        for idx, row in alert_candidates.iterrows():
            alert = {
                'alert_id': f"ALERT_{idx}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'meme_id': f"MEME_{idx}",
                'alert_type': 'BRAND_SAFETY_CRITICAL',
                'ici_score': row['irony_collapse_index'],
                'toxicity_score': row['toxicity_score'],
                'recommended_action': 'IMMEDIATE_KEYWORD_EXCLUSION',
                'estimated_campaign_exposure': 'HIGH',
                'alert_timestamp': datetime.now().isoformat()
            }
            
            text_words = str(row['body']).lower().split()
            risky_keywords = [w for w in text_words if len(w) > 3][:5]
            alert['associated_keywords'] = risky_keywords
            
            alerts.append(alert)
        
        return pd.DataFrame(alerts)
    
    def monitor_weaponized_memes(self, recent_df):
        """Monitor for new weaponized meme patterns"""
        
        high_risk = recent_df[recent_df['toxicity_score'] >= 3]
        
        if len(high_risk) > 0:
            alert_message = {
                'timestamp': datetime.now().isoformat(),
                'high_risk_count': len(high_risk),
                'top_subreddits': high_risk['subreddit'].value_counts().head(3).to_dict(),
                'average_toxicity': high_risk['toxicity_score'].mean()
            }
            
            print(f"High-risk memes detected: {len(high_risk)}")
            return high_risk, alert_message
        
        return None, None

if __name__ == "__main__":
    monitor = BrandSafetyMonitor()
    print("Brand Safety Monitor initialized")
