import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class PulseDashboard:
    def __init__(self):
        pass
        
    def create_diffusion_heatmap(self, platform_df):
        """Cross-platform diffusion heatmap visualization"""
        
        fig = go.Figure()
        
        for platform in ['Reddit', 'TikTok', 'Google_Search']:
            platform_data = platform_df[platform_df['platform'] == platform]
            pivot = platform_data.pivot_table(
                values='reddit_volume', 
                index='term', 
                columns='date', 
                aggfunc='sum'
            ).fillna(0)
            
            fig.add_trace(go.Heatmap(
                z=pivot.values,
                x=[str(d)[:10] for d in pivot.columns],
                y=pivot.index,
                colorscale='Viridis',
                name=platform,
                visible=(platform == 'Reddit')
            ))
        
        fig.update_layout(
            updatemenus=[{
                'buttons': [
                    {'label': 'Reddit (Niche)', 'method': 'update', 'args': [{'visible': [True, False, False]}]},
                    {'label': 'TikTok (Viral)', 'method': 'update', 'args': [{'visible': [False, True, False]}]},
                    {'label': 'Google Search (Mainstream)', 'method': 'update', 'args': [{'visible': [False, False, True]}]}
                ],
                'direction': 'down',
                'showactive': True,
                'x': 0.17,
                'y': 1.15
            }],
            title='Cross-Platform Diffusion Heatmap: Niche to Viral to Mainstream',
            xaxis_title='Date',
            yaxis_title='Meme Term',
            height=600
        )
        
        return fig
    
    def create_ici_meter(self, top_memes_df):
        """Irony Collapse Index gauge visualization"""
        
        fig = make_subplots(
            rows=2, cols=3,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
            subplot_titles=[f"Meme {i+1}" for i in range(6)]
        )
        
        for i, (idx, row) in enumerate(top_memes_df.head(6).iterrows()):
            ici_val = row['irony_collapse_index']
            
            gauge_color = "green" if ici_val < 0.5 else ("yellow" if ici_val < 0.8 else "red")
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=ici_val,
                    delta={'reference': 0.5},
                    gauge={
                        'axis': {'range': [0, 1]},
                        'bar': {'color': gauge_color},
                        'steps': [
                            {'range': [0, 0.5], 'color': 'lightgreen'},
                            {'range': [0.5, 0.8], 'color': 'lightyellow'},
                            {'range': [0.8, 1], 'color': 'lightcoral'}
                        ],
                        'threshold': {
                            'line': {'color': 'red', 'width': 4},
                            'thickness': 0.75,
                            'value': 0.8
                        }
                    },
                    title={'text': f"ICI: {ici_val:.2f}"}
                ),
                row=(i // 3) + 1,
                col=(i % 3) + 1
            )
        
        fig.update_layout(
            title_text="Irony Collapse Meter: Pure Joke (Green) to Market-Moving Belief (Red)",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_predictive_odds_ticker(self, ticker_df):
        """Predictive odds ticker showing impact probabilities"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(len(ticker_df))),
            y=ticker_df['impact_prob_24h'],
            mode='lines+markers',
            name='24h Impact',
            line=dict(color='lightblue', width=2),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=list(range(len(ticker_df))),
            y=ticker_df['impact_prob_48h'],
            mode='lines+markers',
            name='48h Impact',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=list(range(len(ticker_df))),
            y=ticker_df['impact_prob_72h'],
            mode='lines+markers',
            name='72h Impact',
            line=dict(color='darkblue', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title='Predictive Odds Ticker: Live Feed of Market Impact Probability',
            xaxis_title='Meme Index',
            yaxis_title='Impact Probability (%)',
            height=500,
            hovermode='x unified'
        )
        
        return fig

if __name__ == "__main__":
    dashboard = PulseDashboard()
    print("Pulse Dashboard initialized")
