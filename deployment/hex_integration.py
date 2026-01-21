from src.data_collection.bigquery_reddit import RedditDataCollector
from src.data_collection.google_trends import GoogleTrendsCollector
from src.data_collection.tiktok_api import TikTokDataCollector
from src.semantic_analysis.semantic_scoring import SemanticScorer
from src.semantic_analysis.vector_clustering import VectorClusterer
from src.modeling.market_impact_predictor import MarketImpactPredictor
from src.brand_safety.toxicity_analyzer import ToxicityAnalyzer
from src.utils.storage import StorageManager
from src.utils.export import ExportManager

class HexIntegration:
    def __init__(self):
        self.reddit_collector = RedditDataCollector()
        self.trends_collector = GoogleTrendsCollector()
        self.tiktok_collector = TikTokDataCollector()
        self.semantic_scorer = SemanticScorer()
        self.clusterer = VectorClusterer()
        self.predictor = MarketImpactPredictor()
        self.toxicity_analyzer = ToxicityAnalyzer()
        self.storage_manager = StorageManager()
        self.export_manager = ExportManager()
        
    def run_full_pipeline(self):
        """Execute complete meme-to-market analysis pipeline"""
        
        print("Starting Meme-to-Market Impact Forecaster Pipeline...")
        
        # Step 1: Data Collection
        print("\n[1/6] Collecting data from all sources...")
        reddit_df = self.reddit_collector.extract_reddit_comments()
        trends_df = self.trends_collector.collect_trends_data()
        tiktok_df = self.tiktok_collector.fetch_trending_hashtags()
        
        # Step 2: Semantic Analysis
        print("\n[2/6] Running semantic analysis...")
        semantic_results = self.semantic_scorer.process_batch(reddit_df['body'].tolist()[:1000])
        reddit_df = reddit_df.head(len(semantic_results))
        reddit_df = reddit_df.join(semantic_results)
        
        # Step 3: Vector Clustering
        print("\n[3/6] Performing vector clustering...")
        reddit_df = self.clusterer.find_lookalikes(reddit_df)
        
        # Step 4: Market Impact Prediction
        print("\n[4/6] Training market impact predictor...")
        metrics = self.predictor.train(reddit_df)
        reddit_df = self.predictor.predict(reddit_df)
        reddit_df = self.predictor.calculate_impact_probability(reddit_df)
        
        # Step 5: Brand Safety Analysis
        print("\n[5/6] Analyzing brand safety...")
        reddit_df = self.toxicity_analyzer.process_dataframe(reddit_df)
        alerts = self.toxicity_analyzer.generate_alerts(reddit_df)
        
        # Step 6: Export Results
        print("\n[6/6] Exporting results...")
        self.storage_manager.export_to_gcs(reddit_df, 'final_predictions.json')
        export_df = self.export_manager.prepare_betting_odds_export(reddit_df)
        self.export_manager.export_to_csv(export_df, 'betting_odds_export.csv')
        
        print("\nPipeline Complete!")
        
        return reddit_df, trends_df, tiktok_df, alerts, metrics

if __name__ == "__main__":
    integration = HexIntegration()
    results = integration.run_full_pipeline()
