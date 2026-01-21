# Meme-to-Market Impact Forecaster

A Cultural-to-Financial Intelligence Hub that converts unstructured meme data into actionable market signals using Hex, BigQuery and Vertex AI.

## Overview

Memes moved $20B in market cap during GME, but advertisers had zero warning before keyword costs spiked 340%. This system quantifies when jokes become financial actions 48 hours early, protecting ad budgets and enabling proactive brand safety filtering.

It predicts when internet memes acquire economic mass to impact advertising ecosystems and financial markets by analyzing cross-platform diffusion patterns from Reddit through TikTok to Google Search. The system built on Hex that converts unstructured internet meme data into quantified financial market signals. 

## Links
- **Source Code**: https://github.com/SamiraSamrose/meme-to-market-forecaster
- **Video Demo**: https://youtu.be/5PlcKkNkWHg

## Architecture

- **Orchestration Layer**: Hex Notebooks
- **Data Warehouse**: Google BigQuery
- **AI Engine**: Vertex AI (Gemini 3)
- **Storage**: Google Cloud Storage
- **Visualization**: Plotly, Looker

## Features

### Data Sources Integration
- BigQuery Public Datasets (Reddit comments)
- Google Trends API Alpha (real-time search velocity)
- TikTok Open API (viral trend data)
- KnowYourMeme (semantic grounding)

### Semantic Analysis
- Meme Seriousness Threshold calculation
- Irony Collapse Index tracking
- Vector clustering against historical market movers
- Multimodal visual metaphor detection

### Market Prediction
- 24/48/72-hour impact probability forecasting
- Slang acceleration rate analysis
- BigQuery ML regression models
- Cross-platform diffusion tracking

### Brand Safety
- Weaponized meme detection
- Toxicity scoring
- Automated monitoring alerts
- Keyword exclusion recommendations

### UI Dashboards
- Pulse Dashboard (cross-platform heatmaps, ICI meters)
- Semantic Analysis Workspace (multimodal previews, acceleration charts)
- Action & Integration Panel (Google Ads alerts, export functions)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `config/credentials.json.template` to `config/credentials.json`
2. Add your Google Cloud project credentials
3. Update `config/settings.py` with your project parameters

## Usage

### Data Collection
```bash
python -m src.data_collection.bigquery_reddit
python -m src.data_collection.google_trends
python -m src.data_collection.tiktok_api
```

### Semantic Analysis
```bash
python -m src.semantic_analysis.semantic_scoring
python -m src.semantic_analysis.vector_clustering
```

### Model Training
```bash
python -m src.modeling.market_impact_predictor
```

### Dashboard
```bash
python -m src.visualization.pulse_dashboard
```

## Requirements

- Python 3.9+
- Google Cloud Project with BigQuery, Vertex AI, Storage enabled
- Hex workspace (optional for full integration)
- API keys: Google Trends, TikTok

## Functionalities

**Meme Seriousness Threshold Calculation**: Analyzes text to compute ratio of financial keywords to humor keywords on 0-1 scale for intent classification.

**Irony Collapse Index Tracking**: Quantifies transition from ironic meme sharing to sincere financial action using keyword frequency patterns.

**Cross-Platform Diffusion Monitoring**: Tracks meme progression from Reddit to TikTok to Google Search with velocity metrics.

**Vector Clustering Against Historical Benchmarks**: Compares memes to DOGE, GME, NFT, SHIB using 20-dimensional cosine similarity.

**24/48/72-Hour Impact Probability Forecasting**: Predicts market movement likelihood across three time windows using regression models.

**Slang Acceleration Rate Measurement**: Calculates term usage velocity and acceleration across platforms.

**Toxicity Pattern Detection**: Identifies weaponized memes through four-category regex matching and KnowYourMeme cross-reference.

**Visual Metaphor Extraction**: Detects core visual elements (rocket, moon, diamond) and correlates with Google Shopping trends.

**Google Ads Keyword Intelligence**: Generates targeting opportunities and exclusion recommendations with CPC impact projections.

**Automated Brand Safety Alerts**: Creates severity-ranked warnings for toxic memes with high market impact potential.

**BigQuery ML Model Training**: Builds SQL-based regression models for scalable prediction within data warehouse.

**Multi-Modal Dashboard Rendering**: Displays heatmaps, gauges, time series, scatter plots across three interface layers.

**Google Sheets Writeback**: Exports betting odds versus real-world impact data for stakeholder tracking.

**Model Health Monitoring**: Tracks R² scores, data freshness and prediction accuracy across four model types.

**Narrative Report Generation**: Creates executive summaries using AI analysis of semantic patterns and platform diffusion.

## Target audience

Target audience includes digital advertising agencies managing Google Ads budgets, financial compliance teams monitoring market manipulation and consumer brands tracking viral trends for product launches. Operators run Hex notebook cells daily or schedule automated execution, review dashboard alerts for ICI thresholds above 0.8 and export keyword recommendations to Google Sheets for campaign adjustments within 48-hour prediction windows.

## License

MIT License