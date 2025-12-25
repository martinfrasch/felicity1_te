# Statistical Analysis Summary for Figures 3, 4, 6, and 7

**Date**: December 18, 2025  
**Analysis**: Acceleration/deceleration ratios and entropy rate (hmax/hmean) values

---

## Figures 3 & 4: Acceleration/Deceleration Ratios

### Figure 3: Overall Statistics (All Subjects)

#### Maternal HR Conditioning
- **Fraction of accelerations**: 0.5107 ± 0.0122
  - **vs 0.5 (null hypothesis)**: t = 9.50, **p < 0.001***
  - Significantly MORE accelerations than expected by chance
  
- **Fraction of decelerations**: 0.4782 ± 0.0123
  - **vs 0.5**: t = -19.30, **p < 0.001***
  - Significantly FEWER decelerations than expected
  
- **Decel/Accel ratio**: 0.9375 ± 0.0453
  - **vs 1.0**: t = -15.04, **p < 0.001***
  - Decelerations occur ~6% less frequently than accelerations

#### Fetal HR Conditioning
- **Fraction of accelerations**: 0.5207 ± 0.0154
  - **vs 0.5**: t = 14.66, **p < 0.001***
  - Even stronger acceleration bias than maternal conditioning
  
- **Fraction of decelerations**: 0.4600 ± 0.0192
  - **vs 0.5**: t = -22.70, **p < 0.001***
  - Fewer decelerations
  
- **Decel/Accel ratio**: 0.8853 ± 0.0611
  - **vs 1.0**: t = -20.50, **p < 0.001***
  - Decelerations occur ~11% less frequently than accelerations

**Interpretation**: Both maternal and fetal HR show asymmetry favoring accelerations over decelerations. This asymmetry is MORE pronounced in fetal HR conditioning.

---

### Figure 4: Group Comparisons

#### Maternal HR Conditioning

**Stress Group (Stressed vs Control):**
- Fraction of accelerations: p = 0.331 (ns)
- Fraction of decelerations: p = 0.697 (ns)
- Decel/Accel ratio: p = 0.508 (ns)
- **No stress effects detected**

**Sex Group (Male vs Female):**
- Fraction of accelerations: p = 0.259 (ns)
- **Fraction of decelerations**: p = **0.045*** ✓
  - Male: 0.4805 ± 0.0112 (n=49)
  - Female: 0.4766 ± 0.0131 (n=68)
  - Males show slightly MORE decelerations than females
- Decel/Accel ratio: p = 0.103 (ns, trend)

#### Fetal HR Conditioning

**Stress Group (Stressed vs Control):**
- Fraction of accelerations: p = 0.588 (ns)
- Fraction of decelerations: p = 0.558 (ns)
- Decel/Accel ratio: p = 0.551 (ns)
- **No stress effects detected**

**Sex Group (Male vs Female):**
- Fraction of accelerations: p = 0.949 (ns)
- Fraction of decelerations: p = 0.454 (ns)
- Decel/Accel ratio: p = 0.629 (ns)
- **No sex effects detected**

**Summary for Figure 4**: Only ONE significant group difference detected across all comparisons:
- **Male vs Female deceleration fraction in maternal HR conditioning (p=0.045)**
- No stress effects on accel/decel patterns
- Fetal HR conditioning shows no group differences

---

## Figures 6 & 7: Entropy Rate (Hmax/Hmean) Values

### Key Findings

#### HMAX Analysis

**Significant Findings:**

1. **Fetus Mother Accel - Sex Effect**: p = **0.028*** ✓
   - Male: -0.9895 ± 0.3286 (n=47)
   - Female: -0.8647 ± 0.3761 (n=65)
   - Males show LOWER hmax (more negative = lower entropy) during maternal accelerations

**Non-Significant Findings:**
- No conditioning: No sex or stress effects
- Mother conditioning: No group differences detected
- Fetal conditioning (accel/decel): No group differences
- Maternal conditioning (accel/decel): No group differences

#### HMEAN Analysis

**All comparisons non-significant (all p > 0.05)**

Notable trend:
- Fetus Mother Accel - Sex Effect: p = 0.072 (trend)
  - Male: -1.0820 ± 0.3383 (n=47)
  - Female: -0.9703 ± 0.3920 (n=65)
  - Same pattern as HMAX (males lower) but not significant

---

## Important Data Quality Note

### Stressed vs Control Comparisons

**All stressed vs control comparisons show p = 1.000** across ALL conditions and metrics (both hmax and hmean).

**This indicates:**
- The stressed and control arrays contain **identical data**
- This is a **data processing issue** that needs investigation
- Mean and SD values are identical between stressed and control groups

**Example:**
- Hmax Fetus No Conditioning:
  - Stressed: -0.6481 ± 0.2698 (n=58)
  - Control: -0.6481 ± 0.2698 (n=58)
  - **Exact same values** → data duplication issue

**Recommendation**: Check the data generation pipeline for stressed/control group assignment in hmax/hmean files.

---

## Summary for Manuscript

### Figure 3 Statistics to Add:

**Maternal HR Conditioning:**
- Accelerations: 51.1% of points (p < 0.001 vs 50%)
- Decelerations: 47.8% of points (p < 0.001 vs 50%)
- Decel/Accel ratio: 0.94 (p < 0.001 vs 1.0)

**Fetal HR Conditioning:**
- Accelerations: 52.1% of points (p < 0.001 vs 50%)
- Decelerations: 46.0% of points (p < 0.001 vs 50%)
- Decel/Accel ratio: 0.89 (p < 0.001 vs 1.0)

### Figure 4 Statistics to Add:

**Key Finding:**
- Male vs Female deceleration fraction (maternal HR): p = 0.045
- No other significant group differences detected

**Interpretation**: Sex differences in deceleration patterns emerge specifically during maternal HR conditioning, with males showing slightly more decelerations than females.

### Figure 6 & 7 Statistics to Add:

**Key Finding (HMAX only):**
- Male vs Female fetus entropy during maternal accelerations: p = 0.028
- Males show lower entropy rate than females during maternal HR accelerations

**Data Quality Issue**: Stressed vs control comparisons cannot be performed due to identical data in stressed/control arrays (requires data verification).

---

## Statistical Methods Used

1. **Figure 3 (overall patterns)**: One-sample t-tests comparing fractions/ratios to null hypotheses (0.5 for fractions, 1.0 for ratios)
2. **Figure 4 (group comparisons)**: Mann-Whitney U tests (non-parametric) for stressed vs control and male vs female
3. **Figures 6 & 7 (entropy rate)**: Mann-Whitney U tests with NaN-aware filtering
4. **Significance threshold**: p < 0.05
5. **Sample sizes**: n=117-120 for accel/decel, variable for hmax/hmean depending on valid data points

---

## Files Generated

- `statistical_analysis_v2.py` - Main analysis script (NaN-aware)
- `statistical_results_complete.txt` - Complete analysis output
- `STATISTICAL_ANALYSIS_SUMMARY.md` - This summary document
