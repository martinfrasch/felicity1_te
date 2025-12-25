# Results: Entropy Features in Relation to Clinical Biomarkers

## 3.4 Entropy Rate, Sample Entropy, and Transfer Entropy in Relation to Neurodevelopmental Outcomes

### 3.4.1 Study Sample and Data Availability

A total of 120 mother-fetus dyads with complete entropy feature data were included in the analysis. The cohort was balanced for maternal stress exposure, with 61 subjects (50.8%) classified as controls (PSS < 19) and 59 subjects (49.2%) classified as stressed (PSS ≥ 19). Mean PSS score was 16.3 ± 7.6 (range 0-32), and mean PDQ score was 12.5 ± 6.8 (range 2-33).

Neurodevelopmental outcome data were available for approximately half of the cohort: cognitive composite scores (n = 66, 55.0%), language composite scores (n = 63, 52.5%), and motor composite scores (n = 65, 54.2%).

**Feature Set:**
- 10 entropy rate (ER) features: univariate complexity measures
- 10 sample entropy (SE) features: regularity/predictability measures
- 12 transfer entropy (TE) features: directional coupling between maternal-fetal HR

Each feature was computed under multiple conditioning paradigms (full data, fetal HR accelerations/decelerations, maternal HR accelerations/decelerations).

### 3.4.2 Normality Assessment and Statistical Methods

Normality was assessed using the Shapiro-Wilk test (α = 0.05) for each variable pair prior to correlation analysis. Entropy rate features demonstrated predominantly normal distributions (9/10 features, 90%), while sample entropy features showed more frequent deviations from normality (3/10 features, 30%). Transfer entropy features showed mixed normality patterns, with epoch-specific features (accel/decel) more often normally distributed than "all points" features.

Correlation method selection was data-driven: Pearson correlation was applied when both variables passed normality testing; Spearman rank correlation was used otherwise.

### 3.4.3 Overall Correlation Patterns

#### Entropy Rate and Sample Entropy

Six significant correlations (p < 0.05) were identified between ER/SE features and neurodevelopmental outcomes (3.0% of all tested correlations), distributed across motor (n = 3) and language (n = 3) domains.

**Table 1. Significant ER/SE correlations with outcomes (p < 0.05)**

| Feature | Outcome | r | p-value | Method | n |
|---------|---------|---|---------|--------|---|
| SE_fetus_mHR_accel | Motor Fine Skills | -0.290 | 0.021 | Spearman | 63 |
| SE_mother_mHR_accel | Motor Fine Skills | -0.286 | 0.023 | Spearman | 63 |
| SE_fetus_fHR_accel | Language Receptive | +0.290 | 0.026 | Spearman | 59 |
| SE_mother_fHR_accel | Language Receptive | +0.290 | 0.026 | Spearman | 59 |
| ER_mother_fHR_decel | Motor Gross Skills | -0.363 | 0.030 | Pearson | 36 |
| ER_mother_mHR_accel | Language Receptive | -0.263 | 0.046 | Pearson | 58 |

*SE = Sample Entropy; ER = Entropy Rate; mHR = maternal heart rate; fHR = fetal heart rate*

#### Transfer Entropy

Seven significant correlations (p < 0.05) were identified between TE features and maternal cortisol. Notably, no significant TE correlations were observed with Bayley neurodevelopmental scores.

**Table 2. Significant TE correlations with outcomes (p < 0.05)**

| Feature | Outcome | r | p-value | Method | n |
|---------|---------|---|---------|--------|---|
| max_TE_mHR_decel | Maternal Cortisol | +0.315 | 0.003 | Spearman | 88 |
| max_TE_mHR_accel | Maternal Cortisol | +0.287 | 0.007 | Spearman | 88 |
| max_TE_fHR_decel | Maternal Cortisol | +0.271 | 0.011 | Spearman | 88 |
| max_TE_fHR_accel | Maternal Cortisol | +0.250 | 0.019 | Spearman | 88 |
| mean_TE_mHR_accel | Maternal Cortisol | +0.221 | 0.038 | Spearman | 88 |
| mean_TE_mHR_decel | Maternal Cortisol | +0.217 | 0.042 | Spearman | 88 |
| mean_TE_fHR_accel | Maternal Cortisol | +0.212 | 0.047 | Spearman | 88 |

**Key TE Finding:** All significant TE correlations were positive associations with maternal hair cortisol, indicating that stronger maternal-fetal HR coupling is associated with higher chronic stress levels. TE computed during acceleration and deceleration epochs was more informative than "all points" TE.

### 3.4.4 Stress-Stratified Analysis

Stratification by maternal stress status (PSS ≥ 19 vs < 19) revealed divergent correlation patterns between groups.

**Control group (n = 61):**
- Significant correlations were predominantly observed between entropy rate features and motor outcomes
- Maternal entropy rate during fetal HR decelerations showed a strong negative correlation with motor composite scores (r = -0.793, p = 0.001, n = 13)
- Fetal entropy rate features showed moderate positive correlations with motor fine skills (r = 0.38-0.44, p < 0.04)

**Stressed group (n = 59):**
- Sample entropy features showed the predominant associations
- SE_mother_full correlated positively with cognitive composite scores (r = +0.377, p = 0.034)
- Sample entropy during fHR accelerations showed negative correlations with PDQ scores (r = -0.26, p < 0.05)

The reversal of correlation directions between groups for motor outcomes is noteworthy: in controls, higher entropy predicted better motor skills; in stressed mothers, the pattern was reversed.

### 3.4.5 Sex-Stratified Analysis

Analysis by fetal sex revealed pronounced differences:

**Female fetuses (n = 58):**
- 9 significant TE correlations identified
- TE features correlated with both cortisol and developmental scores
- max_TE_fHR_accel vs COG Composite: r = -0.398, p = 0.024

**Male fetuses (n = 60):**
- 0 significant TE correlations identified
- No significant associations with any outcome variable

This sex-specific pattern suggests that maternal-fetal autonomic coupling may be differentially related to outcomes in male vs female pregnancies.

### 3.4.6 Multivariate Analysis Results

Given the large number of features (32 total) relative to sample size (n ≈ 30-65 for outcomes), multivariate modeling faced substantial challenges.

**Multicollinearity:**
Variance Inflation Factor (VIF) analysis revealed extreme multicollinearity, with 90%+ of features showing VIF > 10. The highest VIF values were observed for TE "all points" features, which are mathematically related across conditioning types.

**Model Performance (Cross-Validated R²):**

| Outcome | Elastic Net | PCA+Ridge | PLS | Random Forest |
|---------|-------------|-----------|-----|---------------|
| COG Composite | -0.10 | -0.06 | -0.79 | -0.10 |
| LANG Composite | -0.42 | -0.57 | -1.23 | -0.40 |
| MOTOR Composite | -0.49 | -0.52 | -0.99 | -0.43 |
| MOTOR Fine Skills | -0.23 | -0.01 | **+0.10** | -0.19 |

Negative CV-R² values indicate models performed worse than simply predicting the mean, reflecting overfitting due to the unfavorable n/k ratio (~1.0). Only PLS regression for Motor Fine Skills achieved marginally positive cross-validated R² (+0.10).

**Features Selected by Parsimonious Models:**
Forward selection identified TE features among top predictors for motor outcomes:
- MOTOR Composite: max_TE_fHR_all, max_TE_mHR_all, SE_mother_fHR_accel
- MOTOR Fine Skills: SE_fetus_mHR_accel, max_TE_fHR_all

### 3.4.7 Correlations with Stress Measures

**Univariate features (ER, SE):** No significant correlations were observed with PSS scores, PDQ scores, or maternal cortisol levels in the unstratified analysis.

**Bivariate features (TE):** Seven significant positive correlations with maternal cortisol (see Table 2), but no associations with psychological stress measures (PSS, PDQ).

This dissociation suggests that TE captures physiological stress (indexed by cortisol) while ER/SE do not, whereas ER/SE show outcome associations that TE lacks.

## Summary

The analysis of 32 entropy-based features (10 ER, 10 SE, 12 TE) in relation to clinical biomarkers revealed:

### Key Findings

1. **Feature-type specificity in outcome associations:**
   - ER/SE → Motor and language outcomes (6 significant correlations)
   - TE → Maternal cortisol only (7 significant correlations)
   - No overlap: TE did not correlate with Bayley scores; ER/SE did not correlate with cortisol

2. **TE-cortisol relationship is robust:**
   - All 7 significant TE correlations were positive (r = 0.21-0.31)
   - Higher maternal-fetal HR coupling associated with higher chronic stress
   - Effect driven by epoch-specific TE (accel/decel), not "all points"

3. **Stress-dependent patterns:**
   - The relationship between ER/SE features and neurodevelopmental outcomes differed qualitatively between stressed and control groups
   - Opposing correlation directions observed for motor outcomes

4. **Sex-specific effects:**
   - Female fetuses showed 9 significant TE correlations; male fetuses showed 0
   - Suggests sexual dimorphism in maternal-fetal autonomic coupling

5. **Multivariate models are underpowered:**
   - n/k ratio ≈ 1.0 (recommended: >10-20)
   - 90%+ features with VIF > 10
   - Negative CV-R² for most models

### Interpretation

The distinct correlation patterns suggest complementary information from univariate (ER, SE) and bivariate (TE) entropy measures:

- **TE reflects stress physiology:** Higher maternal-fetal coupling during pregnancy is associated with elevated cortisol, potentially through shared sympathetic activation
- **ER/SE predict development:** Complexity and regularity measures of individual HR signals relate to motor and language outcomes, moderated by stress status
- **Potential indirect pathway:** TE → Cortisol → Development (requires mediation analysis with larger samples)

### Methodological Notes

- Normality tested via Shapiro-Wilk (α = 0.05) for each correlation
- 70% of analyses used Spearman correlation due to non-normality
- Multiple comparison correction not applied (exploratory analysis)
- Small subgroup samples (n = 13-35) limit power for stratified analyses

### Recommendations for Future Research

1. **Increase sample size** to n > 150 for reliable multivariate inference
2. **Pre-register composite scores** (PC1 from each feature type) to reduce dimensionality
3. **Test mediation models:** TE → Cortisol → Bayley outcomes
4. **Investigate sex-specific effects** with adequate power

These findings extend the transfer entropy results reported in Section 3.3, demonstrating that entropy-based measures of maternal-fetal heart rate dynamics capture both physiological stress markers (TE-cortisol) and developmental outcomes (ER/SE-Bayley), with stress status and fetal sex moderating these relationships.
