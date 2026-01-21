import pandas as pd
import numpy as np
from scipy import stats

class StatisticalAnalyzer:
    def __init__(self):
        pass
        
    def correlation_analysis(self, df, columns):
        """Calculate correlation matrix for key metrics"""
        
        corr_matrix = df[columns].corr()
        print("Correlation Matrix:")
        print(corr_matrix.round(3))
        
        return corr_matrix
    
    def ici_ttest(self, df):
        """T-test comparing high vs low ICI groups"""
        
        high_ici = df[df['irony_collapse_index'] > 0.7]['predicted_readiness']
        low_ici = df[df['irony_collapse_index'] < 0.3]['predicted_readiness']
        
        if len(high_ici) > 0 and len(low_ici) > 0:
            t_stat, p_value = stats.ttest_ind(high_ici, low_ici)
            
            result = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
            
            print(f"\nT-Test: High ICI vs Low ICI Impact")
            print(f"  t-statistic: {t_stat:.4f}")
            print(f"  p-value: {p_value:.4f}")
            print(f"  Significant: {'Yes' if p_value < 0.05 else 'No'}")
            
            return result
        
        return None
    
    def impact_category_anova(self, df):
        """ANOVA test across impact categories"""
        
        if 'impact_category' not in df.columns:
            return None
        
        impact_groups = [
            df[df['impact_category'] == cat]['predicted_readiness'].values
            for cat in df['impact_category'].unique()
            if len(df[df['impact_category'] == cat]) > 0
        ]
        
        if len(impact_groups) > 1:
            f_stat, p_value = stats.f_oneway(*impact_groups)
            
            result = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
            
            print(f"\nANOVA: Impact Categories")
            print(f"  F-statistic: {f_stat:.4f}")
            print(f"  p-value: {p_value:.4f}")
            print(f"  Significant: {'Yes' if p_value < 0.05 else 'No'}")
            
            return result
        
        return None
    
    def residual_analysis(self, y_true, y_pred):
        """Analyze prediction residuals"""
        
        residuals = y_true - y_pred
        
        analysis = {
            'mean_residual': residuals.mean(),
            'std_residual': residuals.std(),
            'skewness': stats.skew(residuals),
            'kurtosis': stats.kurtosis(residuals)
        }
        
        print("\nResidual Analysis:")
        print(f"  Mean Residual: {analysis['mean_residual']:.4f}")
        print(f"  Std Dev: {analysis['std_residual']:.4f}")
        print(f"  Skewness: {analysis['skewness']:.4f}")
        print(f"  Kurtosis: {analysis['kurtosis']:.4f}")
        
        return analysis

if __name__ == "__main__":
    analyzer = StatisticalAnalyzer()
    print("Statistical Analyzer initialized")
