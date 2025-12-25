"""
Multivariate analysis module for entropy features and outcomes.

Implements multiple approaches to capture complex relationships:
1. Elastic Net Regression (with cross-validation)
2. PCA + Linear Regression
3. Partial Least Squares (PLS) Regression
4. Random Forest Regression
5. Interaction models (stress × features)

Handles the challenges of:
- Small sample size (n ≈ 60-66)
- High dimensionality (20+ features)
- Multicollinearity among entropy features
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, LeaveOneOut, KFold
from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

from data_loader import merge_all_data, get_feature_names
from analysis import get_stress_group, ALL_OUTCOMES


def prepare_data(df, feature_cols, outcome_col, include_stress=True):
    """
    Prepare data for modeling: handle missing values, scale features.

    Returns X, y, feature_names, and the scaler
    """
    # Select columns
    cols = feature_cols.copy()
    df = df.copy()

    # Convert all feature columns to numeric
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert outcome to numeric
    df[outcome_col] = pd.to_numeric(df[outcome_col], errors='coerce')

    if include_stress and 'stress_group' in df.columns:
        df['stress_binary'] = (df['stress_group'] == 'stressed').astype(int)
        cols = cols + ['stress_binary']

    # Get complete cases
    all_cols = cols + [outcome_col]
    subset = df[all_cols].dropna()

    if len(subset) < 10:
        return None, None, None, None

    X = subset[cols].astype(float).values
    y = subset[outcome_col].astype(float).values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, cols, scaler


def compute_vif(X, feature_names):
    """Compute Variance Inflation Factors for multicollinearity assessment."""
    vif_data = []
    for i in range(X.shape[1]):
        vif = variance_inflation_factor(X, i)
        vif_data.append({'feature': feature_names[i], 'VIF': vif})
    return pd.DataFrame(vif_data).sort_values('VIF', ascending=False)


def elastic_net_analysis(X, y, feature_names, cv=5):
    """
    Elastic Net regression with cross-validation for alpha and l1_ratio selection.
    """
    if len(y) < 20:
        cv = min(cv, len(y) // 2)

    # Elastic Net with CV
    model = ElasticNetCV(
        l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9, 0.95],
        alphas=np.logspace(-4, 1, 50),
        cv=cv,
        max_iter=10000,
        random_state=42
    )
    model.fit(X, y)

    # Cross-validated R²
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')

    # Feature importance (non-zero coefficients)
    coef_df = pd.DataFrame({
        'feature': feature_names,
        'coefficient': model.coef_
    })
    coef_df['abs_coef'] = np.abs(coef_df['coefficient'])
    coef_df = coef_df.sort_values('abs_coef', ascending=False)

    return {
        'model': model,
        'alpha': model.alpha_,
        'l1_ratio': model.l1_ratio_,
        'r2_train': model.score(X, y),
        'r2_cv_mean': cv_scores.mean(),
        'r2_cv_std': cv_scores.std(),
        'n_features_selected': np.sum(model.coef_ != 0),
        'coefficients': coef_df[coef_df['coefficient'] != 0]
    }


def pca_regression_analysis(X, y, feature_names, n_components=None, cv=5):
    """
    PCA followed by linear regression.
    Automatically selects n_components explaining 90% variance if not specified.
    """
    if len(y) < 20:
        cv = min(cv, len(y) // 2)

    # Determine n_components
    pca_full = PCA()
    pca_full.fit(X)
    cumvar = np.cumsum(pca_full.explained_variance_ratio_)

    if n_components is None:
        n_components = np.argmax(cumvar >= 0.90) + 1
        n_components = min(n_components, len(y) // 5)  # Rule of thumb: n/5 predictors max
        n_components = max(n_components, 2)

    # PCA + Ridge regression pipeline
    pipeline = Pipeline([
        ('pca', PCA(n_components=n_components)),
        ('ridge', RidgeCV(alphas=np.logspace(-3, 3, 50), cv=cv))
    ])
    pipeline.fit(X, y)

    # Cross-validated R²
    cv_scores = cross_val_score(pipeline, X, y, cv=cv, scoring='r2')

    # Get PCA loadings for interpretation
    pca = pipeline.named_steps['pca']
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(n_components)],
        index=feature_names
    )

    return {
        'model': pipeline,
        'n_components': n_components,
        'variance_explained': cumvar[n_components-1],
        'r2_train': pipeline.score(X, y),
        'r2_cv_mean': cv_scores.mean(),
        'r2_cv_std': cv_scores.std(),
        'loadings': loadings,
        'explained_variance_ratio': pca.explained_variance_ratio_
    }


def pls_regression_analysis(X, y, feature_names, cv=5):
    """
    Partial Least Squares regression - ideal for multicollinear predictors.
    """
    if len(y) < 20:
        cv = min(cv, len(y) // 2)

    # Find optimal n_components via CV
    max_components = min(X.shape[1], len(y) // 3, 10)
    best_score = -np.inf
    best_n = 2

    for n in range(2, max_components + 1):
        pls = PLSRegression(n_components=n)
        scores = cross_val_score(pls, X, y, cv=cv, scoring='r2')
        if scores.mean() > best_score:
            best_score = scores.mean()
            best_n = n

    # Fit final model
    model = PLSRegression(n_components=best_n)
    model.fit(X, y)

    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')

    # Feature importance from loadings
    loadings = pd.DataFrame({
        'feature': feature_names,
        'loading': np.abs(model.x_loadings_[:, 0])
    }).sort_values('loading', ascending=False)

    return {
        'model': model,
        'n_components': best_n,
        'r2_train': r2_score(y, model.predict(X)),
        'r2_cv_mean': cv_scores.mean(),
        'r2_cv_std': cv_scores.std(),
        'loadings': loadings
    }


def random_forest_analysis(X, y, feature_names, cv=5):
    """
    Random Forest regression for non-linear relationships.
    """
    if len(y) < 20:
        cv = min(cv, len(y) // 2)

    # Use conservative hyperparameters for small samples
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=3,  # Shallow trees to prevent overfitting
        min_samples_leaf=5,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)

    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')

    # Feature importance
    importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    return {
        'model': model,
        'r2_train': model.score(X, y),
        'r2_cv_mean': cv_scores.mean(),
        'r2_cv_std': cv_scores.std(),
        'feature_importance': importance
    }


def interaction_model_analysis(df, feature_cols, outcome_col):
    """
    OLS regression with stress × feature interactions.
    Tests whether stress moderates the feature-outcome relationships.
    """
    # Prepare data
    df_model = df.copy()
    df_model['stress_binary'] = (df_model['stress_group'] == 'stressed').astype(int)

    # Select top features based on univariate correlation to limit model complexity
    correlations = []
    for feat in feature_cols:
        if feat not in df_model.columns:
            continue
        x = pd.to_numeric(df_model[feat], errors='coerce')
        y = pd.to_numeric(df_model[outcome_col], errors='coerce')
        mask = x.notna() & y.notna()
        if mask.sum() < 10:
            continue
        r, p = stats.spearmanr(x[mask], y[mask])
        correlations.append({'feature': feat, 'r': abs(r), 'p': p})

    if not correlations:
        return None

    corr_df = pd.DataFrame(correlations).sort_values('r', ascending=False)
    top_features = corr_df.head(5)['feature'].tolist()

    # Build model with interactions
    cols_needed = top_features + ['stress_binary', outcome_col]
    subset = df_model[cols_needed].dropna()

    if len(subset) < 20:
        return None

    # Standardize features
    scaler = StandardScaler()
    X_features = scaler.fit_transform(subset[top_features])

    # Create design matrix with interactions
    X_dict = {'const': 1}
    for i, feat in enumerate(top_features):
        feat_short = feat.replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
        X_dict[feat_short] = X_features[:, i]
    X_dict['stress'] = subset['stress_binary'].values

    # Add interactions
    for i, feat in enumerate(top_features):
        feat_short = feat.replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
        X_dict[f'{feat_short}:stress'] = X_features[:, i] * subset['stress_binary'].values

    X = pd.DataFrame(X_dict)
    y = subset[outcome_col].values

    # Fit OLS
    model = sm.OLS(y, X).fit()

    return {
        'model': model,
        'summary': model.summary(),
        'r2': model.rsquared,
        'r2_adj': model.rsquared_adj,
        'f_pvalue': model.f_pvalue,
        'params': model.params,
        'pvalues': model.pvalues,
        'significant_interactions': model.pvalues[model.pvalues.index.str.contains(':stress')] < 0.05
    }


def run_multivariate_analysis(df, feature_cols, outcome_col, output_dir):
    """
    Run all multivariate analyses for a given outcome.
    """
    results = {'outcome': outcome_col}

    # Prepare data
    X, y, feat_names, scaler = prepare_data(df, feature_cols, outcome_col, include_stress=True)

    if X is None:
        print(f"  Insufficient data for {outcome_col}")
        return None

    print(f"\n  Sample size: n = {len(y)}")
    print(f"  Features: {len(feat_names)} (including stress indicator)")

    # 1. Multicollinearity check
    print("\n  1. Multicollinearity Assessment (VIF)")
    vif = compute_vif(X, feat_names)
    high_vif = vif[vif['VIF'] > 10]
    print(f"     Features with VIF > 10: {len(high_vif)}")
    if len(high_vif) > 0:
        print(f"     Top 3: {high_vif.head(3)['feature'].tolist()}")
    results['vif'] = vif

    # 2. Elastic Net
    print("\n  2. Elastic Net Regression")
    try:
        en_results = elastic_net_analysis(X, y, feat_names)
        print(f"     R² (train): {en_results['r2_train']:.3f}")
        print(f"     R² (CV):    {en_results['r2_cv_mean']:.3f} ± {en_results['r2_cv_std']:.3f}")
        print(f"     Features selected: {en_results['n_features_selected']}/{len(feat_names)}")
        print(f"     Best alpha: {en_results['alpha']:.4f}, L1 ratio: {en_results['l1_ratio']:.2f}")
        if len(en_results['coefficients']) > 0:
            print(f"     Top features:")
            for _, row in en_results['coefficients'].head(5).iterrows():
                feat_short = row['feature'].replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
                print(f"       {feat_short}: β = {row['coefficient']:.3f}")
        results['elastic_net'] = en_results
    except Exception as e:
        print(f"     Error: {e}")
        results['elastic_net'] = None

    # 3. PCA + Regression
    print("\n  3. PCA + Ridge Regression")
    try:
        pca_results = pca_regression_analysis(X, y, feat_names)
        print(f"     Components: {pca_results['n_components']} (explaining {pca_results['variance_explained']*100:.1f}% variance)")
        print(f"     R² (train): {pca_results['r2_train']:.3f}")
        print(f"     R² (CV):    {pca_results['r2_cv_mean']:.3f} ± {pca_results['r2_cv_std']:.3f}")
        results['pca_regression'] = pca_results
    except Exception as e:
        print(f"     Error: {e}")
        results['pca_regression'] = None

    # 4. PLS Regression
    print("\n  4. Partial Least Squares (PLS) Regression")
    try:
        pls_results = pls_regression_analysis(X, y, feat_names)
        print(f"     Components: {pls_results['n_components']}")
        print(f"     R² (train): {pls_results['r2_train']:.3f}")
        print(f"     R² (CV):    {pls_results['r2_cv_mean']:.3f} ± {pls_results['r2_cv_std']:.3f}")
        print(f"     Top loading features:")
        for _, row in pls_results['loadings'].head(3).iterrows():
            feat_short = row['feature'].replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
            print(f"       {feat_short}: {row['loading']:.3f}")
        results['pls'] = pls_results
    except Exception as e:
        print(f"     Error: {e}")
        results['pls'] = None

    # 5. Random Forest
    print("\n  5. Random Forest Regression")
    try:
        rf_results = random_forest_analysis(X, y, feat_names)
        print(f"     R² (train): {rf_results['r2_train']:.3f}")
        print(f"     R² (CV):    {rf_results['r2_cv_mean']:.3f} ± {rf_results['r2_cv_std']:.3f}")
        print(f"     Top important features:")
        for _, row in rf_results['feature_importance'].head(5).iterrows():
            feat_short = row['feature'].replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
            print(f"       {feat_short}: {row['importance']:.3f}")
        results['random_forest'] = rf_results
    except Exception as e:
        print(f"     Error: {e}")
        results['random_forest'] = None

    # 6. Parsimonious Regression (recommended for small samples)
    print("\n  6. Parsimonious Regression (forward selection, max 3 features)")
    try:
        feature_cols_only = [f for f in feat_names if f != 'stress_binary']
        pars_results = parsimonious_regression(df, feature_cols_only, outcome_col, max_features=3)
        if pars_results:
            print(f"     Selected features: {pars_results['n_features']}")
            for feat in pars_results['selected_features']:
                feat_short = feat.replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
                print(f"       - {feat_short}")
            print(f"     Model without interactions:")
            print(f"       R² (adj): {pars_results['r2_adj_no_int']:.3f}, AIC: {pars_results['aic_no_int']:.1f}")
            print(f"     Model with stress interactions:")
            print(f"       R² (adj): {pars_results['r2_adj_with_int']:.3f}, AIC: {pars_results['aic_with_int']:.1f}")

            # Show coefficients
            model = pars_results['model_with_interactions']
            print(f"\n     Coefficient estimates (with interactions):")
            for var in model.params.index:
                if var == 'const':
                    continue
                coef = model.params[var]
                pval = model.pvalues[var]
                sig = '*' if pval < 0.05 else ('†' if pval < 0.10 else '')
                print(f"       {var:25}: β = {coef:+.3f}, p = {pval:.4f} {sig}")

            results['parsimonious'] = pars_results
        else:
            print(f"     Insufficient data")
            results['parsimonious'] = None
    except Exception as e:
        print(f"     Error: {e}")
        results['parsimonious'] = None

    return results


def parsimonious_regression(df, feature_cols, outcome_col, max_features=3):
    """
    Parsimonious regression using only top correlated features.
    More appropriate for small samples (n/k ratio > 10).

    Uses forward selection based on adjusted R².
    """
    df = df.copy()

    # Convert to numeric
    for col in feature_cols + [outcome_col]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df['stress_binary'] = (df['stress_group'] == 'stressed').astype(int)

    # Get complete cases for outcome
    subset = df[feature_cols + [outcome_col, 'stress_binary']].dropna()

    if len(subset) < 15:
        return None

    y = subset[outcome_col].values

    # Rank features by absolute correlation
    correlations = []
    for feat in feature_cols:
        x = subset[feat].values
        r, p = stats.spearmanr(x, y)
        if not np.isnan(r):
            correlations.append({'feature': feat, 'r': abs(r), 'p': p, 'sign': np.sign(r)})

    corr_df = pd.DataFrame(correlations).sort_values('r', ascending=False)
    candidate_features = corr_df['feature'].tolist()

    # Forward selection
    selected = []
    best_adj_r2 = -np.inf
    scaler = StandardScaler()

    for feat in candidate_features[:max_features * 2]:  # Consider top candidates
        test_features = selected + [feat]

        X = subset[test_features].values
        X_scaled = scaler.fit_transform(X)
        X_with_const = sm.add_constant(X_scaled)

        try:
            model = sm.OLS(y, X_with_const).fit()
            if model.rsquared_adj > best_adj_r2:
                best_adj_r2 = model.rsquared_adj
                selected = test_features.copy()

            if len(selected) >= max_features:
                break
        except:
            continue

    if not selected:
        return None

    # Fit final model with stress interaction
    X_final = subset[selected].values
    X_scaled = scaler.fit_transform(X_final)

    # Build design matrix
    design_dict = {'const': np.ones(len(y))}
    for i, feat in enumerate(selected):
        feat_short = feat.replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
        design_dict[feat_short] = X_scaled[:, i]

    design_dict['stress'] = subset['stress_binary'].values

    # Add interactions
    for i, feat in enumerate(selected):
        feat_short = feat.replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
        design_dict[f'{feat_short}:stress'] = X_scaled[:, i] * subset['stress_binary'].values

    X_design = pd.DataFrame(design_dict)
    model = sm.OLS(y, X_design).fit()

    # Also fit model without interactions for comparison
    X_no_int = X_design[[c for c in X_design.columns if ':stress' not in c]]
    model_no_int = sm.OLS(y, X_no_int).fit()

    return {
        'selected_features': selected,
        'n': len(y),
        'n_features': len(selected),
        'model_with_interactions': model,
        'model_no_interactions': model_no_int,
        'r2_adj_no_int': model_no_int.rsquared_adj,
        'r2_adj_with_int': model.rsquared_adj,
        'aic_no_int': model_no_int.aic,
        'aic_with_int': model.aic,
        'feature_correlations': corr_df.head(10)
    }


def compare_models(results_dict):
    """
    Create comparison table of model performance across outcomes.
    """
    rows = []
    for outcome, results in results_dict.items():
        if results is None:
            continue
        row = {'outcome': outcome}
        for model_name in ['elastic_net', 'pca_regression', 'pls', 'random_forest']:
            if results.get(model_name):
                row[f'{model_name}_r2_cv'] = results[model_name]['r2_cv_mean']
        rows.append(row)

    return pd.DataFrame(rows)


def main():
    """Run complete multivariate analysis."""
    data_dir = Path(__file__).parent.parent
    output_dir = data_dir / 'output'

    print("=" * 70)
    print("MULTIVARIATE ANALYSIS")
    print("Entropy Features → Neurodevelopmental Outcomes")
    print("=" * 70)

    # Load data
    print("\nLoading data...")
    df = merge_all_data(data_dir)
    df['stress_group'] = get_stress_group(df)

    # Get feature columns
    feature_cols = get_feature_names()
    feature_cols = [f for f in feature_cols if f in df.columns]

    print(f"Total subjects: {len(df)}")
    print(f"Features: {len(feature_cols)}")

    # Define outcomes
    outcomes = [
        'COG COMPOSITE SCORE',
        'LANG COMP SCORE',
        'MOTOR COMPOSITE SCORE',
        'MOTOR FINE  SKILLS SCORE',
    ]
    outcomes = [o for o in outcomes if o in df.columns]

    # Run analysis for each outcome
    all_results = {}
    for outcome in outcomes:
        print("\n" + "=" * 70)
        print(f"OUTCOME: {outcome}")
        print("=" * 70)

        results = run_multivariate_analysis(df, feature_cols, outcome, output_dir)
        all_results[outcome] = results

    # Model comparison
    print("\n" + "=" * 70)
    print("MODEL COMPARISON (Cross-validated R²)")
    print("=" * 70)

    comparison = compare_models(all_results)
    if not comparison.empty:
        print("\n" + comparison.to_string(index=False))
        comparison.to_csv(output_dir / 'multivariate_model_comparison.csv', index=False)

    # Save detailed results
    print("\n" + "=" * 70)
    print("Analysis complete. Results saved to output/")
    print("=" * 70)

    return all_results


if __name__ == '__main__':
    main()
