-- Cross-platform diffusion view
CREATE OR REPLACE VIEW `{PROJECT_ID}.{DATASET_ID}.cross_platform_diffusion_view` AS
SELECT 
  s.meme_id,
  s.text,
  s.meme_seriousness_threshold,
  s.irony_collapse_index,
  v.primary_visual_metaphor,
  v.shopping_correlation_score,
  s.processing_timestamp,
  CASE 
    WHEN s.irony_collapse_index < 0.3 THEN 'Reddit_Early'
    WHEN s.irony_collapse_index BETWEEN 0.3 AND 0.6 THEN 'TikTok_Viral'
    WHEN s.irony_collapse_index BETWEEN 0.6 AND 0.8 THEN 'YouTube_Mainstream'
    ELSE 'Google_Search_Peak'
  END as diffusion_stage,
  s.irony_collapse_index * v.shopping_correlation_score as diffusion_velocity
FROM `{PROJECT_ID}.{DATASET_ID}.semantic_scores` s
LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.visual_metadata` v
ON s.meme_id = v.meme_id
WHERE s.irony_collapse_index IS NOT NULL;

-- Unified market intelligence view
CREATE OR REPLACE VIEW `{PROJECT_ID}.{DATASET_ID}.unified_market_intelligence` AS
SELECT 
  s.meme_id,
  s.text,
  s.meme_seriousness_threshold,
  s.irony_collapse_index,
  v.primary_visual_metaphor,
  v.shopping_correlation_score,
  s.processing_timestamp
FROM `{PROJECT_ID}.{DATASET_ID}.semantic_scores` s
LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.visual_metadata` v
ON s.meme_id = v.meme_id
WHERE s.meme_seriousness_threshold IS NOT NULL;
