# Sex-Stratified Correlation Analysis - Exploratory Findings Summary

**Files**:
- `correlation_heatmaps_sex_stratified.png` (2-panel: Male vs Female)
- `correlation_heatmaps_sex_stress_stratified.png` (4-panel: Sex × Stress interaction)

**Date**: December 19, 2025
**Purpose**: Visualize sex-specific and sex × stress interaction patterns in entropy-outcome correlations

---

## Figure Descriptions

### Two-Panel Sex-Stratified Heatmap
Shows correlation coefficients (r) between:
- **Features** (rows): 32 entropy measures (10 ER, 10 SE, 12 TE)
- **Outcomes** (columns): 10 clinical measures

**Two panels**:
1. **Male Fetuses** (n=49)
2. **Female Fetuses** (n=71)

### Four-Panel Sex × Stress Heatmap
Shows correlation coefficients with complete stratification:
1. **Male-Control** (n=30)
2. **Male-Stressed** (n=19)
3. **Female-Control** (n=32)
4. **Female-Stressed** (n=39)

**Color scale**: Blue = negative, Red = positive (-0.5 to +0.5)
**Significance markers**: * p<0.05, ** p<0.01, *** p<0.001 (uncorrected)

---

## Key Findings: Sex-Stratified Analysis

### Male Fetuses (n=49)

**1 significant correlation (p < 0.05, uncorrected):**
- ER fetus (mHR decel) × Motor Composite: r=+0.387, p=0.035

**Pattern**: Minimal associations in males across all entropy measures

---

### Female Fetuses (n=71)

**16 significant correlations (p < 0.05, uncorrected):**

**Entropy Rate → Motor Skills (4 correlations)**:
- ER fetus (fHR accel) × Motor Gross: r=-0.381, p=0.041
- ER fetus (fHR decel) × Motor Gross: r=-0.612, p=0.003 **
- ER fetus (mHR accel) × Motor Gross: r=-0.366, p=0.043
- ER fetus (mHR decel) × Motor Gross: r=-0.372, p=0.039

**Sample Entropy → Cognitive/Language (3 correlations)**:
- SE mother full × Cognitive: r=+0.436, p=0.011 *
- SE fetus (fHR accel) × Lang Receptive: r=+0.410, p=0.024 *
- SE mother (fHR accel) × Lang Receptive: r=+0.410, p=0.024 *

**Transfer Entropy → Cortisol/Cognitive (9 correlations)**:
- TE max (fHR all) × Cognitive: r=-0.410, p=0.018 *
- TE max (fHR accel) × Cortisol: r=+0.368, p=0.007 **
- TE max (fHR accel) × Cognitive: r=-0.401, p=0.023 *
- TE max (fHR decel) × Cortisol: r=+0.373, p=0.006 **
- TE max (mHR all) × Cognitive: r=-0.410, p=0.018 *
- TE max (mHR accel) × Cortisol: r=+0.351, p=0.009 **
- TE max (mHR decel) × Cortisol: r=+0.423, p=0.002 **
- TE mean (fHR all) × Cognitive: r=-0.377, p=0.031 *
- TE mean (mHR all) × Cognitive: r=-0.377, p=0.031 *

**Pattern**: Strong sex-specific maternal-fetal coupling in females only

---

## Key Findings: Sex × Stress Stratification

### Male-Control (n=30)

**16 significant correlations:**

**Entropy Rate → Motor Skills (8 correlations)**:
- ER fetus full × Motor Fine: r=+0.601, p=0.005 **
- ER fetus full × Motor Composite: r=+0.495, p=0.027 *
- ER fetus (fHR accel) × Motor Fine: r=+0.523, p=0.031 *
- ER fetus (fHR accel) × Motor Composite: r=+0.573, p=0.016 *
- ER fetus (mHR accel) × Motor Fine: r=+0.624, p=0.003 **
- ER fetus (mHR accel) × Motor Composite: r=+0.544, p=0.013 *
- ER fetus (mHR decel) × Motor Fine: r=+0.608, p=0.006 **
- ER fetus (mHR decel) × Motor Composite: r=+0.604, p=0.006 **

**Sample Entropy → Motor Skills (2 correlations)**:
- SE fetus full × Motor Fine: r=+0.724, p<0.001 ***
- SE fetus full × Motor Composite: r=+0.694, p<0.001 ***

**Transfer Entropy → PSS/Cognitive (6 correlations)**:
- TE mean (fHR all) × Cognitive: r=+0.479, p=0.033 *
- TE mean (fHR decel) × PSS: r=+0.445, p=0.014 *
- TE mean (mHR all) × Cognitive: r=+0.479, p=0.033 *
- TE mean (mHR accel) × PSS: r=+0.440, p=0.015 *
- TE mean (mHR decel) × PSS: r=+0.433, p=0.017 *
- ER mother (mHR decel) × PSS: r=-0.393, p=0.042 *

**Pattern**: Strong positive associations with motor skills; TE correlates with maternal stress

---

### Male-Stressed (n=19)

**7 significant correlations:**

**Transfer Entropy → PSS/Language (6 correlations)**:
- TE max (fHR all) × PSS: r=-0.494, p=0.032 *
- TE max (mHR all) × PSS: r=-0.494, p=0.032 *
- TE mean (fHR all) × Lang Receptive: r=-0.698, p=0.025 *
- TE mean (fHR all) × Lang Expressive: r=-0.650, p=0.042 *
- TE mean (mHR all) × Lang Receptive: r=-0.698, p=0.025 *
- TE mean (mHR all) × Lang Expressive: r=-0.650, p=0.042 *

**Sample Entropy → PSS (1 correlation)**:
- SE mother full × PSS: r=+0.586, p=0.008 **

**Pattern**: Negative TE-PSS associations (opposite of Male-Control); negative TE-language

---

### Female-Control (n=32)

**12 significant correlations:**

**Transfer Entropy → Cortisol (2 correlations)**:
- TE max (mHR accel) × Cortisol: r=+0.444, p=0.030 *
- TE max (mHR decel) × Cortisol: r=+0.547, p=0.006 **

**Transfer Entropy → Language (3 correlations)**:
- TE max (fHR accel) × Lang Receptive: r=-0.793, p=0.004 **
- TE max (fHR accel) × Lang Expressive: r=-0.677, p=0.022 *
- TE max (fHR accel) × Lang Composite: r=-0.864, p<0.001 ***

**Transfer Entropy → Motor Skills (2 correlations)**:
- TE max (fHR decel) × Motor Fine: r=+0.691, p=0.027 *
- TE max (mHR decel) × Motor Fine: r=+0.661, p=0.038 *

**Entropy Rate → Cognitive/PDQ (5 correlations)**:
- ER mother (fHR accel) × PDQ: r=+0.421, p=0.036 *
- ER fetus (mHR accel) × Cognitive: r=+0.638, p=0.026 *
- ER mother (mHR accel) × PDQ: r=+0.412, p=0.033 *
- ER fetus (mHR decel) × Cognitive: r=+0.648, p=0.023 *
- ER mother (mHR decel) × PDQ: r=+0.384, p=0.048 *

**Pattern**: Strong TE-Cortisol coupling; very strong negative TE-Language associations

---

### Female-Stressed (n=39)

**7 significant correlations:**

**Transfer Entropy → Cortisol/Cognitive (2 correlations)**:
- TE max (mHR decel) × Cortisol: r=+0.377, p=0.044 *
- TE max (mHR decel) × Cognitive: r=-0.453, p=0.045 *

**Sample Entropy → Cognitive/Language (3 correlations)**:
- SE mother full × Cognitive: r=+0.540, p=0.014 *
- SE fetus (mHR decel) × Lang Expressive: r=+0.517, p=0.028 *
- SE mother (mHR decel) × Lang Expressive: r=+0.505, p=0.033 *

**Entropy Rate → Cortisol/Motor (2 correlations)**:
- ER fetus (fHR decel) × Motor Gross: r=-0.594, p=0.032 *
- ER mother (fHR decel) × Cortisol: r=+0.547, p=0.023 *

**Pattern**: Weaker associations compared to Female-Control; shift from TE to SE/ER

---

## Critical Statistical Note

**⚠️ NONE of these correlations survived False Discovery Rate (FDR) correction (all q > 0.40)**

- Sex-stratified analysis: 17 total significant (1 male, 16 female)
- Sex × stress analysis: 42 total significant (16 M-C, 7 M-S, 12 F-C, 7 F-S)
- **All findings are exploratory and require independent replication**

---

## Interpretation

### Sex-Specific Maternal-Fetal Coupling (Exploratory)

| Sex | TE Correlations | Primary Pattern |
|-----|-----------------|-----------------|
| **Male** | 1 total (0 with cortisol in simple sex stratification) | Minimal maternal-fetal coupling |
| **Female** | 16 total (4 with cortisol, 5 with cognitive) | Strong TE-cortisol/cognitive coupling |

This tentative sex difference (if replicated) suggests:
- **Female fetuses**: Maternal-fetal coupling mechanisms operational; TE captures stress physiology
- **Male fetuses**: Different autonomic regulation or delayed coupling development

### Sex × Stress Interaction Patterns (Exploratory)

**Male-Control vs Male-Stressed:**
- **Control**: Positive TE-cognitive, positive TE-PSS (higher coupling → higher stress perception)
- **Stressed**: Negative TE-PSS, negative TE-language (reversal of association direction)
- **Motor associations**: Strong positive ER/SE-motor in control; absent in stressed

**Female-Control vs Female-Stressed:**
- **Control**: Strong TE-cortisol coupling (r=+0.55), very strong negative TE-language (r=-0.86)
- **Stressed**: Weaker TE-cortisol, shift to SE-cognitive associations
- **Pattern shift**: From TE-dominated to SE/ER-dominated in stressed group

### Developmental Pathway Dissociation by Sex (Exploratory)

| Group | ER/SE Pattern | TE Pattern | Interpretation |
|-------|---------------|------------|----------------|
| **Male-Control** | Strong positive → Motor | Positive → PSS/Cognitive | Complexity supports development; coupling reflects stress |
| **Male-Stressed** | Absent | Negative → PSS/Language | Stress disrupts normal pathways |
| **Female-Control** | Minimal | Strong → Cortisol, Negative → Language | Coupling dominates; language trade-off |
| **Female-Stressed** | Positive → Cognitive/Language | Weak → Cortisol | Shift from coupling to complexity |

### Sex-Differentiated Stress Adaptation (Exploratory)

**Males**: Stress appears to eliminate positive entropy-outcome associations
- Control: 16 significant correlations (strong ER/SE-motor, TE-PSS)
- Stressed: 7 significant (different features, negative TE-language)

**Females**: Stress shifts coupling mechanisms
- Control: TE-cortisol dominant (strong maternal-fetal coupling)
- Stressed: SE/ER-cognitive/language emerge (shift to signal complexity)

This tentative pattern (requiring replication) could indicate sex-specific autonomic adaptation strategies under maternal stress.

---

## Comparison with Overall and Stress-Stratified Results

### Transfer Entropy - Cortisol Associations

| Stratification | Significant TE-Cortisol | Strongest Effect |
|----------------|-------------------------|------------------|
| **All participants** | 7 (r=0.21-0.31) | max TE mHR decel: r=+0.32 |
| **Control** | 4 (r=0.35-0.42) | max TE mHR decel: r=+0.42 |
| **Stressed** | 0 | None |
| **Male** | 0 | None |
| **Female** | 4 (r=0.35-0.42) | max TE mHR decel: r=+0.42 |
| **Male-Control** | 0 | None |
| **Male-Stressed** | 0 | None |
| **Female-Control** | 2 (r=0.44-0.55) | max TE mHR decel: r=+0.55 |
| **Female-Stressed** | 1 (r=0.38) | max TE mHR decel: r=+0.38 |

**Critical finding**: TE-cortisol coupling is **female-specific**, strongest in **female-control** subgroup

### Transfer Entropy - Cognitive Associations

| Stratification | Significant TE-Cognitive | Direction |
|----------------|--------------------------|-----------|
| **All** | 0 | - |
| **Stressed** | 1 (r=-0.40) | Negative |
| **Male** | 0 | - |
| **Female** | 2 (r=-0.41) | Negative |
| **Male-Control** | 2 (r=+0.48) | **Positive** |
| **Male-Stressed** | 0 | - |
| **Female-Control** | 0 | - |
| **Female-Stressed** | 1 (r=-0.45) | Negative |

**Critical finding**: TE-cognitive association is **positive in Male-Control only**; negative in females and stressed males

---

## Sex Differences in Manuscript Context

The manuscript Section 3.3 reports exploratory sex-stratified findings:
- **Female fetuses**: 9 significant TE correlations (did not survive FDR)
- **Male fetuses**: 0 significant TE correlations

This comprehensive analysis extends those findings, revealing:
1. **Female-specific TE-cortisol coupling** (4 correlations in females, 0 in males)
2. **Male-specific motor associations** in control subgroup (absent in females)
3. **Opposite TE-cognitive directions** by sex-stress subgroup
4. **Stress-induced pathway shifts** differ by sex

---

## Usage in Manuscript

**Figure placement**: Supplementary Materials

**Caption (Two-Panel)**:
"Sex-stratified exploratory correlation analysis between entropy features and clinical outcomes. Heatmaps show correlation coefficients (r) for male fetuses (left, n=49) and female fetuses (right, n=71). Asterisks indicate uncorrected significance (* p<0.05, ** p<0.01, *** p<0.001). **CRITICAL**: None of these correlations survived FDR correction (all q > 0.40); findings are exploratory. Note striking sex difference: 16 significant correlations in females vs 1 in males, consistent with reported sex-specific TE-cortisol coupling."

**Caption (Four-Panel)**:
"Sex × Stress interaction in exploratory correlation analysis. Heatmaps show correlation coefficients (r) for four subgroups: Male-Control (n=30), Male-Stressed (n=19), Female-Control (n=32), Female-Stressed (n=39). Asterisks indicate uncorrected significance (* p<0.05, ** p<0.01, *** p<0.001). **CRITICAL**: None of these correlations survived FDR correction (all q > 0.40); findings are exploratory and hypothesis-generating only."

**Referenced in**:
- Results Section 3.2/3.3 (Sex-stratified exploratory correlations)
- Discussion Section 4.1 (Sex-specific maternal-fetal coupling mechanisms)
- Discussion Section 4.2 (Sex-differentiated stress adaptation pathways)

---

## Statistical Methods

**Correlation method selection**: Same as main analysis
- Shapiro-Wilk test for normality (α=0.05)
- Pearson if both variables normal, Spearman otherwise

**Sample sizes**:
- Male: n=49 total (30 control, 19 stressed)
- Female: n=71 total (32 control, 39 stressed)
- Outcome-specific n varies by data availability

**Multiple comparison correction**:
- Benjamini-Hochberg FDR applied to all sex-stratified tests
- None survived FDR correction (all q > 0.40)
- Results interpreted as exploratory only

---

## Robust vs Exploratory Findings

### Robust (MLM, survived within-model testing):
- **Sex × Stress × TE interaction**: β=-0.042, p=0.009 (MLM result)
- **Accel/decel asymmetry**: No sex effects (p=0.361)
- **Conditioned entropy**: No sex effects (p=0.177)

### Exploratory (Correlations, did NOT survive FDR):
- All sex-stratified correlations: 17 total (all q > 0.40)
- All sex × stress correlations: 42 total (all q > 0.40)
- Female-specific TE-cortisol: 4 correlations (all q > 0.40)
- Male-specific motor associations: 16 correlations (all q > 0.40)

**Bottom line**: Only MLM sex × stress interaction (Section 3.4) is statistically robust. All sex-stratified correlation patterns require replication in adequately powered studies.

---

**Analysis**: `generate_correlation_heatmaps_sex_stratified.py`, `generate_correlation_heatmaps_sex_stress.py`
**Data sources**: entropy_rate.txt, SampEn.txt, TE files, clinical outcomes
**Software**: Python 3.9, pandas 1.5.3, scipy 1.11.4, seaborn 0.12.2
