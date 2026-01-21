import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import re
from config.settings import FEATURE_COLUMNS

class MarketImpactPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.feature_columns = FEATURE_COLUMNS
        
    def engineer_features(self, df):
        """Create prediction features"""
        
        df['financial_words'] = df['body'].apply(
            lambda x: len(re.findall(r'\b(buy|invest|hold|long|bullish|calls|puts|strike)\b', str(x).lower()))
        )
        df['urgency_words'] = df['body'].apply(
            lambda x: len(re.findall(r'\b(now|today|asap|urgent|quick|fast)\b', str(x).lower()))
        )
        df['caps_ratio'] = df['body'].apply(
            lambda x: sum(1 for c in str(x) if c.isupper()) / (len(str(x)) + 1)
        )
        df['exclamation_count'] = df['body'].apply(lambda x: str(x).count('!'))
        
        df['market_readiness'] = (
            df['seriousness_threshold'] * 0.3 +
            df['irony_collapse_index'] * 0.3 +
            df.get('lookalike_similarity', 0) * 0.2 +
            (df['score'] / df['score'].max()) * 0.2
        )
        
        return df
    
    def train(self, df):
        """Train market impact prediction model"""
        
        df = self.engineer_features(df)
        
        X = df[self.feature_columns].fillna(0)
        y = df['market_readiness']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model.fit(X_train_scaled, y_train)
        
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        
        metrics = {
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'train_mse': mean_squared_error(y_train, y_pred_train),
            'test_mse': mean_squared_error(y_test, y_pred_test),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test)
        }
        
        print("Model Training Complete")
        print(f"Training R²: {metrics['train_r2']:.4f}")
        print(f"Testing R²: {metrics['test_r2']:.4f}")
        print(f"Testing MAE: {metrics['test_mae']:.4f}")
        
        return metrics
    
    def predict(self, df):
        """Make predictions on new data"""
        
        df = self.engineer_features(df)
        X = df[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        df['predicted_readiness'] = self.model.predict(X_scaled)
        
        return df
    
    def calculate_impact_probability(self, df):
        """Calculate 24/48/72 hour impact probabilities"""
        
        df['impact_prob_24h'] = df.apply(
            lambda row: min(100, max(0, row['predicted_readiness'] * 100 * 
                (0.6 + 0.4 * row['irony_collapse_index']) * 
                (0.7 + 0.3 * row.get('lookalike_similarity', 0)))),
            axis=1
        )
        
        df['impact_prob_48h'] = df.apply(
            lambda row: min(100, max(0, row['predicted_readiness'] * 100 * 
                (0.7 + 0.3 * row['irony_collapse_index']) * 
                (0.8 + 0.2 * row.get('lookalike_similarity', 0)))),
            axis=1
        )
        
        df['impact_prob_72h'] = df.apply(
            lambda row: min(100, max(0, row['predicted_readiness'] * 100 * 
                (0.8 + 0.2 * row['irony_collapse_index']) * 
                (0.9 + 0.1 * row.get('lookalike_similarity', 0)))),
            axis=1
        )
        
        return df

if __name__ == "__main__":
    predictor = MarketImpactPredictor()
    print("Market Impact Predictor initialized")
