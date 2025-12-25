# Figure Captions and Legends

**Manuscript**: Maternal-Fetal Heart Rate Coupling and Prenatal Stress
**Date**: December 17, 2025

---

## Figure 1: Sex-Specific Differences in Fetal Autonomic Complexity During Maternal Heart Rate Events

**Caption**:

**Mixed linear model results showing sex effects in univariate complexity metrics during maternal heart rate conditioning.** **(A)** Entropy rate shows male fetuses (blue) have significantly lower values than female fetuses (pink) during maternal HR events (β=-0.26, SE=0.11, p=0.024). **(B)** Sample entropy demonstrates concordant pattern with males showing lower complexity (β=-0.018, SE=0.008, p=0.030). Both panels show estimated marginal means with 95% confidence intervals (error bars). Sex effects emerge specifically during maternal HR accelerations and decelerations (n=444 observations for ER, n=476 for SE, from 119 patients). Statistical significance indicated by asterisks: *p<0.05. Male fetuses exhibit reduced autonomic complexity during maternal physiological events, suggesting sex-specific patterns of maternal-fetal coordination.

**Legend**:

- **Pink bars**: Female fetuses (reference group)
- **Blue bars**: Male fetuses
- **Error bars**: 95% confidence intervals calculated from mixed linear model standard errors (±1.96 × SE)
- **Sample sizes**: n=119 patients (49 male, 70 female) with repeated measurements during maternal HR events
- **Model specification**: `Value ~ Sex × Stress × HR_Source × HR_Event + (1|Patient_ID)`, REML estimation
- **Asterisk (*p<0.05)**: Indicates statistically significant sex main effect from mixed linear model
- **Units**: Entropy rate (bits/s), Sample entropy (dimensionless)
- **Context**: Values represent autonomic complexity during maternal HR accelerations and decelerations combined

**Statistical Note**: Effects shown are from separate mixed linear models for each metric, focusing on maternal HR conditioning context where sex effects were significant. No sex effects were detected in unconditioned data or during fetal HR events alone.

---

## Figure 2: Sex × Stress Interaction in Maternal-Fetal Transfer Entropy

**Caption**:

**Sex differences in maternal-fetal coupling strength are stress-dependent.** Net transfer entropy (maternal→fetal minus fetal→maternal) shows a significant Sex × Stress interaction (β=-0.042, SE=0.016, p=0.009). In control pregnancies (left two bars), male fetuses exhibit higher coupling than females (difference = +0.018). In stressed pregnancies (right two bars), this sex difference attenuates or reverses (males: 0.061, females: 0.085; difference = -0.024). Bars represent estimated marginal means from mixed linear model with 95% confidence intervals (error bars). The crossing pattern demonstrates that sex differences in maternal-fetal physiological coupling are not constitutive but rather modulated by maternal stress state. N=119 patients (60 control, 59 stressed; 49 male, 70 female) with 1,404 total observations across conditioning types. Statistical significance: **p=0.009 for Sex × Stress interaction term in unified mixed linear model.

**Legend**:

- **Pink bars**: Female fetuses
- **Blue bars**: Male fetuses
- **Light shading**: Control group (no maternal stress)
- **Dark shading**: Stressed group (elevated PSS/STAI scores)
- **Error bars**: 95% confidence intervals (±1.96 × SE from mixed linear model)
- **Asterisks**: **p=0.009 for interaction effect (indicates sex differences depend on stress state)
- **Units**: Net transfer entropy (bits), calculated as TE(maternal→fetal) - TE(fetal→maternal)
- **Model specification**: `TE_value ~ Sex × Stress × TE_Type × Conditioning × HR_Event + (1|Patient_ID)`, REML estimation
- **N**: 1,404 observations from 119 patients across multiple conditioning contexts

**Biological Interpretation**: The interaction pattern suggests male and female fetuses respond differently to maternal stress in terms of maternal-fetal coupling strength. Under control conditions, males show higher coupling (potentially reflecting delayed autonomic development). Under maternal stress, this sex difference disappears, suggesting stress-induced adaptation that is sex-specific.

**Statistical Note**: This interaction effect is impossible to detect using conventional t-test approaches and represents a key advantage of the mixed linear modeling framework.

---

## Figure 3: Comparative Sensitivity of Information-Theoretic Metrics to Sex and Stress Effects

**Caption**:

**Univariate and bivariate information metrics capture distinct physiological processes with differential sensitivity to sex and stress.** **(A) Effect Type Detection**: Entropy rate (ER) and sample entropy (SE) detect sex main effects (green checkmarks) but not stress effects or interactions (red X's), while transfer entropy (TE) detects stress main effect and Sex × Stress interaction but not simple sex main effect. **(B) Context Specificity**: ER and SE sex effects emerge only during maternal HR (mHR) conditioning events, not in unconditioned data or fetal HR events. TE shows stress sensitivity across all contexts. **(C) Effect Sizes**: Standardized effect sizes (Cohen's d) for significant findings show moderate effects for ER sex difference (d=0.52), smaller effects for SE (d=0.31), and small but significant effects for TE stress modulation (d=0.28) and interaction (d=0.34). **(D) Summary**: Univariate metrics reflect fetal autonomic complexity with sex-specific development patterns, while bivariate metric reflects maternal-fetal communication dynamics modulated by maternal stress. This metric complementarity reveals that fetal complexity and maternal-fetal coupling are partially independent physiological processes.

**Legend**:

### Panel A: Effect Type Detection
- **Green checkmarks (✓)**: Statistically significant effect (p<0.05)
- **Red X's (✗)**: Non-significant effect
- **ER/SE (Univariate)**: Measure individual time series complexity
- **TE (Bivariate)**: Measure directional information transfer between systems

### Panel B: Context Specificity
- **Bar heights**: Indicate presence/strength of effect in each context
- **mHR conditioning**: Analysis during maternal heart rate accelerations/decelerations
- **fHR events**: Analysis during fetal heart rate accelerations
- **Unconditioned**: Baseline analysis without event conditioning
- **Blue bars**: ER, **Orange bars**: SE, **Green bars**: TE

### Panel C: Effect Sizes
- **Cohen's d**: Standardized effect size (mean difference / pooled SD)
- **Interpretation**: Small (0.2), Medium (0.5), Large (0.8)
- **Error bars**: 95% confidence intervals on effect size estimates
- **Comparison**: All three metrics show small to moderate effect sizes

### Panel D: Physiological Interpretation Summary
- **Graphic symbols**: Represent different physiological processes measured
- **Key insight**: Different metrics are sensitive to different biological phenomena

**Statistical Note**: All effects shown are from mixed linear models with random intercepts per patient. ER and SE were analyzed using separate models by conditioning type to avoid singular matrix issues from sparse data. TE was analyzed using a unified model across all conditions (n=1,404 observations).

**Sample Sizes**:
- **ER no conditioning**: n=238 observations (119 patients × 2 HR sources)
- **ER mHR conditioning**: n=444 observations
- **ER fHR accel**: n=208 observations
- **SE no conditioning**: n=238 observations
- **SE mHR conditioning**: n=476 observations
- **SE fHR accel**: n=238 observations
- **TE unified model**: n=1,404 observations (119 patients, multiple conditions)

**Conclusion**: The complementary sensitivities of these metrics support a model where fetal autonomic development (captured by ER/SE) and maternal-fetal coupling dynamics (captured by TE) are distinct but interacting physiological processes. Sex influences developmental complexity, stress modulates coupling strength, and their interaction reveals stress-dependent sex differences in maternal-fetal communication.

---

## General Figure Formatting Notes

### Typography
- **Font**: Arial or Helvetica, 8-10pt for labels, 6-8pt for axis labels
- **Line weights**: 1.5pt for bars, 1.0pt for error bars, 0.5pt for grid lines
- **Symbol sizes**: Large enough to be visible at reduced size (journal column width ~3.5")

### Color Scheme
- **Female**: Pink (#FF69B4 or similar) - consistent across all figures
- **Male**: Blue (#4169E1 or similar) - consistent across all figures
- **Control**: Light shading or solid fill
- **Stressed**: Dark shading or hatching
- **Accessibility**: Color scheme is colorblind-friendly (pink/blue distinguishable in grayscale)

### Statistical Annotations
- **Significance levels**:
  - *p<0.05
  - **p<0.01
  - ***p<0.001
- **Effect sizes**: Reported as β (regression coefficient) with SE and p-value
- **Confidence intervals**: Always 95% unless otherwise stated

### File Formats
- **PNG**: 300 DPI minimum for publication
- **PDF**: Vector format for scalability
- **Both formats provided** for each figure

### Accessibility
- **Alt text** should be provided for digital versions
- **Color descriptions** included in legends for colorblind accessibility
- **Pattern/shading** used in addition to color where possible

---

## Supplementary Figure Suggestions

### Supplementary Figure S1: Model Diagnostics
**Suggested content**:
- Residual plots for each MLM model
- Q-Q plots for normality assessment
- Random effects distributions
- Influence diagnostics

**Purpose**: Demonstrate model assumptions are met and results are robust

### Supplementary Figure S2: Complete Breakdown by Conditioning Type
**Suggested content**:
- Separate panels for each conditioning context
- All metrics shown side-by-side
- Sex and stress breakdowns within each context

**Purpose**: Show full detail of context-specific effects

### Supplementary Figure S3: Individual Patient Trajectories
**Suggested content**:
- Random sample of 20 patients
- Individual TE values across conditions
- Group means overlaid
- Illustrate within-subject variability

**Purpose**: Show that group effects are consistent at individual level

### Supplementary Figure S4: Time-Scale Analysis
**Suggested content**:
- Entropy rate across different time scales
- Sex and stress effects at each scale
- Scale-dependent patterns

**Purpose**: Show whether effects are scale-specific or general

### Supplementary Figure S5: Correlation Matrix
**Suggested content**:
- Correlation heatmap of all 32 features
- Clustered by metric type (ER, SE, TE)
- Shows inter-metric relationships

**Purpose**: Demonstrate metrics capture related but distinct information

---

## Table Captions (For Reference)

### Table 1: Mixed Linear Model Results - Univariate Complexity Metrics

**Caption**:
Sex effects in entropy rate (ER) and sample entropy (SE) during maternal heart rate conditioning. Both metrics show significant sex main effects with male fetuses exhibiting lower complexity than females. Models include Sex × Stress × HR_Source × HR_Event interaction terms with patient random intercepts (REML estimation). Significant effects (p<0.05) are highlighted in bold. N=119 patients (49 male, 70 female) with 444 observations for ER and 476 for SE during maternal HR events.

### Table 2: Mixed Linear Model Results - Transfer Entropy

**Caption**:
Maternal-fetal coupling measured by transfer entropy shows significant Sex × Stress interaction (β=-0.042, p=0.009) and stress main effect (β=+0.023, p=0.026). Model includes full factorial interactions: Sex × Stress × TE_Type × Conditioning × HR_Event with patient random intercepts (REML estimation). The interaction indicates sex differences in coupling strength are stress-dependent rather than constitutive. N=119 patients (60 control, 59 stressed; 49 male, 70 female) with 1,404 total observations across all conditioning types.

### Table 3: Comparative Summary - All Metrics

**Caption**:
Summary comparison of mixed linear model results across all three information-theoretic metrics. Checkmarks (✓) indicate statistically significant effects (p<0.05). Entropy rate and sample entropy detect sex differences in fetal autonomic complexity specifically during maternal HR events. Transfer entropy uniquely detects stress modulation of maternal-fetal coupling and Sex × Stress interaction. This differential sensitivity supports the interpretation that univariate complexity (ER, SE) and bivariate coupling (TE) reflect distinct physiological processes.

---

## Usage Guidelines

### For Manuscript Submission
1. **Main text figures**: Figures 1-3 with full captions as written above
2. **Table placement**: Tables 1-3 should appear after first mention in Results
3. **Figure references**: Cite as "Figure 1A" for subpanels, "Figure 1" for whole figure
4. **Supplementary materials**: If journal permits, include suggested supplementary figures

### For Presentations
- **Simplified captions**: Remove statistical details, keep main message
- **One concept per slide**: Split Figure 3 into 4 slides if presenting
- **Larger fonts**: Increase all text sizes by 2-4 points
- **Animation**: Consider building panels sequentially for clarity

### For Grant Applications
- **Preliminary data**: These figures demonstrate feasibility and effect sizes
- **Power analysis**: Use effect sizes from Figure 3C for sample size calculations
- **Impact**: Emphasize novel Sex × Stress interaction (Figure 2)

### For Press/Public Communication
- **Simplified language**: Replace technical terms in captions
- **Key message**: "Baby's sex matters for how stress affects mother-baby connection"
- **Visual simplification**: Show only Figure 2 (most impactful finding)

---

**END OF FIGURE CAPTIONS**
