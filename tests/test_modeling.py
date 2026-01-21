import unittest
from src.modeling.market_impact_predictor import MarketImpactPredictor
from src.brand_safety.toxicity_analyzer import ToxicityAnalyzer
import pandas as pd

class TestModeling(unittest.TestCase):
    
    def setUp(self):
        self.predictor = MarketImpactPredictor()
        self.toxicity = ToxicityAnalyzer()
        
    def test_predictor_initialization(self):
        self.assertIsNotNone(self.predictor.model)
        self.assertIsNotNone(self.predictor.scaler)
        
    def test_toxicity_analysis(self):
        text = "pump and dump scam fraud"
        score, breakdown = self.toxicity.analyze_toxicity(text)
        
        self.assertGreater(score, 0)
        self.assertIn('misinformation', breakdown)

if __name__ == '__main__':
    unittest.main()
