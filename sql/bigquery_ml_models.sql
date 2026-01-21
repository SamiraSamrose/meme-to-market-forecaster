CREATE OR REPLACE MODEL `{PROJECT_ID}.{DATASET_ID}.slang_acceleration_predictor`
OPTIONS(
  model_type='LINEAR_REG',
  input_label_cols=['market_impact_score'],
  data_split_method='AUTO_SPLIT',
  data_split_eval_fraction=0.2,
  enable_global_explain=TRUE
) AS
SELECT
  meme_seriousness_threshold,
  irony_collapse_index,
  financial_keywords_count,
  humor_keywords_count,
  CAST(financial_keywords_count AS FLOAT64) / NULLIF(CAST(humor_keywords_count AS FLOAT64), 0) as slang_acceleration_rate,
  irony_collapse_index * meme_seriousness_threshold as combined_readiness,
  meme_seriousness_threshold * 0.4 + irony_collapse_index * 0.6 as market_impact_score
FROM `{PROJECT_ID}.{DATASET_ID}.semantic_scores`
WHERE meme_seriousness_threshold IS NOT NULL
  AND irony_collapse_index IS NOT NULL;
