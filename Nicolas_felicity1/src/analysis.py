"""
Analysis module for TE and entropy features in relation to biomarkers.

Replicates and extends Section 3.4 of the manuscript:
"TE in relation to other biomarkers"

Features analyzed:
- Entropy rate (from entropy_rate.txt): Feature 1-10
- Sample entropy (from SampEn.txt): Feature 11-20

Outcome variables:
- Neurodevelopmental: COG_COMPOSITE_SCORE, LANG_*, MOTOR_*
- Stress indicators: PSS, PDQ, cortisol
- Group: stressed vs control (PSS >= 19)
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings

from data_loader import merge_all_data, get_feature_names


# Outcome columns of interest
OUTCOME_COLS = {
    'stress_indicators': [
        'Mother Score_PSS',
        'Mother Score PDQ',
        'Mother CORTISOL (pg/mg of maternal hair)',
    ],
    'cognitive': [
        'COG COMPOSITE SCORE',
    ],
    'language': [
        'LANG RECEPT SCORE',
        'LANG EXPRES SCORE',
        'LANG COMP SCORE',
    ],
    'motor': [
        'MOTOR FINE  SKILLS SCORE',
        'MOTOR GROSS SKILLS SCORE',
        'MOTOR COMPOSITE SCORE',
    ],
}

# Flatten for convenience
ALL_OUTCOMES = []
for v in OUTCOME_COLS.values():
    ALL_OUTCOMES.extend(v)


def get_stress_group(df: pd.DataFrame) -> pd.Series:
    """
    Categorize subjects by stress status.
    PSS >= 19 = stressed, PSS < 19 = control
    """
    pss_col = 'Mother Score_PSS'
    if pss_col not in df.columns:
        # Try alternative column names
        for col in df.columns:
            if 'PSS' in col.upper() and 'SCORE' in col.upper():
                pss_col = col
                break

    return (df[pss_col] >= 19).map({True: 'stressed', False: 'control'})


def get_sex_group(df: pd.DataFrame) -> pd.Series:
    """Get fetus sex from dataframe."""
    sex_col = None
    for col in df.columns:
        if 'SEX' in col.upper() or 'GENDER' in col.upper():
            sex_col = col
            break

    if sex_col is None:
        return pd.Series(['unknown'] * len(df), index=df.index)

    return df[sex_col]


def test_normality(x: pd.Series, alpha: float = 0.05) -> tuple:
    """
    Test for normality using Shapiro-Wilk test.

    Args:
        x: Data series
        alpha: Significance level

    Returns:
        (is_normal, p_value)
    """
    if len(x) < 3:
        return False, np.nan

    # Shapiro-Wilk test (good for n < 5000)
    if len(x) <= 5000:
        stat, p = stats.shapiro(x)
    else:
        # For larger samples, use D'Agostino-Pearson
        stat, p = stats.normaltest(x)

    return p > alpha, p


def compute_correlations(
    df: pd.DataFrame,
    feature_cols: list,
    outcome_cols: list,
    method: str = 'auto'
) -> pd.DataFrame:
    """
    Compute correlations between features and outcomes.

    Args:
        df: Data frame with features and outcomes
        feature_cols: List of feature column names
        outcome_cols: List of outcome column names
        method: 'auto' (test normality), 'spearman', or 'pearson'

    Returns:
        DataFrame with correlation coefficients and p-values
    """
    results = []

    for feature in feature_cols:
        if feature not in df.columns:
            continue

        for outcome in outcome_cols:
            if outcome not in df.columns:
                continue

            # Convert to numeric and get valid pairs
            x = pd.to_numeric(df[feature], errors='coerce')
            y = pd.to_numeric(df[outcome], errors='coerce')

            mask = x.notna() & y.notna()
            x = x[mask]
            y = y[mask]

            if len(x) < 5:
                continue

            try:
                # Determine method based on normality if auto
                if method == 'auto':
                    x_normal, x_p = test_normality(x)
                    y_normal, y_p = test_normality(y)
                    use_pearson = x_normal and y_normal
                    used_method = 'pearson' if use_pearson else 'spearman'
                else:
                    used_method = method
                    x_normal = y_normal = None

                if used_method == 'pearson':
                    r, p = stats.pearsonr(x, y)
                else:
                    r, p = stats.spearmanr(x, y)

                results.append({
                    'feature': feature,
                    'outcome': outcome,
                    'r': r,
                    'p_value': p,
                    'n': len(x),
                    'method': used_method,
                    'x_normal': x_normal if method == 'auto' else None,
                    'y_normal': y_normal if method == 'auto' else None,
                })
            except Exception:
                continue

    return pd.DataFrame(results)


def compute_stratified_correlations(
    df: pd.DataFrame,
    feature_cols: list,
    outcome_cols: list,
    stratify_col: str,
    method: str = 'spearman'
) -> pd.DataFrame:
    """
    Compute correlations stratified by a grouping variable.
    """
    results = []

    groups = df[stratify_col].dropna().unique()

    for group in groups:
        group_df = df[df[stratify_col] == group]
        corr_df = compute_correlations(group_df, feature_cols, outcome_cols, method)
        corr_df['group'] = group
        results.append(corr_df)

    if results:
        return pd.concat(results, ignore_index=True)
    return pd.DataFrame()


def run_group_comparison(
    df: pd.DataFrame,
    feature_cols: list,
    group_col: str,
) -> pd.DataFrame:
    """
    Compare feature distributions between groups using Mann-Whitney U test.
    """
    results = []
    groups = df[group_col].dropna().unique()

    if len(groups) != 2:
        warnings.warn(f"Expected 2 groups, got {len(groups)}")
        return pd.DataFrame()

    g1, g2 = groups

    for feature in feature_cols:
        if feature not in df.columns:
            continue

        x1 = pd.to_numeric(df.loc[df[group_col] == g1, feature], errors='coerce').dropna()
        x2 = pd.to_numeric(df.loc[df[group_col] == g2, feature], errors='coerce').dropna()

        if len(x1) < 3 or len(x2) < 3:
            continue

        try:
            stat, p = stats.mannwhitneyu(x1, x2, alternative='two-sided')

            results.append({
                'feature': feature,
                f'median_{g1}': x1.median(),
                f'median_{g2}': x2.median(),
                f'n_{g1}': len(x1),
                f'n_{g2}': len(x2),
                'U_statistic': stat,
                'p_value': p,
            })
        except Exception:
            continue

    return pd.DataFrame(results)


def create_feature_labels() -> dict:
    """
    Create human-readable labels for features.

    Based on manuscript description:
    - Columns 1-10 in each file are estimates at different conditioning
    """
    labels = {}

    # Entropy rate features (Feature 1-10)
    er_cols = get_feature_names('entropy_rate')
    for i, col in enumerate(er_cols, start=1):
        labels[col] = f"Feature {i} (entropy_rate)"

    # SampEn features (Feature 11-20)
    se_cols = get_feature_names('sampen')
    for i, col in enumerate(se_cols, start=11):
        labels[col] = f"Feature {i} (sampen)"

    return labels


def main():
    """Run the complete analysis."""
    data_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("Analysis: Entropy Features in Relation to Biomarkers")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    df = merge_all_data(data_dir)
    print(f"  Total subjects: {len(df)}")

    # Add stress group
    df['stress_group'] = get_stress_group(df)
    print(f"  Stress distribution:")
    print(f"    {df['stress_group'].value_counts().to_dict()}")

    # Get feature columns
    feature_cols = get_feature_names()
    available_features = [c for c in feature_cols if c in df.columns]
    print(f"\n  Available features: {len(available_features)}")

    # Get available outcomes
    available_outcomes = [c for c in ALL_OUTCOMES if c in df.columns]
    print(f"  Available outcomes: {len(available_outcomes)}")
    for outcome in available_outcomes:
        n_valid = df[outcome].notna().sum()
        print(f"    {outcome}: n={n_valid}")

    # 1. Overall correlations
    print("\n" + "-" * 60)
    print("1. Overall Correlations (Features vs Outcomes)")
    print("-" * 60)

    corr_all = compute_correlations(df, available_features, available_outcomes)
    if not corr_all.empty:
        # Show significant correlations
        sig_corr = corr_all[corr_all['p_value'] < 0.05].sort_values('p_value')
        print(f"\nSignificant correlations (p < 0.05): {len(sig_corr)}")
        if len(sig_corr) > 0:
            print(sig_corr.head(20).to_string(index=False))

        # Save full results
        corr_all.to_csv(data_dir / 'output' / 'correlations_all.csv', index=False)

    # 2. Stratified by stress status
    print("\n" + "-" * 60)
    print("2. Correlations Stratified by Stress Status")
    print("-" * 60)

    corr_stress = compute_stratified_correlations(
        df, available_features, available_outcomes, 'stress_group'
    )
    if not corr_stress.empty:
        sig_stress = corr_stress[corr_stress['p_value'] < 0.05].sort_values('p_value')
        print(f"\nSignificant correlations (p < 0.05): {len(sig_stress)}")
        if len(sig_stress) > 0:
            print(sig_stress.head(20).to_string(index=False))

        corr_stress.to_csv(data_dir / 'output' / 'correlations_by_stress.csv', index=False)

    # 3. Group comparisons (stressed vs control)
    print("\n" + "-" * 60)
    print("3. Feature Comparisons: Stressed vs Control")
    print("-" * 60)

    group_comp = run_group_comparison(df, available_features, 'stress_group')
    if not group_comp.empty:
        sig_diff = group_comp[group_comp['p_value'] < 0.05].sort_values('p_value')
        print(f"\nSignificant differences (p < 0.05): {len(sig_diff)}")
        if len(sig_diff) > 0:
            print(sig_diff.to_string(index=False))

        group_comp.to_csv(data_dir / 'output' / 'group_comparison_stress.csv', index=False)

    # 4. Correlation with stress scores (PSS, PDQ)
    print("\n" + "-" * 60)
    print("4. Correlations with Stress Scores")
    print("-" * 60)

    stress_cols = ['Mother Score_PSS', 'Mother Score PDQ']
    stress_cols = [c for c in stress_cols if c in df.columns]

    corr_stress_scores = compute_correlations(df, available_features, stress_cols)
    if not corr_stress_scores.empty:
        sig = corr_stress_scores[corr_stress_scores['p_value'] < 0.1].sort_values('p_value')
        print(f"\nCorrelations with p < 0.1: {len(sig)}")
        if len(sig) > 0:
            print(sig.to_string(index=False))

        corr_stress_scores.to_csv(
            data_dir / 'output' / 'correlations_stress_scores.csv', index=False
        )

    print("\n" + "=" * 60)
    print("Analysis complete. Results saved to output/")
    print("=" * 60)

    return df, corr_all, corr_stress, group_comp


if __name__ == '__main__':
    main()
