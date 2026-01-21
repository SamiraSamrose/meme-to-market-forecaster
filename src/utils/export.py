import pandas as pd
from datetime import datetime
from config.settings import EXPORT_CONFIG

class ExportManager:
    def __init__(self):
        self.export_config = EXPORT_CONFIG
        
    def prepare_betting_odds_export(self, df):
        """Prepare betting odds vs real impact data for sheets export"""
        
        export_data = []
        
        for idx, row in df.iterrows():
            export_data.append({
                'Meme_ID': f"MEME_{idx}",
                'Text_Preview': str(row['body'])[:80],
                'ICI_Score': round(row['irony_collapse_index'], 3),
                'Seriousness_Threshold': round(row['seriousness_threshold'], 3),
                'Predicted_Impact_72h': round(row.get('impact_prob_72h', 0), 2),
                'Betting_Odds_Percentage': round(row.get('predicted_readiness', 0) * 100, 1),
                'Real_World_Impact_Score': round(row.get('estimated_market_impact', 0), 3),
                'Recommendation': 'MONITOR' if row['irony_collapse_index'] < 0.7 else 'ALERT'
            })
        
        sheets_df = pd.DataFrame(export_data)
        return sheets_df
    
    def export_to_csv(self, df, filename):
        """Export dataframe to CSV for sheets import"""
        
        filepath = f"{self.export_config['storage_path']}{filename}"
        df.to_csv(filepath, index=False)
        
        print(f"Export file created: {filepath}")
        print(f"Total rows exported: {len(df)}")
        
        return filepath
    
    def create_keyword_export(self, target_keywords, exclude_keywords):
        """Create keyword recommendations export"""
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'target_opportunities': target_keywords.to_dict('records'),
            'exclusion_recommendations': exclude_keywords.to_dict('records')
        }
        
        return export_data

if __name__ == "__main__":
    manager = ExportManager()
    print("Export Manager initialized")
