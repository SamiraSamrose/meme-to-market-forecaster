import pandas as pd
import numpy as np
import re
from config.settings import SEMANTIC_THRESHOLDS

class SemanticScorer:
    def __init__(self):
        self.financial_keywords = ['buy', 'invest', 'hold', 'long', 'bullish', 'calls', 'puts', 'position', 'portfolio', 'stake']
        self.humor_keywords = ['lol', 'lmao', 'haha', 'joke', 'jk', 'kidding', 'ironic', 'sarcasm']
        
    def calculate_meme_seriousness_threshold(self, text):
        """Calculate ratio of financial vs humor keywords (0-1 scale)"""
        
        text_lower = text.lower()
        financial_count = sum(text_lower.count(kw) for kw in self.financial_keywords)
        humor_count = sum(text_lower.count(kw) for kw in self.humor_keywords)
        
        total_keywords = financial_count + humor_count
        if total_keywords == 0:
            return 0.5
        
        return financial_count / total_keywords
    
    def calculate_irony_collapse_index(self, text, financial_count=None, humor_count=None):
        """Measure shift from ironic sharing to sincere financial action (0-1 scale)"""
        
        if financial_count is None or humor_count is None:
            text_lower = text.lower()
            financial_count = sum(text_lower.count(kw) for kw in self.financial_keywords)
            humor_count = sum(text_lower.count(kw) for kw in self.humor_keywords)
        
        if humor_count == 0 and financial_count > 0:
            return 0.9
        elif humor_count > financial_count * 2:
            return 0.1
        elif financial_count > humor_count:
            return 0.7 + (financial_count / (financial_count + humor_count)) * 0.3
        else:
            return 0.3 + (financial_count / (financial_count + humor_count)) * 0.4
    
    def process_batch(self, texts):
        """Process batch of texts and return semantic scores"""
        
        results = []
        
        for text in texts:
            text_lower = text.lower()
            financial_count = sum(text_lower.count(kw) for kw in self.financial_keywords)
            humor_count = sum(text_lower.count(kw) for kw in self.humor_keywords)
            
            mst = self.calculate_meme_seriousness_threshold(text)
            ici = self.calculate_irony_collapse_index(text, financial_count, humor_count)
            
            results.append({
                'seriousness_threshold': min(1.0, max(0.0, mst)),
                'irony_collapse_index': min(1.0, max(0.0, ici)),
                'financial_keywords_count': financial_count,
                'humor_keywords_count': humor_count
            })
        
        return pd.DataFrame(results)

if __name__ == "__main__":
    scorer = SemanticScorer()
    test_texts = [
        "HODL diamond hands to the moon! Buy the dip!",
        "lol this is just a joke haha kidding",
        "Seriously considering buying and holding long term"
    ]
    results = scorer.process_batch(test_texts)
    print(results)
