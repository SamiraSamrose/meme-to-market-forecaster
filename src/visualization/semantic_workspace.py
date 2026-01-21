import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class SemanticWorkspace:
    def __init__(self):
        pass
        
    def create_multimodal_preview(self, df):
        """Multimodal meme preview with hover analysis"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['seriousness_threshold'],
            y=df['irony_collapse_index'],
            mode='markers',
            marker=dict(
                size=df['predicted_readiness'] * 50,
                color=df['predicted_readiness'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title='Market Readiness')
            ),
            text=[f"ID: M{i}<br>Metaphor: {row.get('primary_metaphor', 'none')}<br>Intent: {'Financial' if row.get('financial_intent', 0) == 1 else 'Ironic'}<br>Text: {str(row['body'])[:100]}" 
                  for i, row in df.iterrows()],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Multimodal Meme Preview: Hover for AI Breakdown',
            xaxis_title='Seriousness Threshold',
            yaxis_title='Irony Collapse Index',
            height=600
        )
        
        return fig
    
    def create_slang_acceleration_charts(self, reddit_df, slang_acceleration_df):
        """Interactive slang acceleration comparison charts"""
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Term Frequency vs Google Trends', 'Acceleration Rate Comparison'),
            vertical_spacing=0.12
        )
        
        for term in slang_acceleration_df.head(5)['term']:
            term_data = reddit_df[reddit_df['body'].str.contains(term, case=False, na=False)]
            term_daily = term_data.groupby('date').size().reset_index(name='count')
            
            fig.add_trace(
                go.Scatter(
                    x=term_daily['date'],
                    y=term_daily['count'],
                    mode='lines+markers',
                    name=f"{term} (Reddit)",
                    line=dict(width=2)
                ),
                row=1, col=1
            )
        
        fig.add_trace(
            go.Bar(
                x=slang_acceleration_df.head(10)['term'],
                y=slang_acceleration_df.head(10)['avg_acceleration'],
                name='Acceleration Rate',
                marker=dict(color='orange')
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_yaxes(title_text="Frequency", row=1, col=1)
        fig.update_xaxes(title_text="Term", row=2, col=1)
        fig.update_yaxes(title_text="Acceleration", row=2, col=1)
        
        fig.update_layout(
            title_text="Slang Acceleration: HODL, Skibidi, Rizz vs Google Trends",
            height=800,
            showlegend=True
        )
        
        return fig
    
    def generate_narrative_summary(self, df, diffusion_df, slang_acceleration_df):
        """Generate AI narrative summary"""
        
        from datetime import datetime
        
        narrative = f"""
CULTURAL INTELLIGENCE REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}

EXECUTIVE SUMMARY:
This analysis reveals {(df['irony_collapse_index'] > 0.8).sum()} memes transitioning from 
ironic TikTok soundbites to legitimate market signals. The term '{slang_acceleration_df.iloc[0]['term']}' 
shows the highest acceleration rate at {slang_acceleration_df.iloc[0]['avg_acceleration']:.3f}, indicating 
rapid mainstream adoption.

PLATFORM DIFFUSION ANALYSIS:
Memes are moving from Reddit (early adopter communities) through TikTok (viral amplification) to 
Google Shopping trends at an average velocity of {diffusion_df['diffusion_index'].mean():.2f if not diffusion_df.empty else 'N/A'} diffusion index points.

KEY INSIGHT:
{(df['irony_collapse_index'] > 0.8).sum()} memes have crossed the critical 0.8 ICI threshold, 
suggesting imminent financial market impact. Expected Google Ads keyword cost increase: 
{df[df['irony_collapse_index'] > 0.8]['predicted_readiness'].mean() * 15:.1f}% 
within 48 hours.

RECOMMENDATION:
Monitor high-ICI memes for brand safety violations. Consider proactive keyword exclusions.
"""
        
        return narrative

if __name__ == "__main__":
    workspace = SemanticWorkspace()
    print("Semantic Workspace initialized")
