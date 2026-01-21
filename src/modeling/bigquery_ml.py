from google.cloud import bigquery
from config.settings import PROJECT_ID, DATASET_ID

class BigQueryMLModel:
    def __init__(self):
        self.client = bigquery.Client(project=PROJECT_ID)
        self.dataset_id = DATASET_ID
        
    def create_slang_acceleration_model(self):
        """Create BigQuery ML linear regression model"""
        
        model_query = f"""
        CREATE OR REPLACE MODEL `{PROJECT_ID}.{DATASET_ID}.slang_acceleration_predictor`
        OPTIONS(
          model_type='LINEAR_REG',
          input_label_cols=['market_impact_score'],
          data_split_method='AUTO_SPLIT',
          data_split_eval_fraction=0.2,
          enable_global_explain=TRUE
        ) AS
        SELECT
          meme_seriousness_threshold,
          irony_collapse_index,
          financial_keywords_count,
          humor_keywords_count,
          CAST(financial_keywords_count AS FLOAT64) / NULLIF(CAST(humor_keywords_count AS FLOAT64), 0) as slang_acceleration_rate,
          irony_collapse_index * meme_seriousness_threshold as combined_readiness,
          meme_seriousness_threshold * 0.4 + irony_collapse_index * 0.6 as market_impact_score
        FROM `{PROJECT_ID}.{DATASET_ID}.semantic_scores`
        WHERE meme_seriousness_threshold IS NOT NULL
          AND irony_collapse_index IS NOT NULL
        """
        
        print("Creating BigQuery ML model...")
        job = self.client.query(model_query)
        job.result()
        print("BigQuery ML model created successfully")
        
    def evaluate_model(self):
        """Evaluate the BigQuery ML model"""
        
        eval_query = f"""
        SELECT
          mean_squared_error,
          mean_absolute_error,
          r2_score,
          explained_variance
        FROM
          ML.EVALUATE(MODEL `{PROJECT_ID}.{DATASET_ID}.slang_acceleration_predictor`)
        """
        
        results = self.client.query(eval_query).to_dataframe()
        print("\nBigQuery ML Model Evaluation:")
        print(results)
        
        return results
    
    def make_predictions(self, limit=100):
        """Make predictions using the BigQuery ML model"""
        
        predict_query = f"""
        SELECT
          meme_id,
          predicted_market_impact_score,
          meme_seriousness_threshold,
          irony_collapse_index
        FROM
          ML.PREDICT(MODEL `{PROJECT_ID}.{DATASET_ID}.slang_acceleration_predictor`,
            (SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.semantic_scores` LIMIT {limit}))
        ORDER BY predicted_market_impact_score DESC
        """
        
        predictions = self.client.query(predict_query).to_dataframe()
        print(f"\nTop predictions generated: {len(predictions)}")
        
        return predictions

if __name__ == "__main__":
    bqml = BigQueryMLModel()
    bqml.create_slang_acceleration_model()
    bqml.evaluate_model()
