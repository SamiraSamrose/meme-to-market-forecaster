import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import re

class VectorClusterer:
    def __init__(self):
        self.historical_benchmarks = {
            'DOGE_2021': {
                'text': 'DOGE to the moon diamond hands hold the line crypto investment',
                'market_impact': 0.95,
                'category': 'cryptocurrency'
            },
            'GME_2021': {
                'text': 'GME stonks ape together strong buy hold wallstreetbets',
                'market_impact': 0.98,
                'category': 'stocks'
            },
            'NFT_2021': {
                'text': 'NFT investment mint drop blockchain digital art',
                'market_impact': 0.85,
                'category': 'crypto_art'
            },
            'SHIB_2021': {
                'text': 'SHIB shiba inu meme coin hold investment community',
                'market_impact': 0.82,
                'category': 'cryptocurrency'
            }
        }
        
    def create_feature_vector(self, text, seriousness=0.5, ici=0.5):
        """Create 20-dimensional feature vector"""
        
        text_lower = text.lower()
        features = [
            seriousness,
            ici,
            text_lower.count('buy') / (len(text) + 1),
            text_lower.count('invest') / (len(text) + 1),
            text_lower.count('hold') / (len(text) + 1),
            text_lower.count('moon') / (len(text) + 1),
            text_lower.count('diamond') / (len(text) + 1),
            text_lower.count('hands') / (len(text) + 1),
            text_lower.count('ape') / (len(text) + 1),
            text_lower.count('stonk') / (len(text) + 1),
            len(text.split()) / 100,
            len(re.findall(r'[A-Z]{2,}', text)) / (len(text) + 1),
            text.count('!') / (len(text) + 1),
            text.count('$') / (len(text) + 1),
            1 if 'crypto' in text_lower else 0,
            1 if 'stock' in text_lower else 0,
            1 if 'nft' in text_lower else 0,
            text_lower.count('rocket') / (len(text) + 1),
            text_lower.count('gain') / (len(text) + 1),
            text_lower.count('loss') / (len(text) + 1)
        ]
        
        return np.array(features, dtype=np.float32)
    
    def find_lookalikes(self, df):
        """Find historical lookalikes for current memes"""
        
        benchmark_embeddings = []
        benchmark_labels = []
        
        for name, data in self.historical_benchmarks.items():
            vector = self.create_feature_vector(data['text'], 0.9, 0.85)
            benchmark_embeddings.append(vector)
            benchmark_labels.append(name)
        
        benchmark_embeddings = np.array(benchmark_embeddings)
        
        current_embeddings = []
        for _, row in df.iterrows():
            vector = self.create_feature_vector(
                row['body'],
                row.get('seriousness_threshold', 0.5),
                row.get('irony_collapse_index', 0.5)
            )
            current_embeddings.append(vector)
        
        current_embeddings = np.array(current_embeddings)
        
        similarity_matrix = cosine_similarity(current_embeddings, benchmark_embeddings)
        
        df['best_lookalike'] = ''
        df['lookalike_similarity'] = 0.0
        df['estimated_market_impact'] = 0.0
        
        for i in range(len(similarity_matrix)):
            best_match_idx = np.argmax(similarity_matrix[i])
            similarity_score = similarity_matrix[i][best_match_idx]
            
            matched_benchmark = benchmark_labels[best_match_idx]
            impact = self.historical_benchmarks[matched_benchmark]['market_impact']
            
            df.loc[df.index[i], 'best_lookalike'] = matched_benchmark
            df.loc[df.index[i], 'lookalike_similarity'] = similarity_score
            df.loc[df.index[i], 'estimated_market_impact'] = similarity_score * impact
        
        return df
    
    def perform_clustering(self, df, n_clusters=6):
        """Perform K-means clustering"""
        
        vectors = []
        for _, row in df.iterrows():
            vector = self.create_feature_vector(
                row['body'],
                row.get('seriousness_threshold', 0.5),
                row.get('irony_collapse_index', 0.5)
            )
            vectors.append(vector)
        
        vectors = np.array(vectors)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(vectors)
        
        return df

if __name__ == "__main__":
    clusterer = VectorClusterer()
    test_df = pd.DataFrame({
        'body': ['HODL to the moon!', 'Buy the dip stonks'],
        'seriousness_threshold': [0.8, 0.7],
        'irony_collapse_index': [0.9, 0.6]
    })
    result = clusterer.find_lookalikes(test_df)
    print(result[['body', 'best_lookalike', 'lookalike_similarity']])
