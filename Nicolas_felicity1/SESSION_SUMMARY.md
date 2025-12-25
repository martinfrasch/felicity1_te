# Session Summary: Maternal-Fetal Heart Rate Entropy Analysis

## Project Overview

Analysis of entropy-based biomarkers from maternal-fetal heart rate recordings to predict neurodevelopmental outcomes (Bayley scores) and their relationship with maternal stress markers.

## Data Sources

| File | Description |
|------|-------------|
| `entropy_rate.txt` | 10 entropy rate features (11 columns: patient_code + 10 features) |
| `SampEn.txt` | 10 sample entropy features (same structure) |
| `max_TE_fHR_conditioning.csv` | Max TE with fetal HR conditioning |
| `max_TE_mHR_conditioning.csv` | Max TE with maternal HR conditioning |
| `mean_TE_fHR_conditioning.csv` | Mean TE with fetal HR conditioning |
| `mean_TE_mHR_conditioning.csv` | Mean TE with maternal HR conditioning |
| `210716 EXCEL FILE FOR BAYLEY-STAN.xlsx` | Clinical outcomes (Bayley scores, PSS, PDQ, cortisol) |

## Feature Structure

**32 total features:**
- **10 Entropy Rate (ER):** fetus_full, mother_full, fetus_fHR_accel, mother_fHR_accel, fetus_fHR_decel, mother_fHR_decel, fetus_mHR_accel, mother_mHR_accel, fetus_mHR_decel, mother_mHR_decel
- **10 Sample Entropy (SE):** Same structure as ER
- **12 Transfer Entropy (TE):** max/mean × fHR/mHR conditioning × all/accel/decel

**Outcome variables:**
- Stress markers: PSS, PDQ, Cortisol
- Bayley scores: COG, LANG (receptive, expressive, composite), MOTOR (fine, gross, composite)

## Key Findings

### 1. TE-Cortisol Relationship (Main Finding)
- **7 significant correlations** between TE and maternal cortisol (r = 0.21-0.31, all positive)
- Higher maternal-fetal HR coupling → higher chronic stress (cortisol)
- Epoch-specific TE (accel/decel) significant; "all points" TE not significant
- Max TE stronger than mean TE

### 2. ER/SE-Bayley Relationship
- **6 significant correlations** with motor and language outcomes
- SE during mHR accel → Motor Fine Skills (negative)
- SE during fHR accel → Language Receptive (positive)
- No correlations with cognitive scores or cortisol

### 3. Distinct Pathways
- **TE captures stress physiology** (cortisol) but NOT developmental outcomes
- **ER/SE predict development** but NOT stress markers
- Suggests indirect pathway: TE → Cortisol → Development

### 4. Moderating Effects
- **Stress-stratified:** Different patterns in stressed vs control groups; effect direction reversal for motor outcomes
- **Sex-stratified:** Female fetuses showed 9 significant TE correlations; males showed 0

### 5. Multivariate Models Failed
- n/k ratio ~1.0 (should be >10-20)
- 90%+ features with VIF > 10 (severe multicollinearity)
- Negative CV-R² for most models (overfitting)
- Only PLS for Motor Fine Skills achieved positive CV-R² (+0.10)

## Code Structure

```
src/
├── data_loader.py      # Load and merge all data sources
├── analysis.py         # Correlation analysis with normality testing
├── visualization.py    # Plotting functions
└── multivariate_analysis.py  # Elastic Net, PCA+Ridge, PLS, RF, parsimonious regression

output/
├── RESULTS_SUMMARY.md           # Main findings (manuscript style)
├── MULTIVARIATE_RESULTS.md      # Multivariate analysis details
├── TE_CORRELATION_SUMMARY.md    # TE-specific findings
├── MANUSCRIPT_SECTIONS.md       # Full Methods/Results/Discussion
├── MANUSCRIPT_SECTIONS.tex      # LaTeX version
├── correlations_TE.csv          # TE correlation results
├── correlations_all_features.csv
├── correlations_by_stress.csv
└── multivariate_model_comparison.csv
```

## Key Functions

```python
# Data loading
from src.data_loader import merge_all_data, get_feature_names, get_te_feature_names

# Analysis
from src.analysis import compute_correlations, test_normality, get_stress_group

# Multivariate
from src.multivariate_analysis import (
    elastic_net_analysis,
    pca_regression_analysis,
    pls_regression_analysis,
    random_forest_analysis,
    parsimonious_regression
)
```

## Statistical Methods

1. **Normality:** Shapiro-Wilk test (α = 0.05)
2. **Correlations:** Pearson if both normal, Spearman otherwise
3. **Stress classification:** PSS ≥ 19 = stressed
4. **Multivariate:** 5-fold CV, VIF for multicollinearity
5. **No multiple comparison correction** (exploratory analysis)

## Sample Sizes

| Analysis | n |
|----------|---|
| Total subjects | 120 |
| Cortisol | 88-90 |
| Bayley COG | 65-66 |
| Bayley LANG | 58-63 |
| Bayley MOTOR | 62-65 |
| Stressed group | 59 |
| Control group | 61 |

## Recommendations for Future Work

1. **Increase sample size** to n > 150 for multivariate inference
2. **Pre-register composite scores** (PC1 from each feature type) → reduces 32 features to 3
3. **Test mediation:** TE → Cortisol → Bayley outcomes
4. **Investigate sex-specific effects** with adequate power
5. **Focus on epoch-specific TE** (accel/decel), not "all points"

## Files Modified This Session

1. Created `output/TE_CORRELATION_SUMMARY.md` - Detailed TE analysis
2. Updated `output/MULTIVARIATE_RESULTS.md` - Added TE to multivariate models
3. Updated `output/RESULTS_SUMMARY.md` - Comprehensive combined results
4. Created `output/MANUSCRIPT_SECTIONS.md` - Full manuscript Methods/Results/Discussion
5. Created `output/MANUSCRIPT_SECTIONS.tex` - LaTeX version for journal submission

## Running the Analysis

```bash
# Run correlation analysis
python3 src/analysis.py

# Run multivariate analysis
python3 src/multivariate_analysis.py

# Check feature counts
python3 -c "from src.data_loader import get_feature_names; print(len(get_feature_names()))"
```

## Dependencies

```
pandas
numpy
scipy
scikit-learn
statsmodels
openpyxl  # for Excel files
matplotlib
seaborn
```
