import pandas as pd
import re
from config.settings import SEMANTIC_THRESHOLDS

class ToxicityAnalyzer:
    def __init__(self):
        self.toxic_patterns = {
            'misinformation': r'\b(fake|scam|ponzi|rug pull|fraud)\b',
            'harassment': r'\b(attack|target|brigade|raid)\b',
            'extremism': r'\b(war|fight|destroy|kill)\b',
            'manipulation': r'\b(pump|dump|coordinate|manipulate)\b'
        }
        self.weaponized_threshold = SEMANTIC_THRESHOLDS['toxicity_threshold']
        
    def analyze_toxicity(self, text):
        """Analyze text for toxic content markers"""
        
        toxicity_scores = {}
        for category, pattern in self.toxic_patterns.items():
            matches = len(re.findall(pattern, text.lower()))
            toxicity_scores[category] = matches
        
        total_toxicity = sum(toxicity_scores.values())
        
        return total_toxicity, toxicity_scores
    
    def process_dataframe(self, df):
        """Process entire dataframe for toxicity"""
        
        toxicity_results = df['body'].apply(self.analyze_toxicity)
        df['toxicity_score'] = [r[0] for r in toxicity_results]
        df['toxicity_breakdown'] = [r[1] for r in toxicity_results]
        
        df['is_weaponized'] = df['toxicity_score'] >= self.weaponized_threshold
        
        return df
    
    def generate_alerts(self, df):
        """Generate brand safety alerts for weaponized memes"""
        
        alerts = df[
            (df['is_weaponized']) & 
            (df.get('predicted_readiness', 0) > 0.5)
        ].copy()
        
        if len(alerts) > 0:
            alerts['alert_severity'] = pd.cut(
                alerts['toxicity_score'],
                bins=[0, 2, 4, 100],
                labels=['Medium', 'High', 'Critical']
            )
        
        print(f"Brand safety alerts generated: {len(alerts)}")
        
        return alerts
    
    def subreddit_safety_analysis(self, df):
        """Analyze safety metrics by subreddit"""
        
        subreddit_safety = df.groupby('subreddit').agg({
            'toxicity_score': 'mean',
            'is_weaponized': 'sum',
            'body': 'count'
        }).reset_index()
        
        subreddit_safety.columns = ['subreddit', 'avg_toxicity', 'weaponized_count', 'total_posts']
        subreddit_safety['weaponized_rate'] = subreddit_safety['weaponized_count'] / subreddit_safety['total_posts']
        subreddit_safety = subreddit_safety.sort_values('weaponized_rate', ascending=False)
        
        return subreddit_safety

if __name__ == "__main__":
    analyzer = ToxicityAnalyzer()
    test_df = pd.DataFrame({
        'body': ['pump and dump scam', 'normal discussion', 'coordinated manipulation raid'],
        'predicted_readiness': [0.8, 0.3, 0.9],
        'subreddit': ['test1', 'test2', 'test1']
    })
    result = analyzer.process_dataframe(test_df)
    print(result[['body', 'toxicity_score', 'is_weaponized']])
