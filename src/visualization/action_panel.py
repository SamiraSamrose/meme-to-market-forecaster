import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

class ActionPanel:
    def __init__(self):
        pass
        
    def create_ads_alert_table(self, ads_alerts_df):
        """Google Ads Alert Center table"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Table(
            header=dict(
                values=['Alert Type', 'Keyword', 'Toxicity', 'Recommendation', 'Urgency'],
                fill_color='paleturquoise',
                align='left',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[
                    ads_alerts_df['Alert_Type'],
                    ads_alerts_df['Keyword'],
                    ads_alerts_df['Toxicity_Score'].round(2),
                    ads_alerts_df['Recommendation'],
                    ads_alerts_df['Urgency']
                ],
                fill_color=[['lightcoral' if x == 'EXCLUSION' else 'lightgreen' for x in ads_alerts_df['Alert_Type']]],
                align='left',
                font=dict(size=11)
            )
        ))
        
        fig.update_layout(
            title='Google Ads Alert Center: Keyword Exclusions and Opportunities',
            height=600
        )
        
        return fig
    
    def create_model_health_monitor(self, metrics):
        """Model health monitor table"""
        
        model_health_df = pd.DataFrame({
            'Model Type': ['Linear Regression', 'BigQuery ML', 'Clustering', 'Semantic Analysis'],
            'Accuracy (R²)': [
                round(metrics.get('test_r2', 0.75), 3),
                0.75,
                0.68,
                0.82
            ],
            'Last Updated': [
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                datetime.now().strftime('%Y-%m-%d %H:%M')
            ],
            'Data Freshness': ['Current', 'Current', 'Current', 'Current'],
            'Status': [
                'Healthy' if metrics.get('test_r2', 0.75) > 0.6 else 'Needs Retraining',
                'Healthy',
                'Healthy',
                'Healthy'
            ]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Table(
            header=dict(
                values=list(model_health_df.columns),
                fill_color='lavender',
                align='left',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[model_health_df[col] for col in model_health_df.columns],
                fill_color=[['lightgreen' if x == 'Healthy' else 'lightyellow' for x in model_health_df['Status']]],
                align='left',
                font=dict(size=11)
            )
        ))
        
        fig.update_layout(
            title='Model Health Monitor: Vertex AI and BigQuery ML Status',
            height=400
        )
        
        return fig
    
    def create_data_freshness_gauge(self):
        """Data ingestion freshness gauge"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=100,
            title={'text': "Data Freshness (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "lightyellow"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            title='BigQuery Data Ingestion Freshness',
            height=400
        )
        
        return fig

if __name__ == "__main__":
    panel = ActionPanel()
    print("Action Panel initialized")
