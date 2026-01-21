import vertexai
from vertexai.generative_models import GenerativeModel
import json
import re
from config.settings import PROJECT_ID, LOCATION, VERTEX_AI_CONFIG

class GeminiAnalyzer:
    def __init__(self):
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        self.model = GenerativeModel(VERTEX_AI_CONFIG['model_name'])
        
    def analyze_semantic_scores(self, text):
        """Use Gemini to calculate semantic scores"""
        
        prompt = f"""Analyze this meme-related text and provide ONLY a JSON response with two numerical scores:

Text: "{text}"

Return JSON format:
{{
  "seriousness_threshold": <float 0-1>,
  "irony_collapse_index": <float 0-1>
}}

Scoring criteria:
- seriousness_threshold: Ratio of financial action words (buy, invest, hold) vs humor words (lol, lmao). Higher = more serious financial intent.
- irony_collapse_index: Degree to which ironic language has shifted to sincere belief. 0 = pure irony, 1 = sincere action.

Provide ONLY the JSON, no other text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            json_match = re.search(r'\{[^}]+\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    'seriousness_threshold': float(result.get('seriousness_threshold', 0.5)),
                    'irony_collapse_index': float(result.get('irony_collapse_index', 0.5))
                }
        except Exception as e:
            print(f"Gemini analysis error: {e}")
        
        return {'seriousness_threshold': 0.5, 'irony_collapse_index': 0.5}
    
    def analyze_visual_metaphor(self, text_description):
        """Identify visual metaphors and Google Shopping correlation"""
        
        visual_metaphors = {
            'rocket': {'trend_category': 'price_surge', 'google_shopping_relevance': 0.6},
            'moon': {'trend_category': 'extreme_growth', 'google_shopping_relevance': 0.4},
            'diamond': {'trend_category': 'holding_strength', 'google_shopping_relevance': 0.7},
            'ape': {'trend_category': 'community_action', 'google_shopping_relevance': 0.3},
            'hands': {'trend_category': 'holding_commitment', 'google_shopping_relevance': 0.5},
            'brain': {'trend_category': 'intelligence_signal', 'google_shopping_relevance': 0.4},
            'stonk': {'trend_category': 'stock_reference', 'google_shopping_relevance': 0.8},
            'chart': {'trend_category': 'technical_analysis', 'google_shopping_relevance': 0.9}
        }
        
        text_lower = text_description.lower()
        detected_metaphors = []
        
        for metaphor, properties in visual_metaphors.items():
            if metaphor in text_lower:
                detected_metaphors.append({
                    'metaphor': metaphor,
                    'trend_category': properties['trend_category'],
                    'shopping_relevance': properties['google_shopping_relevance']
                })
        
        if detected_metaphors:
            avg_shopping_relevance = np.mean([m['shopping_relevance'] for m in detected_metaphors])
            primary_metaphor = max(detected_metaphors, key=lambda x: x['shopping_relevance'])
        else:
            avg_shopping_relevance = 0.0
            primary_metaphor = None
        
        return {
            'detected_metaphors': detected_metaphors,
            'primary_visual_metaphor': primary_metaphor['metaphor'] if primary_metaphor else 'none',
            'google_shopping_correlation': avg_shopping_relevance,
            'metaphor_count': len(detected_metaphors)
        }

if __name__ == "__main__":
    import numpy as np
    analyzer = GeminiAnalyzer()
    test_text = "Buy HODL diamond hands to the moon with rockets!"
    scores = analyzer.analyze_semantic_scores(test_text)
    visual = analyzer.analyze_visual_metaphor(test_text)
    print("Semantic Scores:", scores)
    print("Visual Analysis:", visual)
