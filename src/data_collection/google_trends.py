from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
from config.settings import MEME_TERMS

class GoogleTrendsCollector:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        
    def collect_trends_data(self, terms=None, timeframe='today 3-m'):
        """Pull real-time search velocity for meme terms"""
        
        if terms is None:
            terms = MEME_TERMS
        
        trends_data = []
        
        for term in terms:
            try:
                self.pytrends.build_payload([term], timeframe=timeframe, geo='US')
                interest_over_time = self.pytrends.interest_over_time()
                
                if not interest_over_time.empty:
                    interest_over_time = interest_over_time.reset_index()
                    interest_over_time['term'] = term
                    interest_over_time['search_velocity'] = interest_over_time[term]
                    
                    interest_over_time['velocity_7d_avg'] = interest_over_time['search_velocity'].rolling(7).mean()
                    interest_over_time['velocity_change'] = interest_over_time['search_velocity'].pct_change()
                    interest_over_time['acceleration'] = interest_over_time['velocity_change'].diff()
                    interest_over_time['momentum'] = interest_over_time['search_velocity'] * interest_over_time['acceleration']
                    
                    trends_data.append(interest_over_time[['date', 'term', 'search_velocity', 
                                                             'velocity_7d_avg', 'velocity_change', 
                                                             'acceleration', 'momentum']])
            except Exception as e:
                print(f"Error fetching trends for {term}: {e}")
                continue
        
        trends_df = pd.concat(trends_data, ignore_index=True)
        print(f"Collected trends data for {len(terms)} terms")
        print(f"Total data points: {len(trends_df)}")
        
        return trends_df
    
    def calculate_search_delta(self, trends_df):
        """Calculate search delta metrics"""
        
        summary = trends_df.groupby('term').agg({
            'search_velocity': 'mean',
            'acceleration': 'mean',
            'momentum': 'mean'
        }).reset_index()
        
        summary['search_delta'] = summary['acceleration'] / (summary['search_velocity'] + 1)
        summary = summary.sort_values('momentum', ascending=False)
        
        return summary

if __name__ == "__main__":
    collector = GoogleTrendsCollector()
    trends_df = collector.collect_trends_data()
    delta_summary = collector.calculate_search_delta(trends_df)
    print(delta_summary)
