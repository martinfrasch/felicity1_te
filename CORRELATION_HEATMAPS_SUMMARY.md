# Correlation Heatmap Figures - Exploratory Findings Summary

**File**: `correlation_heatmaps_exploratory.png`
**Date**: December 19, 2025
**Purpose**: Visualize all exploratory correlation findings (ER, SE, TE vs clinical outcomes)

---

## Figure Description

Three-panel heatmap showing correlation coefficients (r) between:
- **Features** (rows): 32 entropy measures
  - 10 Entropy Rate (ER) features
  - 10 Sample Entropy (SE) features
  - 12 Transfer Entropy (TE) features
- **Outcomes** (columns): 10 clinical measures
  - Maternal stress: Cortisol, PSS, PDQ
  - Neurodevelopment: Cognitive, Language (Receptive, Expressive, Composite), Motor (Fine, Gross, Composite)

**Three panels**:
1. **All Participants** (n=120)
2. **Control Group** (stress=0)
3. **Stressed Group** (stress=1)

**Color scale**: Blue = negative correlation, Red = positive correlation (-0.5 to +0.5)
**Significance markers**: * p<0.05, ** p<0.01, *** p<0.001 (uncorrected)

---

## Key Findings

### All Participants (n=120)

**13 significant correlations (p < 0.05, uncorrected):**

**Transfer Entropy → Cortisol (7 correlations)**:
- Max TE (mHR decel): r=+0.315, p=0.003 **
- Max TE (mHR accel): r=+0.287, p=0.007 **
- Max TE (fHR decel): r=+0.271, p=0.011 *
- Max TE (fHR accel): r=+0.250, p=0.019 *
- Mean TE (mHR accel): r=+0.221, p=0.038 *
- Mean TE (mHR decel): r=+0.217, p=0.042 *
- Mean TE (fHR accel): r=+0.212, p=0.047 *

**Pattern**: Higher maternal-fetal coupling (TE) → higher chronic stress (cortisol)

**Sample Entropy → Language/Motor (6 correlations)**:
- SE fetus (fHR accel) × Lang Receptive: r=+0.290, p=0.026 *
- SE mother (fHR accel) × Lang Receptive: r=+0.290, p=0.026 *
- SE fetus (mHR accel) × Motor Fine: r=-0.290, p=0.021 *
- SE mother (mHR accel) × Motor Fine: r=-0.286, p=0.023 *
- ER mother (fHR decel) × Motor Gross: r=-0.363, p=0.030 *
- ER mother (mHR accel) × Lang Receptive: r=-0.263, p=0.046 *

**Pattern**: Mixed positive/negative associations with neurodevelopment

---

### Control Group

**10 significant correlations (p < 0.05, uncorrected):**

**Transfer Entropy → Cortisol (4 correlations)**:
- Max TE (mHR decel): r=+0.423, p=0.003 **
- Max TE (mHR accel): r=+0.387, p=0.008 **
- Max TE (fHR decel): r=+0.348, p=0.018 *
- Max TE (fHR accel): r=+0.346, p=0.019 *

**Entropy Rate/Sample Entropy → Motor Skills (6 correlations)**:
- ER mother (fHR decel) × Motor Composite: r=-0.837, p<0.001 ***
- ER mother (fHR decel) × Motor Gross: r=-0.617, p=0.019 *
- ER fetus full × Motor Fine: r=+0.416, p=0.020 *
- SE fetus full × Motor Fine: r=+0.398, p=0.027 *
- ER fetus (mHR accel) × Motor Fine: r=+0.382, p=0.037 *
- ER fetus (mHR decel) × Motor Fine: r=+0.384, p=0.040 *

**Pattern**: Stronger effect sizes in control group, particularly for motor outcomes

---

### Stressed Group

**10 significant correlations (p < 0.05, uncorrected):**

**Distinct pattern from control group:**

**Transfer Entropy → Stress Measures (3 correlations)**:
- Max TE (fHR all) × PSS: r=-0.287, p=0.029 *
- Max TE (mHR all) × PSS: r=-0.287, p=0.029 *
- Max TE (fHR all) × Cognitive: r=-0.398, p=0.024 *

**Sample Entropy → Various Outcomes (7 correlations)**:
- SE mother full × Cognitive: r=+0.377, p=0.034 *
- SE fetus (fHR accel) × PDQ: r=-0.264, p=0.045 *
- SE mother (fHR accel) × PDQ: r=-0.264, p=0.045 *
- SE fetus (mHR accel) × Motor Fine: r=-0.381, p=0.032 *
- SE mother (mHR accel) × Motor Fine: r=-0.371, p=0.036 *

**Pattern**: Different correlation patterns compared to control group, suggesting stress moderation

---

## Critical Statistical Note

**⚠️ NONE of these correlations survived False Discovery Rate (FDR) correction (all q > 0.40)**

- 144 total correlation tests performed (32 features × 10 outcomes × 3 groups, with overlap)
- Expected false positives at α=0.05: ~7.2 correlations
- Observed significant correlations: 13 (All), 10 (Control), 10 (Stressed)
- **All findings are exploratory and require independent replication**

---

## Interpretation

### Pathway Dissociation (Exploratory)

| Feature Type | Primary Association | Tentative Interpretation |
|--------------|---------------------|--------------------------|
| **Transfer Entropy (TE)** | Maternal cortisol | Temporal coupling reflects stress physiology |
| **Entropy Rate/Sample Entropy (ER/SE)** | Bayley scores | Signal complexity relates to neurodevelopment |

This dissociation (if replicated) suggests:
- **TE → Stress pathway**: Directional coupling captures maternal stress state
- **ER/SE → Development pathway**: Signal complexity relates to autonomic maturation

### Stress Moderation (Exploratory)

**Effect direction reversal** between control and stressed groups:
- **Control**: ER/SE → Motor skills (stronger positive associations)
- **Stressed**: Different pattern, some negative associations

This tentative pattern (requiring replication) could indicate stress-related changes in neurodevelopmental pathways.

### Sex-Stratified Patterns (Not shown in main heatmap)

Manuscript Section 3.3 reports:
- **Female fetuses**: 9 significant TE correlations
- **Male fetuses**: 0 significant TE correlations
- Suggests potential sex-specific maternal-fetal coupling mechanisms (exploratory)

---

## Usage in Manuscript

**Figure placement**: Supplementary Materials

**Caption (Main Stress-Stratified Figure)**:
"Exploratory correlation analysis between entropy features and clinical outcomes. Heatmaps show correlation coefficients (r) for all participants (left), control group (center), and stressed group (right). Asterisks indicate uncorrected significance (* p<0.05, ** p<0.01, *** p<0.001). **CRITICAL**: None of these correlations survived False Discovery Rate correction (all q > 0.40); all findings are exploratory and hypothesis-generating only."

**Related Figures**:
- **Supplementary Figure S1**: Sex-stratified analysis (Male vs Female) - see `SEX_STRATIFIED_CORRELATION_SUMMARY.md` and `MANUSCRIPT_FIGURE_CAPTIONS.md`
- **Supplementary Figure S2**: Sex × Stress stratified analysis (4 panels) - see `SEX_STRATIFIED_CORRELATION_SUMMARY.md` and `MANUSCRIPT_FIGURE_CAPTIONS.md`

**Referenced in**:
- Results Section 3.2 (ER/SE exploratory correlations)
- Results Section 3.3 (TE exploratory correlations)
- Discussion Section 4.1 (Exploratory findings)
- Supplementary Results: Sex-stratified patterns (cross-reference with Figures S1, S2)

---

## Statistical Methods

**Correlation method selection**:
- Shapiro-Wilk test for normality (α=0.05)
- Pearson if both variables normal
- Spearman otherwise

**Sample sizes**:
- Cortisol: n=88-90
- Bayley scores: n=30-66 (varies by outcome)
- Stress groups: Control n=62, Stressed n=58

**Multiple comparison correction**:
- Benjamini-Hochberg FDR procedure applied
- None of 144 tests survived FDR (all q > 0.40)
- Results interpreted as exploratory only

---

## Comparison with Robust Findings

### Robust (MLM, survived within-model testing):
- **Accel/decel asymmetry**: β=-0.061, p<0.001
- **Conditioned entropy coupling**: β=-0.123, p=0.012 (60% reduction)
- **TE stress effects**: β=+0.023, p=0.026
- **TE sex-stress interaction**: β=-0.042, p=0.009

### Exploratory (Correlations, did NOT survive FDR):
- All TE-cortisol correlations: r=0.21-0.31, q>0.40
- All ER/SE-Bayley correlations: r=0.26-0.29, q>0.40
- All stratified correlations shown in heatmap

**Bottom line**: Only MLM findings (Sections 3.4-3.7) should be interpreted as established. All correlation findings require replication in adequately powered studies.

---

**Analysis**: `generate_correlation_heatmaps.py`
**Data sources**: entropy_rate.txt, SampEn.txt, TE files, clinical outcomes
**Software**: Python 3.9, pandas 1.5.3, scipy 1.11.4, seaborn 0.12.2
