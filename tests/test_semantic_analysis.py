import unittest
from src.semantic_analysis.semantic_scoring import SemanticScorer
from src.semantic_analysis.vector_clustering import VectorClusterer
import pandas as pd

class TestSemanticAnalysis(unittest.TestCase):
    
    def setUp(self):
        self.scorer = SemanticScorer()
        self.clusterer = VectorClusterer()
        
    def test_semantic_scorer(self):
        text = "Buy HODL diamond hands to the moon!"
        mst = self.scorer.calculate_meme_seriousness_threshold(text)
        ici = self.scorer.calculate_irony_collapse_index(text)
        
        self.assertGreaterEqual(mst, 0)
        self.assertLessEqual(mst, 1)
        self.assertGreaterEqual(ici, 0)
        self.assertLessEqual(ici, 1)
        
    def test_vector_clustering(self):
        df = pd.DataFrame({
            'body': ['HODL moon', 'stonks'],
            'seriousness_threshold': [0.8, 0.7],
            'irony_collapse_index': [0.9, 0.6]
        })
        result = self.clusterer.find_lookalikes(df)
        
        self.assertIn('best_lookalike', result.columns)
        self.assertIn('lookalike_similarity', result.columns)

if __name__ == '__main__':
    unittest.main()
