# Multivariate Analysis Results (Updated with TE Metrics)

## Overview

This analysis examined whether entropy rate (ER), sample entropy (SE), and transfer entropy (TE) features jointly predict neurodevelopmental outcomes, and whether maternal stress status moderates these relationships.

## Feature Set

| Feature Type | Count | Description |
|--------------|-------|-------------|
| Entropy Rate (ER) | 20 | max/mean × fetus/mother × 5 conditioning types |
| Sample Entropy (SE) | 20 | max/mean × fetus/mother × 5 conditioning types |
| Transfer Entropy (TE) | 12 | max/mean × 2 conditioning sources × 3 event types |
| **Total** | **52** | Plus stress indicator (53 predictors) |

### Transfer Entropy Features (New)
- `max_TE_fHR_*` / `mean_TE_fHR_*`: TE with fetal HR conditioning
- `max_TE_mHR_*` / `mean_TE_mHR_*`: TE with maternal HR conditioning
- Each computed on: all points, acceleration epochs, deceleration epochs

## Methods Applied

| Model | Purpose | Strengths |
|-------|---------|-----------|
| **Elastic Net** | Regularized regression with L1+L2 penalty | Handles multicollinearity, performs feature selection |
| **PCA + Ridge** | Dimensionality reduction then regression | Addresses multicollinearity through orthogonal transformation |
| **PLS Regression** | Partial least squares | Designed for high-dimensional, multicollinear predictors |
| **Random Forest** | Non-parametric ensemble | Captures non-linear relationships |
| **Parsimonious OLS** | Forward selection (max 3 features) | Appropriate for small samples |

## Key Findings

### 1. Sample Size Limitations (Critical)

| Outcome | n | Features | n/k ratio |
|---------|---|----------|-----------:|
| COG Composite | 34 | 53 | 0.6 |
| LANG Composite | 30 | 53 | 0.6 |
| MOTOR Composite | 33 | 53 | 0.6 |
| MOTOR Fine Skills | 33 | 53 | 0.6 |

**Critical issue:** The n/k ratio should be >10-20 for reliable multivariate inference. With 52 features and n~30, we have severe underpowering (ratio ~0.6).

### 2. Multicollinearity Assessment

Variance Inflation Factor (VIF) analysis revealed extreme multicollinearity:

| Outcome | Features with VIF > 10 |
|---------|----------------------:|
| COG Composite | 30/33 (91%) |
| LANG Composite | 31/33 (94%) |
| MOTOR Composite | 30/33 (91%) |
| MOTOR Fine Skills | 30/33 (91%) |

**Highest VIF features:**
- `max_TE_mHR_all`, `max_TE_fHR_all`, `mean_TE_mHR_all` (TE features using "all" points)
- These TE "all" features are mathematically related, explaining the extreme VIF

### 3. Model Performance (Cross-Validated R²)

| Outcome | Elastic Net | PCA+Ridge | PLS | Random Forest |
|---------|------------:|----------:|----:|--------------:|
| COG Composite | -0.10 | -0.06 | -0.79 | -0.10 |
| LANG Composite | -0.42 | -0.57 | -1.23 | -0.40 |
| MOTOR Composite | -0.49 | -0.52 | -0.99 | -0.43 |
| MOTOR Fine Skills | -0.23 | -0.01 | **+0.10** | -0.19 |

**Interpretation:**
- Negative CV-R² indicates models perform worse than predicting the mean
- Only PLS for Motor Fine Skills achieved marginally positive CV-R² (+0.10)
- This reflects severe overfitting due to high dimensionality and small samples

### 4. TE Features in Model Selection

**Elastic Net Selected Features (COG Composite):**
| Feature | Coefficient |
|---------|------------:|
| SE_mother_mHR_accel | +0.095 |
| stress_binary | -0.094 |
| max_TE_fHR_all | -0.067 |
| max_TE_mHR_all | -0.067 |
| SE_fetus_mHR_accel | +0.053 |

TE features were selected by Elastic Net, but with small coefficients.

**Random Forest Feature Importance (Top 5 per outcome):**

| Outcome | Top Features | Importance |
|---------|--------------|----------:|
| COG | SE_fetus_full | 0.109 |
| COG | mean_TE_fHR_all | 0.065 |
| COG | max_TE_fHR_all | 0.061 |
| MOTOR Composite | max_TE_fHR_all | 0.079 |
| MOTOR Composite | max_TE_mHR_decel | 0.071 |
| MOTOR Fine | max_TE_mHR_decel | 0.092 |

TE features consistently appear among top Random Forest predictors, particularly for motor outcomes.

### 5. Parsimonious Regression Results

Using forward selection with maximum 3 features:

#### COG Composite Score
- **Selected features:** mean_TE_mHR_all, SE_mother_mHR_accel
- R²(adj) = 0.067 (without interactions)
- No significant predictors

#### LANG Composite Score
- **Selected feature:** SE_mother_mHR_decel
- R²(adj) = 0.116 (without interactions)
- Stress main effect: β = -13.4, p = 0.051 (marginally significant)

#### MOTOR Composite Score
- **Selected features:** max_TE_fHR_all, max_TE_mHR_all, SE_mother_fHR_accel
- R²(adj) = 0.082 (without interactions)
- TE features selected but not individually significant

#### MOTOR Fine Skills Score
- **Selected features:** SE_fetus_mHR_accel, max_TE_fHR_all
- R²(adj) = 0.007 (without interactions)
- No significant predictors

### 6. PLS Loading Analysis

PLS identifies latent components that best explain outcome variance:

**Top Loading Features by Outcome:**

| Outcome | Feature | Loading |
|---------|---------|--------:|
| COG | max_TE_mHR_all | 0.430 |
| COG | max_TE_fHR_all | 0.430 |
| COG | mean_TE_mHR_all | 0.416 |
| LANG | ER_mother_mHR_accel | 0.364 |
| LANG | ER_mother_full | 0.349 |
| MOTOR | ER_mother_mHR_decel | 0.353 |
| MOTOR Fine | mean_TE_mHR_all | 0.381 |

**Pattern:** TE features dominate PLS loadings for COG and Motor Fine Skills, while ER features dominate for LANG and Motor Composite.

## TE-Specific Findings

### Univariate TE Correlations (from separate analysis)

All 7 significant TE correlations were with maternal cortisol:

| Feature | r | p-value |
|---------|--:|--------:|
| max_TE_mHR_decel | +0.315 | 0.003** |
| max_TE_mHR_accel | +0.287 | 0.007** |
| max_TE_fHR_decel | +0.271 | 0.011* |
| max_TE_fHR_accel | +0.250 | 0.019* |
| mean_TE_mHR_accel | +0.221 | 0.038* |
| mean_TE_mHR_decel | +0.217 | 0.042* |
| mean_TE_fHR_accel | +0.212 | 0.047* |

### TE vs ER/SE Pattern

| Feature Type | Primary Correlate | Bayley Associations |
|--------------|-------------------|---------------------|
| TE | Maternal cortisol (7 sig.) | None direct |
| ER | Few significant | Some in stratified analysis |
| SE | Few significant | Some in stratified analysis |

TE captures physiological stress response (cortisol) rather than directly predicting developmental outcomes.

## Recommendations

### For Current Analysis

1. **Primary findings: Univariate/stratified correlations** - Given severe underpowering, the stratified univariate analysis remains most interpretable.

2. **TE-cortisol relationship is robust** - The 7 significant TE-cortisol correlations suggest maternal-fetal coupling reflects chronic stress.

3. **Acknowledge multivariate limitations** - With n/k ≈ 0.6 and VIF > 10 for 90%+ of features, multivariate inference is unreliable.

4. **Motor Fine Skills shows promise** - PLS achieved positive CV-R² only for this outcome; TE features had highest importance.

### For Future Studies

1. **Increase sample size** - Minimum n = 500 recommended for 52 features (approximately 10 × 52)

2. **Pre-specify composites:**
   - ER_composite (PC1 from 20 ER features)
   - SE_composite (PC1 from 20 SE features)
   - TE_composite (PC1 from 12 TE features)
   - This reduces to 3 predictors

3. **Focus on epoch-specific TE** - "all points" TE shows extreme multicollinearity; accel/decel epochs are more informative

4. **Consider mediation models** - Test whether TE → Cortisol → Developmental outcomes (indirect pathway)

## Statistical Notes

- All features standardized (z-scored) before modeling
- Cross-validation: 5-fold CV (reduced when n < 20)
- Normality tested via Shapiro-Wilk for correlation method selection
- VIF calculated using variance_inflation_factor from statsmodels
- Significance: * p < 0.05, ** p < 0.01, † p < 0.10

## Conclusion

The multivariate analysis with 52 features (20 ER + 20 SE + 12 TE) reveals:

1. **Severe underpowering** (n ≈ 30-66 vs 53 predictors) prevents reliable multivariate inference

2. **Extreme multicollinearity** (90%+ features with VIF > 10) particularly among TE "all points" features

3. **TE features are selected by regularized models** and rank highly in Random Forest importance, especially for motor outcomes

4. **PLS shows marginal success** for Motor Fine Skills (CV-R² = +0.10), with TE features as top loadings

5. **Key substantive finding:** TE correlates with cortisol (stress marker) but not directly with Bayley scores, suggesting an indirect pathway through stress physiology

**Bottom line:** The univariate TE-cortisol correlations and stratified ER/SE-outcome analyses provide the most reliable and interpretable findings for this sample size. Multivariate models require larger samples (n > 500) for valid inference with all 52 features.
