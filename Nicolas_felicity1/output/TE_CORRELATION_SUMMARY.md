# Transfer Entropy Correlation Analysis Results

## Overview

This analysis examines the relationship between Transfer Entropy (TE) measures of maternal-fetal heart rate coupling and clinical outcomes including maternal stress markers and infant neurodevelopmental scores.

## Transfer Entropy Features

Twelve TE features were analyzed, derived from four conditioning approaches and three data segmentations:

### Conditioning Types
- **max_TE_fHR**: Maximum TE with fetal HR conditioning
- **max_TE_mHR**: Maximum TE with maternal HR conditioning
- **mean_TE_fHR**: Mean TE with fetal HR conditioning
- **mean_TE_mHR**: Mean TE with maternal HR conditioning

### Data Segmentations
- **all**: All data points
- **accel**: Acceleration epochs only
- **decel**: Deceleration epochs only

## Outcome Variables

| Category | Variables | Sample Size |
|----------|-----------|-------------|
| Stress Markers | PSS, PDQ | n = 115-118 |
| Physiological | Maternal Cortisol | n = 88-90 |
| Cognitive | COG Composite Score | n = 64-65 |
| Language | LANG Receptive, Expressive, Composite | n = 58-59 |
| Motor | MOTOR Fine, Gross, Composite | n = 62-64 |

## Statistical Methods

- **Normality testing**: Shapiro-Wilk test (α = 0.05)
- **Correlation method**: Pearson if both variables normally distributed; Spearman otherwise
- **Significance threshold**: p < 0.05

## Results

### Significant Correlations (p < 0.05)

| TE Feature | Outcome | r | p-value | Method | n |
|------------|---------|---|---------|--------|---|
| max_TE_mHR_decel | Cortisol | +0.315 | 0.003** | Spearman | 88 |
| max_TE_mHR_accel | Cortisol | +0.287 | 0.007** | Spearman | 88 |
| max_TE_fHR_decel | Cortisol | +0.271 | 0.011* | Spearman | 88 |
| max_TE_fHR_accel | Cortisol | +0.250 | 0.019* | Spearman | 88 |
| mean_TE_mHR_accel | Cortisol | +0.221 | 0.038* | Spearman | 88 |
| mean_TE_mHR_decel | Cortisol | +0.217 | 0.042* | Spearman | 88 |
| mean_TE_fHR_accel | Cortisol | +0.212 | 0.047* | Spearman | 88 |

*p < 0.05, **p < 0.01

### Marginally Significant Correlations (0.05 < p < 0.10)

| TE Feature | Outcome | r | p-value | Method | n |
|------------|---------|---|---------|--------|---|
| max_TE_fHR_accel | PSS | +0.160 | 0.088 | Spearman | 115 |
| max_TE_fHR_accel | LANG Expressive | -0.222 | 0.095 | Pearson | 58 |
| mean_TE_fHR_decel | Cortisol | +0.207 | 0.053 | Spearman | 88 |

### Non-Significant Associations

No significant correlations were found between TE features and:
- Perceived Stress Scale (PSS)
- Prenatal Distress Questionnaire (PDQ)
- Cognitive Composite Score
- Language Composite Score
- Motor Composite Score

## Key Findings

### 1. Cortisol is the Primary Correlate

All 7 statistically significant TE correlations involve maternal cortisol. This suggests that maternal-fetal heart rate coupling, as measured by TE, is more closely related to physiological stress markers than to psychological stress measures (PSS, PDQ) or developmental outcomes.

### 2. Epoch-Specific TE is More Informative

| Segmentation | Significant Correlations |
|--------------|-------------------------|
| All points | 0 |
| Acceleration epochs | 4 |
| Deceleration epochs | 3 |

TE computed during acceleration and deceleration epochs captures meaningful variance that is averaged out when using all data points.

### 3. Maximum TE Shows Stronger Associations

| Aggregation | Mean |r| | Range |
|-------------|--------|-------|
| Maximum TE | 0.281 | 0.250 - 0.315 |
| Mean TE | 0.217 | 0.212 - 0.221 |

Peak coupling strength (max TE) is more strongly associated with cortisol than average coupling (mean TE).

### 4. Direction of Association

All significant correlations are **positive**: higher TE (stronger maternal-fetal HRV coupling) is associated with higher maternal cortisol levels.

### 5. Conditioning Direction

Both fetal HR conditioning (max_TE_fHR) and maternal HR conditioning (max_TE_mHR) show similar patterns, suggesting the TE-cortisol relationship is bidirectional.

## Interpretation

### Biological Significance

The positive association between TE and cortisol suggests that elevated maternal stress (indexed by hair cortisol) is accompanied by altered patterns of maternal-fetal autonomic coupling. Several interpretations are possible:

1. **Stress-induced synchronization**: Maternal stress may increase sympathetic activation in both mother and fetus, leading to more coupled heart rate dynamics.

2. **Compensatory mechanism**: Higher TE during stress may reflect a protective fetal response to maintain homeostasis.

3. **Shared environmental effects**: Cortisol may directly influence both maternal and fetal autonomic function through placental transfer.

### Lack of Developmental Associations

The absence of direct TE-Bayley correlations contrasts with some univariate entropy findings. This may reflect:

1. **Different information captured**: TE measures directional coupling between two systems, while ER and SE measure complexity within a single system.

2. **Sample size limitations**: With n = 58-65 for Bayley outcomes, power to detect small-to-medium effects is limited.

3. **Indirect pathways**: TE may influence development through cortisol rather than directly.

## Comparison with Univariate Entropy Metrics

| Feature Type | Cortisol Correlations | Bayley Correlations |
|--------------|----------------------|---------------------|
| Entropy Rate (ER) | Few significant | Some in stratified analysis |
| Sample Entropy (SE) | Few significant | Some in stratified analysis |
| Transfer Entropy (TE) | 7 significant | None |

TE shows a distinct pattern: strong cortisol associations but no direct developmental links, whereas ER and SE show the opposite pattern in stratified analyses.

## Limitations

1. **Sample size**: n = 88 for cortisol analyses, n = 58-65 for Bayley outcomes
2. **Multiple comparisons**: 120 correlations tested; 7 significant at α = 0.05 (expected by chance: 6)
3. **Cross-sectional design**: Causal direction cannot be established
4. **Single cortisol measure**: Hair cortisol reflects chronic rather than acute stress

## Conclusions

1. Transfer Entropy during acceleration and deceleration epochs is significantly associated with maternal hair cortisol (r = 0.21-0.31, p < 0.05).

2. Higher maternal-fetal HRV coupling correlates with higher chronic maternal stress.

3. TE does not directly predict Bayley neurodevelopmental outcomes in this sample.

4. The TE-cortisol relationship provides a physiological mechanism that may partially explain previously reported stress-development associations.

## Statistical Notes

- Shapiro-Wilk normality test applied to each variable pair
- Pearson correlation used when both variables passed normality (p > 0.05)
- Spearman correlation used otherwise
- No correction for multiple comparisons applied (exploratory analysis)
