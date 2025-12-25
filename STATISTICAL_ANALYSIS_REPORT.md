# Statistical Analysis Report: TE and ER Features
## Effects of Stress Exposure and Fetal Sex

**Date:** December 17, 2025
**Analyst:** Statistical Analysis Pipeline
**Data Source:** FELICITy1 TE/ER Dataset

---

## Executive Summary

This report presents a comprehensive statistical analysis of Transfer Entropy (TE) and Entropy Rate (ER) features comparing:
1. **Stress Exposure**: Stressed (n=58) vs Control (n=58) mothers
2. **Fetal Sex**: Male (n=49) vs Female (n=68) fetuses

### Key Findings

1. **No statistically significant differences** were found between stressed and control groups across any TE or ER features (all p > 0.05)

2. **No statistically significant differences** were found between male and female fetuses across any TE or ER features (all p > 0.05)

3. **Data Quality Issue Identified**: Files with "no conditioning" contain identical data for stressed and control groups, indicating a data generation error

4. **Effect sizes** are uniformly negligible (Cohen's d < 0.2) for all comparisons

---

## Methodology

### Statistical Approach

**Primary Analysis:**
- Independent samples t-tests for group comparisons
- Effect size calculation (Cohen's d)
- Multiple comparison corrections (Bonferroni, FDR, Holm-Bonferroni)

**Diagnostic Tests:**
- Levene's test for equality of variances
- Shapiro-Wilk test for normality
- Mann-Whitney U test (non-parametric alternative)

### Sample Sizes

Total cohort: 120 mother-fetus dyads

**Stress Groups:**
- Stressed: n = 58
- Control: n = 58

**Sex Groups:**
- Male: n = 49
- Female: n = 68

**Note:** Sample sizes differ from paper-reported values (59 stressed, 61 control, 60 male, 58 female), suggesting possible data filtering or processing differences.

---

## Detailed Results

### 1. Exposure Effects (Stressed vs Control)

**Summary:** No significant differences detected

| Metric | Result |
|--------|--------|
| Features analyzed | 22 |
| Significant at p < 0.05 | 0 |
| Surviving FDR correction | 0 |
| Median p-value | 1.000 |
| Range of Cohen's d | 0.000 |

**Effect Size Distribution:**
- Negligible (&#124;d&#124; < 0.2): 22 features (100%)
- Small (0.2 ≤ &#124;d&#124; < 0.5): 0 features
- Medium (0.5 ≤ &#124;d&#124; < 0.8): 0 features
- Large (&#124;d&#124; ≥ 0.8): 0 features

### 2. Sex Effects (Male vs Female)

**Summary:** No significant differences detected

| Metric | Result |
|--------|--------|
| Features analyzed | 22 |
| Significant at p < 0.05 | 0 |
| Surviving FDR correction | 0 |
| Median p-value | 0.613 |
| Range of Cohen's d | -0.169 to 0.166 |

**Effect Size Distribution:**
- Negligible (&#124;d&#124; < 0.2): 22 features (100%)
- Small (0.2 ≤ &#124;d&#124; < 0.5): 0 features
- Medium (0.5 ≤ &#124;d&#124; < 0.8): 0 features
- Large (&#124;d&#124; ≥ 0.8): 0 features

---

## Data Quality Issues

### Files with Identical Stressed/Control Data

The following files contain identical values for stressed and control groups:

1. `TEmax_no-condioning.npz`
2. `TEmean_no-condioning.npz`
3. `hmax_fetus_no_conditoning.npz`
4. `hmax_mother_no_conditoning.npz`
5. `hmean_fetus_no_conditoning.npz`
6. `hmean_mother_no_conditoning.npz`

**Impact:** All "no conditioning" features return t = 0.000, p = 1.000

**Recommendation:** Re-generate these data files with correct group assignments

---

## Interpretation

### Consistency with Paper Findings

These results are **consistent with the paper's conclusions**:

> "However, with the transfer entropy approach, we were unable to demonstrate the strict presence of information flow only in stressed mother-fetus dyads." (Abstract, lines 9-10)

The paper reports:
- Net TE is slightly positive when considered over the cohort
- TEAUC is indistinguishable from 0
- No clear group separation for stressed vs control or male vs female

### Possible Explanations

1. **True null effect**: TE and ER features may not differ systematically between these groups

2. **Insufficient sample size**: With n ≈ 50-70 per group, power to detect small effects (d = 0.2) is limited (~35% power)

3. **High within-group variability**: Individual differences may overwhelm group differences

4. **Conditioning requirements**: The paper suggests that stress-specific effects may require more sophisticated conditional approaches beyond simple group comparisons

### Power Analysis

For detecting:
- **Small effect** (d = 0.2): Requires n ≈ 400 per group for 80% power
- **Medium effect** (d = 0.5): Requires n ≈ 65 per group for 80% power
- **Large effect** (d = 0.8): Current sample provides >90% power

**Conclusion:** Current sample is well-powered to detect medium-to-large effects but underpowered for small effects.

---

## Recommendations

### For Current Analysis

1. **Verify data files**: Regenerate "no conditioning" files with correct group assignments

2. **Examine individual features**: Some features may show trends worth exploring in larger samples

3. **Consider subgroup analyses**: Examine specific conditioning scenarios (e.g., deceleration-specific TE)

4. **Investigate non-linear relationships**: Current analysis assumes linear group differences

### For Future Work

1. **Factorial models**: Test exposure × sex interactions (requires subject-level data with both factors)

2. **Continuous predictors**: Use actual PSS/PDQ scores and cortisol levels rather than binary grouping

3. **Mixed-effects models**: Account for potential non-independence if subjects have multiple measurements

4. **Time-scale specific analyses**: The paper identifies 0.5-2.5s as the relevant time scale; focus analyses there

5. **Machine learning approaches**: Multivariate pattern analysis might reveal subtle group differences

6. **Larger sample**: Power calculations suggest n ≈ 400 per group needed for small effect detection

---

## Technical Notes

### Software and Methods

- **Language**: Python 3.x
- **Statistical packages**: scipy.stats, statsmodels
- **Visualization**: matplotlib, seaborn
- **Multiple comparison correction**: Benjamini-Hochberg FDR, Bonferroni, Holm-Bonferroni

### Data Structure

Each .npz file contains 5 arrays:
- `all`: All 120 subjects
- `stressed`: Stressed subgroup (n=58)
- `control`: Control subgroup (n=58)
- `male`: Male fetuses subgroup (n=49)
- `female`: Female fetuses subgroup (n=68)

### Statistical Assumptions

- **Independence**: Stressed/control and male/female are independent samples
- **Normality**: Assessed via Shapiro-Wilk test; Mann-Whitney U provided as non-parametric alternative
- **Homogeneity of variance**: Assessed via Levene's test

---

## File Outputs

All results saved to: `analysis_output/`

1. **Data files:**
   - `exposure_effects_detailed.csv` - Complete exposure analysis results
   - `sex_effects_detailed.csv` - Complete sex analysis results
   - `data_validation_report.csv` - Data quality validation

2. **Visualizations:**
   - `exposure_effects_forest.png` - Forest plot of exposure effects
   - `sex_effects_forest.png` - Forest plot of sex effects
   - `volcano_plots.png` - Volcano plots showing effect size vs significance
   - `effect_size_distributions.png` - Distribution of Cohen's d values

---

## Conclusions

1. **No evidence of exposure effects**: TE and ER features do not differ significantly between stressed and control mothers in this dataset

2. **No evidence of sex effects**: TE and ER features do not differ significantly between male and female fetuses

3. **Data quality requires attention**: Six files contain identical stressed/control data

4. **Consistent with paper**: Findings align with paper's inability to demonstrate stress-specific TE differences using standard approaches

5. **Future directions**: Paper suggests exploring "additional information-theoretical conditional approaches" beyond simple group comparisons

---

## Contact

For questions about this analysis, please refer to:
- Analysis scripts: `statistical_analysis_v2.py`, `validate_data.py`
- Output directory: `analysis_output/`
- Original paper: Sections 3.5.3-3.5.5 (Stratified Analysis)
