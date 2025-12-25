# Mixed Linear Model Analysis Summary
## Figures 3, 4, 6, 7 - Matching TE/ER/SE Methodology

**Date**: December 18, 2025  
**Analysis Type**: Mixed Linear Models with REML estimation  
**Sample**: n=120 patients (49 male, 71 female; 58 stressed, 62 control)

---

## Why MLM vs T-tests?

### Methodological Advantages

**Previous t-test approach:**
- Treated repeated measures as independent ❌
- Could not detect interactions ❌
- Inflated Type I error rate ❌
- Inconsistent with TE/ER/SE analysis from yesterday ❌

**Current MLM approach:**
- Accounts for within-subject correlations ✓
- Can detect Sex × Stress interactions ✓
- Proper hierarchical structure ✓
- **Matches yesterday's TE/ER/SE methodology** ✓

---

## PART 1: Accel/Decel Ratios (Figures 3 & 4)

### Model Specification

```
Fraction ~ Sex × Stress × HR_Source × Event_Type + (1|Patient_ID)
```

**Data structure:**
- 480 observations (120 patients × 4 measurements each)
- 4 measurements per patient: mHR_accel, mHR_decel, fHR_accel, fHR_decel
- Random intercept accounts for patient-level correlation

### Significant Effects (p < 0.05)

| Effect | β | SE | p-value | Interpretation |
|--------|---|----|---------| ---------------|
| **Event_Type (deceleration)** | -0.0606 | 0.0028 | <0.001*** | Decelerations occur 6.1% less frequently than accelerations |
| **HR_Source(maternal) × Event_Type(decel)** | +0.0282 | 0.0028 | <0.001*** | The decel reduction is LESS pronounced in maternal HR |
| **HR_Source (maternal)** | -0.0109 | 0.0028 | <0.001*** | Maternal HR shows slightly different baseline pattern |

### Non-Significant Effects

| Effect | β | p-value | Note |
|--------|---|---------|------|
| Sex (male) | -0.0026 | 0.361 | No overall sex difference |
| Stress (stressed) | 0.0007 | 0.802 | No stress effect |
| **Sex × Stress** | -0.0001 | 0.985 | **No interaction** |
| Sex × HR_Source | 0.0027 | 0.342 | ns |
| Sex × Event_Type | 0.0014 | 0.626 | ns |
| Stress × HR_Source | -0.0005 | 0.865 | ns |
| Stress × Event_Type | -0.0013 | 0.651 | ns |

### Key Findings for Manuscript

**Figure 3 (Overall patterns):**
- Accelerations significantly more common than decelerations (β = -0.061, p < 0.001)
- This asymmetry differs by HR source (interaction p < 0.001)
- **Fetal HR**: 52.1% accel, 46.0% decel (stronger asymmetry)
- **Maternal HR**: 51.1% accel, 47.8% decel (weaker asymmetry)

**Figure 4 (Group comparisons):**
- **No significant Sex effects** (p = 0.361)
- **No significant Stress effects** (p = 0.802)
- **No Sex × Stress interaction** (p = 0.985)

**Comparison to t-test results:**
- T-tests found: Male vs Female deceleration p = 0.045
- **MLM finds**: This effect disappears when accounting for repeated measures (p = 0.626)
- **Conclusion**: The t-test finding was likely a Type I error from treating repeated measures as independent

---

## PART 2: Hmax/Hmean Values (Figures 6 & 7)

### Model Specification

```
Value ~ Sex × Stress × Metric × HR_Source × Conditioning + (1|Patient_ID)
(with selected 2-way interactions)
```

**Data structure:**
- 1,262 observations (average 10.5 per patient)
- Variable observations per patient due to NaN filtering
- Conditions: none, fetus_accel, fetus_decel, mother_accel, mother_decel

### Significant Effects (p < 0.05)

| Effect | β | SE | p-value | Interpretation |
|--------|---|----|---------| ---------------|
| **Conditioning (none)** | +0.2061 | 0.0351 | <0.001*** | No conditioning → higher entropy (less negative) |
| **Conditioning (mother_decel)** | -0.1228 | 0.0491 | 0.012* | Mother decel → lower entropy |
| **Metric (hmean)** | -0.1172 | 0.0515 | 0.023* | Hmean consistently lower than hmax |

### Marginal/Trending Effects (p < 0.10)

| Effect | β | p-value | Note |
|--------|---|---------|------|
| Conditioning (fetus_decel) | -0.0816 | 0.054 | Trend toward lower entropy |

### Non-Significant Effects

| Effect | β | p-value | Note |
|--------|---|---------|------|
| Sex (male) | -0.1058 | 0.177 | No overall sex difference |
| Stress (stressed) | -0.0852 | 0.128 | No stress effect ⚠️ |
| **Sex × Stress** | +0.1079 | 0.223 | **No interaction** ⚠️ |
| Sex × HR_Source | 0.0598 | 0.153 | ns |
| Sex × Conditioning (all) | - | >0.24 | All ns |

**⚠️ Data Quality Note**: Stressed vs Control likely unreliable due to data duplication issue flagged earlier. Rerun when corrected data available.

### Key Findings for Manuscript

**Conditioning Effects:**
- **No conditioning** (baseline): Highest entropy values
- **Mother deceleration**: Significantly reduces entropy (β = -0.123, p = 0.012)
- **Fetal deceleration**: Trend toward reduction (β = -0.082, p = 0.054)

**Metric Differences:**
- **Hmean** consistently 0.117 units lower than **hmax** (p = 0.023)

**Group Effects:**
- No significant Sex, Stress, or Sex × Stress effects detected
- Likely due to data quality issue (reanalyze with corrected data)

**Comparison to t-test results:**
- T-tests found: Male vs Female hmax_fetus_mother_accel p = 0.028
- **MLM finds**: This effect becomes non-significant in full model (p = 0.246 for Sex × mother_accel)
- **Conclusion**: May be specific to that condition, not a general sex effect

---

## Comparison: MLM vs T-test Approach

| Aspect | T-test Approach | MLM Approach | Winner |
|--------|----------------|--------------|--------|
| **Accel/Decel Sex Effect** | p = 0.045* | p = 0.361 (ns) | **MLM** (accounts for correlation) |
| **Hmax Sex Effect** | p = 0.028* | p = 0.246 (ns) | **MLM** (proper hierarchical structure) |
| **Interaction Detection** | Not possible | Full factorial tested | **MLM** |
| **Consistency** | Inconsistent with TE/ER/SE | Matches yesterday | **MLM** |
| **Statistical Validity** | Pseudoreplication | Proper repeated measures | **MLM** |

**Key Insight**: The "significant" sex effects from t-tests **disappear** when properly accounting for:
1. Within-subject correlations
2. Multiple measurements per patient
3. Hierarchical data structure

This is a classic case of **pseudoreplication** being corrected by proper mixed modeling.

---

## Manuscript Updates Needed

### Figure 3 Caption

**Add:**
"Mixed linear model analysis revealed significant main effect of event type (β = -0.061, p < 0.001) and HR_Source × Event_Type interaction (β = 0.028, p < 0.001), indicating accelerations occur more frequently than decelerations with stronger asymmetry in fetal HR conditioning. Model: Fraction ~ Sex × Stress × HR_Source × Event_Type + (1|Patient_ID), REML estimation, n=120 patients, 480 observations."

### Figure 4 Caption

**Replace previous text with:**
"Group comparisons using mixed linear models revealed no significant sex (p = 0.361) or stress effects (p = 0.802) on acceleration/deceleration patterns. Sex × Stress interaction was also non-significant (p = 0.985). Results indicate accel/decel asymmetry is consistent across demographic groups. Same model specification as Figure 3."

### Figure 6 & 7 Caption

**Add:**
"Mixed linear model revealed significant conditioning effects: no conditioning showed highest entropy (β = +0.206, p < 0.001) while maternal deceleration reduced entropy (β = -0.123, p = 0.012). Hmean was consistently lower than hmax (β = -0.117, p = 0.023). No significant sex (p = 0.177) or stress effects (p = 0.128) detected. Model: Value ~ Sex × Stress × Metric × HR_Source × Conditioning + (1|Patient_ID), REML estimation, n=120 patients, 1,262 observations. Note: Stress effects require validation with corrected group assignment data."

---

## Statistical Methods Section (for manuscript)

### Recommended Text

"Statistical analysis employed mixed linear models (MLMs) with restricted maximum likelihood (REML) estimation to account for repeated measures within subjects. For acceleration/deceleration ratios, the model specification was:

```
Fraction ~ Sex × Stress × HR_Source × Event_Type + (1|Patient_ID)
```

For entropy rate values (hmax/hmean), we used:

```
Value ~ Sex × Stress × Metric × HR_Source × Conditioning + (1|Patient_ID)
```

Random intercepts for Patient_ID accounted for within-subject correlation across multiple measurements. This approach is consistent with our analysis of transfer entropy and entropy rate in the main results, enabling detection of interaction effects (e.g., Sex × Stress) while properly handling the hierarchical data structure. Statistical significance was assessed at α = 0.05."

---

## Files Generated

1. **mlm_accel_decel_data.csv** - Reshaped data in long format (480 rows)
2. **mlm_accel_decel_results.csv** - MLM coefficients and p-values
3. **mlm_hmax_hmean_data.csv** - Reshaped data in long format (1,262 rows)
4. **mlm_hmax_hmean_results.csv** - MLM coefficients and p-values
5. **mlm_analysis_results.txt** - Complete analysis output with full model summaries
6. **mixed_linear_model_analysis.py** - Reusable analysis script

---

## Next Steps

1. **Update manuscript figures** with MLM-derived p-values and effect sizes
2. **Remove t-test results** that showed spurious sex effects
3. **Add statistical methods** section text describing MLM approach
4. **Rerun hmax/hmean analysis** when corrected stressed/control data available
5. **Verify consistency** with yesterday's TE/ER/SE findings (all using MLM)

---

## Replication Instructions

To re-run when you get corrected hmax/hmean data:

```bash
python3 mixed_linear_model_analysis.py
```

The script will:
- Load corrected .npz files from `hmax_values/` directory
- Reshape data to long format
- Fit MLM models with REML
- Generate updated results tables
- Save new CSV files

**Expected outcome**: Stress effects should become detectable once data duplication is resolved.
