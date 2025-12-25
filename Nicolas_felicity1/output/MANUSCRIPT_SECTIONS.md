# Manuscript Sections: Entropy-Based Biomarkers of Maternal-Fetal Heart Rate Dynamics

---

## 2. Methods

### 2.1 Study Population

This prospective cohort study enrolled pregnant women receiving prenatal care between [dates]. Inclusion criteria were singleton pregnancy, gestational age 32-40 weeks at enrollment, and absence of known fetal anomalies. The study was approved by [IRB], and all participants provided written informed consent.

Maternal stress exposure was assessed using the Perceived Stress Scale (PSS; Cohen et al., 1983) and the Prenatal Distress Questionnaire (PDQ; Yali & Lobel, 1999). Participants were classified as "stressed" (PSS ≥ 19) or "control" (PSS < 19) based on established cutoffs for elevated perceived stress. Maternal hair cortisol concentration (pg/mg) was measured as a physiological marker of chronic stress exposure.

### 2.2 Fetal and Maternal Heart Rate Acquisition

Simultaneous fetal and maternal heart rate (HR) recordings were obtained using [equipment/method]. Recordings of at least [duration] were required for inclusion. Signal quality was assessed, and segments with artifacts or signal dropout were excluded from analysis.

### 2.3 Entropy Feature Extraction

Three categories of entropy-based features were computed from the HR time series:

**Entropy Rate (ER):** Entropy rate quantifies the complexity or unpredictability of a time series, representing the rate at which new information is generated. Higher entropy rate indicates greater irregularity in HR dynamics. ER was computed separately for fetal and maternal HR signals using [specific algorithm/parameters].

**Sample Entropy (SE):** Sample entropy measures the regularity of a time series by quantifying the conditional probability that sequences similar for *m* points remain similar at *m+1* points. Lower SE indicates more regular, predictable patterns. SE was computed with embedding dimension m = [value] and tolerance r = [value] × SD.

**Transfer Entropy (TE):** Transfer entropy quantifies the directed information flow between two time series, measuring the extent to which knowledge of one signal reduces uncertainty about the future of another. TE was computed bidirectionally between maternal and fetal HR, with conditioning on either fetal HR (TE_fHR) or maternal HR (TE_mHR). Both maximum and mean TE values across the recording were extracted.

For each feature type, values were computed under five conditioning paradigms: (1) full recording, (2) fetal HR acceleration epochs, (3) fetal HR deceleration epochs, (4) maternal HR acceleration epochs, and (5) maternal HR deceleration epochs. This yielded 10 ER features, 10 SE features, and 12 TE features (32 total).

### 2.4 Neurodevelopmental Outcome Assessment

Infant neurodevelopmental outcomes were assessed at [age] months using the Bayley Scales of Infant and Toddler Development, Fourth Edition (Bayley-4). Composite scores were obtained for cognitive (COG), language (LANG), and motor (MOTOR) domains. Subscale scores for language (receptive, expressive) and motor (fine, gross) skills were also analyzed.

### 2.5 Statistical Analysis

#### 2.5.1 Normality Assessment and Correlation Methods

Distributional properties of all variables were assessed using the Shapiro-Wilk test (α = 0.05). Correlation method selection was data-driven: Pearson product-moment correlation was applied when both variables satisfied normality assumptions; Spearman rank correlation was used otherwise. This approach optimizes statistical power while maintaining validity across non-normal distributions.

#### 2.5.2 Univariate Correlation Analysis

Bivariate correlations were computed between each entropy feature and outcome variable. Given the exploratory nature of this analysis, no correction for multiple comparisons was applied; findings are interpreted as hypothesis-generating rather than confirmatory. Statistical significance was set at p < 0.05 (two-tailed).

#### 2.5.3 Stratified Analyses

To examine potential moderating effects, correlations were computed separately for: (1) stressed versus control groups based on PSS classification, and (2) male versus female fetuses based on sex determined at birth.

#### 2.5.4 Multivariate Modeling

Given the high-dimensional feature space (32 predictors) relative to sample size, multiple regularized regression approaches were employed:

- **Elastic Net Regression:** Combines L1 (lasso) and L2 (ridge) penalties to handle multicollinearity while performing feature selection. Hyperparameters (α, λ) were optimized via 5-fold cross-validation.

- **Principal Component Analysis + Ridge Regression:** PCA was applied to reduce dimensionality, retaining components explaining 90% of variance, followed by ridge regression.

- **Partial Least Squares (PLS) Regression:** PLS identifies latent components that maximize covariance between predictors and outcome, well-suited for multicollinear predictors.

- **Random Forest Regression:** Non-parametric ensemble method to capture potential non-linear relationships. Conservative hyperparameters (max_depth = 3, min_samples_leaf = 5) were used to prevent overfitting.

- **Parsimonious Forward Selection:** Forward stepwise selection with adjusted R² criterion, limited to maximum 3 predictors to maintain appropriate n/k ratios.

Model performance was evaluated using 5-fold cross-validated R² (CV-R²). Multicollinearity was assessed via Variance Inflation Factor (VIF), with VIF > 10 indicating severe multicollinearity.

All analyses were conducted in Python 3.x using scipy (v1.x), statsmodels (v0.x), and scikit-learn (v1.x). Statistical significance was set at p < 0.05 unless otherwise specified.

---

## 3. Results

### 3.1 Study Sample Characteristics

A total of 120 mother-fetus dyads with complete entropy feature data were included. The cohort was balanced for maternal stress exposure: 61 participants (50.8%) were classified as controls and 59 (49.2%) as stressed. Mean PSS score was 16.3 ± 7.6 (range: 0-32), and mean PDQ score was 12.5 ± 6.8 (range: 2-33). The sample included 60 male (50.0%) and 58 female (48.3%) fetuses, with sex data missing for 2 participants.

Neurodevelopmental follow-up data were available for a subset of participants: cognitive composite scores (n = 66, 55.0%), language composite scores (n = 63, 52.5%), and motor composite scores (n = 65, 54.2%). Hair cortisol data were available for 88-90 participants depending on the analysis.

### 3.2 Normality Assessment

Entropy rate features demonstrated predominantly normal distributions (9/10 features passing Shapiro-Wilk test), while sample entropy features showed more frequent deviations from normality (3/10 passing). Transfer entropy features showed mixed patterns, with epoch-specific features (acceleration/deceleration) more often normally distributed than "all points" features. Consequently, 70% of correlations employed Spearman rank correlation and 30% employed Pearson correlation.

### 3.3 Entropy Rate and Sample Entropy Correlations with Outcomes

Six statistically significant correlations (p < 0.05) were identified between ER/SE features and neurodevelopmental outcomes, representing 3.0% of all tested correlations (Table 1). Significant associations were observed exclusively in motor and language domains; no correlations reached significance for cognitive composite scores.

**Table 1. Significant correlations between entropy rate/sample entropy features and neurodevelopmental outcomes**

| Feature | Outcome | r | p | Method | n |
|---------|---------|---|---|--------|---|
| SE fetus (mHR accel) | Motor Fine Skills | -0.290 | 0.021 | Spearman | 63 |
| SE mother (mHR accel) | Motor Fine Skills | -0.286 | 0.023 | Spearman | 63 |
| SE fetus (fHR accel) | Language Receptive | +0.290 | 0.026 | Spearman | 59 |
| SE mother (fHR accel) | Language Receptive | +0.290 | 0.026 | Spearman | 59 |
| ER mother (fHR decel) | Motor Gross Skills | -0.363 | 0.030 | Pearson | 36 |
| ER mother (mHR accel) | Language Receptive | -0.263 | 0.046 | Pearson | 58 |

*SE = sample entropy; ER = entropy rate; mHR = maternal heart rate; fHR = fetal heart rate; accel = acceleration epochs; decel = deceleration epochs*

Sample entropy features computed during maternal HR acceleration epochs showed negative associations with motor fine skills, indicating that higher entropy (greater irregularity) in maternal-fetal HR coupling during maternal accelerations was associated with poorer fine motor development. Conversely, sample entropy during fetal HR accelerations showed positive associations with language receptive scores.

No significant correlations were observed between ER/SE features and maternal stress measures (PSS, PDQ) or cortisol (all p > 0.05).

### 3.4 Transfer Entropy Correlations with Outcomes

Seven statistically significant correlations (p < 0.05) were identified between TE features and maternal cortisol (Table 2). Notably, no significant correlations were observed between TE features and Bayley neurodevelopmental scores or psychological stress measures (PSS, PDQ).

**Table 2. Significant correlations between transfer entropy features and maternal cortisol**

| Feature | r | p | n |
|---------|---|---|---|
| Max TE (mHR conditioning, decel) | +0.315 | 0.003 | 88 |
| Max TE (mHR conditioning, accel) | +0.287 | 0.007 | 88 |
| Max TE (fHR conditioning, decel) | +0.271 | 0.011 | 88 |
| Max TE (fHR conditioning, accel) | +0.250 | 0.019 | 88 |
| Mean TE (mHR conditioning, accel) | +0.221 | 0.038 | 88 |
| Mean TE (mHR conditioning, decel) | +0.217 | 0.042 | 88 |
| Mean TE (fHR conditioning, accel) | +0.212 | 0.047 | 88 |

*All correlations computed using Spearman method. TE = transfer entropy; mHR = maternal heart rate; fHR = fetal heart rate*

All significant TE-cortisol correlations were positive, indicating that stronger directional coupling between maternal and fetal heart rates was associated with higher chronic stress as indexed by hair cortisol. Maximum TE values showed stronger associations (r = 0.25-0.31) than mean TE values (r = 0.21-0.22). TE computed during acceleration and deceleration epochs reached significance, while TE computed using all data points did not (all p > 0.10).

### 3.5 Stress-Stratified Analysis

Stratification by maternal stress status revealed qualitatively different correlation patterns between groups (Table 3).

**Table 3. Selected significant correlations by stress group**

| Group | Feature | Outcome | r | p | n |
|-------|---------|---------|---|---|---|
| **Control** | ER mother (fHR decel) | Motor Composite | -0.793 | 0.001 | 13 |
| | ER fetus (full) | Motor Fine Skills | +0.438 | 0.028 | 26 |
| | ER fetus (mHR accel) | Motor Fine Skills | +0.383 | 0.039 | 30 |
| **Stressed** | SE mother (full) | Cognitive Composite | +0.377 | 0.034 | 32 |
| | SE fetus (fHR accel) | PDQ | -0.263 | 0.045 | 59 |
| | SE mother (fHR accel) | PDQ | -0.261 | 0.046 | 59 |

In control participants, entropy rate features showed the predominant associations, with positive correlations between fetal ER and motor fine skills. In stressed participants, sample entropy features predominated, with higher maternal SE associated with better cognitive outcomes. The reversal of effect directions between groups for motor outcomes suggests that maternal stress may moderate the relationship between entropy features and neurodevelopment.

### 3.6 Sex-Stratified Analysis

Analysis by fetal sex revealed pronounced differences in TE-outcome associations (Table 4).

**Table 4. Transfer entropy correlations by fetal sex**

| Sex | Significant Correlations | Primary Outcomes |
|-----|--------------------------|------------------|
| Female (n = 58) | 9 | Cortisol, Cognitive, Motor |
| Male (n = 60) | 0 | None |

Female fetuses showed significant TE correlations with cortisol (consistent with unstratified findings) as well as cognitive outcomes not observed in the overall sample (e.g., max TE fHR accel vs. Cognitive Composite: r = -0.398, p = 0.024). Male fetuses showed no significant TE-outcome correlations.

### 3.7 Multivariate Analysis

#### 3.7.1 Multicollinearity Assessment

Variance Inflation Factor analysis revealed severe multicollinearity among entropy features. Across outcomes, 90-94% of features (30-31 of 33) showed VIF > 10. The highest VIF values were observed for TE "all points" features, which share substantial variance due to their mathematical relationships across conditioning types.

#### 3.7.2 Model Performance

Cross-validated R² values for multivariate models are presented in Table 5.

**Table 5. Cross-validated R² by model and outcome**

| Outcome | Elastic Net | PCA+Ridge | PLS | Random Forest |
|---------|-------------|-----------|-----|---------------|
| Cognitive Composite | -0.10 | -0.06 | -0.79 | -0.10 |
| Language Composite | -0.42 | -0.57 | -1.23 | -0.40 |
| Motor Composite | -0.49 | -0.52 | -0.99 | -0.43 |
| Motor Fine Skills | -0.23 | -0.01 | **+0.10** | -0.19 |

Negative CV-R² values indicate that models performed worse than a null model predicting the sample mean, reflecting overfitting due to the unfavorable ratio of predictors to observations (n/k ≈ 1.0; recommended >10-20). Only PLS regression for Motor Fine Skills achieved a marginally positive CV-R² of 0.10.

#### 3.7.3 Feature Selection

Parsimonious forward selection (maximum 3 features) identified TE features among top predictors for motor outcomes:

- **Motor Composite:** max TE fHR (all), max TE mHR (all), SE mother (fHR accel); adjusted R² = 0.082
- **Motor Fine Skills:** SE fetus (mHR accel), max TE fHR (all); adjusted R² = 0.007
- **Cognitive Composite:** mean TE mHR (all), SE mother (mHR accel); adjusted R² = 0.067
- **Language Composite:** SE mother (mHR decel); adjusted R² = 0.116, stress main effect β = -13.4, p = 0.051

PLS loadings revealed that TE features dominated the first latent component for Cognitive and Motor Fine Skills outcomes, while ER features dominated for Language and Motor Composite outcomes.

---

## 4. Discussion

### 4.1 Principal Findings

This study examined the relationship between entropy-based measures of maternal-fetal heart rate dynamics and clinical outcomes including maternal stress markers and infant neurodevelopmental scores. Three principal findings emerged.

First, transfer entropy and univariate entropy measures (ER, SE) showed distinct patterns of association with outcomes. TE correlated exclusively with maternal cortisol (7 significant associations, all positive), while ER/SE correlated with Bayley motor and language scores (6 significant associations) but not with cortisol. This dissociation suggests that bivariate (TE) and univariate (ER, SE) entropy measures capture different aspects of maternal-fetal physiology with distinct clinical relevance.

Second, the relationship between entropy features and neurodevelopmental outcomes was moderated by maternal stress status. In control participants, entropy rate features showed positive associations with motor outcomes; in stressed participants, sample entropy features predominated, and effect directions were reversed for motor development. This interaction suggests that the physiological significance of heart rate complexity may differ depending on the stress milieu.

Third, pronounced sex differences emerged in TE-outcome relationships. Female fetuses showed 9 significant TE correlations spanning cortisol, cognitive, and motor outcomes, while male fetuses showed none. This sexual dimorphism aligns with broader literature on sex-specific fetal programming and differential vulnerability to prenatal stress.

### 4.2 Transfer Entropy as a Marker of Stress Physiology

The consistent positive correlations between TE and maternal cortisol suggest that stronger maternal-fetal heart rate coupling reflects heightened stress-related autonomic synchronization. Several mechanisms may explain this relationship.

Maternal stress activates the hypothalamic-pituitary-adrenal axis, increasing cortisol secretion, which can cross the placental barrier and influence fetal physiology. Concurrent sympathetic activation in both mother and fetus may produce coupled heart rate responses, manifesting as elevated transfer entropy. Alternatively, chronic stress may alter placental function in ways that increase maternal-fetal physiological interdependence.

Notably, TE computed during acceleration and deceleration epochs showed significant cortisol correlations, while TE computed using all data points did not. This suggests that stress-related coupling is most apparent during transient autonomic events (accelerations and decelerations) rather than during baseline heart rate regulation. The epoch-specific nature of this relationship has implications for clinical monitoring protocols.

### 4.3 Univariate Entropy Measures and Neurodevelopment

Sample entropy during maternal HR acceleration epochs showed negative associations with motor fine skills, indicating that greater irregularity in maternal-fetal coupling during maternal accelerations predicted poorer motor development. This finding extends previous work linking reduced fetal heart rate variability complexity to adverse outcomes.

The stress-dependent reversal of ER-motor associations is noteworthy. In unstressed pregnancies, higher fetal entropy rate predicted better motor outcomes, consistent with the notion that healthy physiological systems exhibit complex, adaptive dynamics. In stressed pregnancies, this relationship was attenuated or reversed, possibly reflecting stress-induced alterations in the meaning of heart rate complexity for developmental outcomes.

### 4.4 Sex-Specific Effects

The finding that TE-outcome correlations were observed exclusively in female fetuses aligns with evidence for sex-specific fetal programming. Female fetuses may show greater physiological responsiveness to maternal state, resulting in stronger maternal-fetal coupling that correlates with both stress markers and developmental outcomes. Alternatively, male and female fetuses may employ different adaptive strategies, with coupling being more relevant to outcomes in females.

This sex difference has clinical implications, suggesting that markers of maternal-fetal coupling may have greater predictive utility for female pregnancies. However, given the exploratory nature of stratified analyses and reduced sample sizes, replication in larger cohorts is essential before clinical application.

### 4.5 Limitations of Multivariate Modeling

The multivariate analyses were severely constrained by the unfavorable ratio of predictors (32 features) to observations (n = 30-66 for outcomes). The recommended n/k ratio of 10-20 would require sample sizes of 320-640, far exceeding the current cohort. Consequently, all complex models showed negative cross-validated R², indicating overfitting.

This limitation underscores the importance of dimensionality reduction strategies for future research. Pre-specifying composite scores (e.g., PC1 from each feature type) would reduce the predictor set from 32 to 3, achieving adequate n/k ratios with current sample sizes. Alternatively, hypothesis-driven selection of specific features based on theoretical predictions would improve power.

### 4.6 Clinical Implications

The distinct associations of TE (with cortisol) and ER/SE (with neurodevelopment) suggest potential for a two-stage clinical assessment. TE could serve as a real-time marker of maternal stress physiology, identifying pregnancies with elevated cortisol without invasive sampling. ER/SE could provide complementary information about developmental risk, particularly when interpreted in the context of maternal stress status.

The finding that epoch-specific TE (during accelerations/decelerations) is more informative than continuous TE has practical implications for monitoring protocols. Brief assessment windows capturing transient heart rate events may suffice for stress biomarker purposes, reducing monitoring burden.

### 4.7 Limitations

Several limitations warrant consideration. First, neurodevelopmental outcome data were available for only approximately half of the cohort, introducing potential selection bias. Second, the cross-sectional design precludes causal inference; the observed associations may reflect confounding by unmeasured variables. Third, the exploratory analysis of 320+ correlations without multiple comparison correction increases the risk of false positives; findings should be considered hypothesis-generating. Fourth, small subgroup sizes in stratified analyses (n = 13-35 for some comparisons) limit statistical power and precision. Finally, the single-site design may limit generalizability.

### 4.8 Future Directions

Several lines of investigation are warranted. First, replication in larger, independent cohorts is essential to confirm the observed associations and effect sizes. Second, mediation analysis testing the pathway TE → Cortisol → Neurodevelopment would clarify whether TE influences development directly or indirectly through stress physiology. Third, longitudinal designs with repeated entropy measurements could determine whether changes in maternal-fetal coupling over gestation predict outcomes better than single timepoint assessments. Fourth, investigation of the mechanisms underlying sex-specific effects would advance understanding of fetal programming. Finally, development of composite entropy scores through dimensionality reduction would enable more powerful multivariate modeling.

### 4.9 Conclusions

Entropy-based measures of maternal-fetal heart rate dynamics show distinct patterns of association with clinical outcomes. Transfer entropy correlates with maternal cortisol, suggesting it captures stress-related physiological coupling, while entropy rate and sample entropy correlate with neurodevelopmental outcomes in a stress-dependent manner. Sex-specific effects and stress-group interactions indicate that the clinical utility of these biomarkers may depend on contextual factors. These findings support continued investigation of entropy measures as potential biomarkers in prenatal care, while highlighting the need for larger samples to enable robust multivariate inference.

---

## Supplementary Tables

### Table S1. Complete correlation matrix: Entropy Rate features vs. outcomes

| Feature | PSS | PDQ | Cortisol | COG | LANG | MOTOR |
|---------|-----|-----|----------|-----|------|-------|
| ER fetus (full) | ns | ns | ns | ns | ns | ns |
| ER mother (full) | ns | ns | ns | ns | ns | ns |
| ER fetus (fHR accel) | ns | ns | ns | ns | ns | ns |
| ER mother (fHR accel) | ns | ns | ns | ns | ns | ns |
| ER fetus (fHR decel) | ns | ns | ns | ns | ns | ns |
| ER mother (fHR decel) | ns | ns | ns | ns | ns | * |
| ER fetus (mHR accel) | ns | ns | ns | ns | ns | ns |
| ER mother (mHR accel) | ns | ns | ns | ns | * | ns |
| ER fetus (mHR decel) | ns | ns | ns | ns | ns | ns |
| ER mother (mHR decel) | ns | ns | ns | ns | ns | ns |

*ns = not significant; * p < 0.05*

### Table S2. Complete correlation matrix: Sample Entropy features vs. outcomes

| Feature | PSS | PDQ | Cortisol | COG | LANG | MOTOR Fine |
|---------|-----|-----|----------|-----|------|------------|
| SE fetus (full) | ns | ns | ns | ns | ns | ns |
| SE mother (full) | ns | ns | ns | ns | ns | ns |
| SE fetus (fHR accel) | ns | ns | ns | ns | * | ns |
| SE mother (fHR accel) | ns | ns | ns | ns | * | ns |
| SE fetus (fHR decel) | ns | ns | ns | ns | ns | ns |
| SE mother (fHR decel) | ns | ns | ns | ns | ns | ns |
| SE fetus (mHR accel) | ns | ns | ns | ns | ns | * |
| SE mother (mHR accel) | ns | ns | ns | ns | ns | * |
| SE fetus (mHR decel) | ns | ns | ns | ns | ns | ns |
| SE mother (mHR decel) | ns | ns | ns | ns | ns | ns |

### Table S3. Complete correlation matrix: Transfer Entropy features vs. cortisol

| Feature | r | p | Significance |
|---------|---|---|--------------|
| Max TE fHR (all) | +0.083 | 0.437 | ns |
| Max TE fHR (accel) | +0.250 | 0.019 | * |
| Max TE fHR (decel) | +0.271 | 0.011 | * |
| Max TE mHR (all) | +0.083 | 0.437 | ns |
| Max TE mHR (accel) | +0.287 | 0.007 | ** |
| Max TE mHR (decel) | +0.315 | 0.003 | ** |
| Mean TE fHR (all) | +0.057 | 0.594 | ns |
| Mean TE fHR (accel) | +0.212 | 0.047 | * |
| Mean TE fHR (decel) | +0.207 | 0.053 | ns |
| Mean TE mHR (all) | +0.057 | 0.594 | ns |
| Mean TE mHR (accel) | +0.221 | 0.038 | * |
| Mean TE mHR (decel) | +0.217 | 0.042 | * |

*ns = not significant; * p < 0.05; ** p < 0.01*

---

*Word count: ~3,200 (Methods: ~800; Results: ~1,200; Discussion: ~1,200)*
