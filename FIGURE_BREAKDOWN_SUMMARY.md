# Figure Breakdown Summary

**Date**: December 17, 2025
**Purpose**: Enhanced manuscript figures with sex and group breakdowns

---

## Updated Figures Overview

All figures now include comprehensive breakdowns by **sex** (male/female) and **stress group** (stressed/control), in addition to the complete cohort ("all").

### Group Definitions
- **all**: Complete cohort (n=119)
- **stressed**: Mothers exposed to stress (n=59)
- **control**: Control group (n=60)
- **male fetus**: Male fetuses (n=49)
- **female fetus**: Female fetuses (n=70)

---

## Figure 6: Entropy Rate - No Conditioning

**Layout**: 1 row × 5 columns (unchanged from original)

**Columns**: all | stressed | control | male fetus | female fetus

**Each subplot shows**:
- Blue box: Maternal HR (mHR) entropy rate
- Red box: Fetal HR (fHR) entropy rate

**Data**: Mean values only (hAUC) - hmax not available

**File**: `Figure_6_ER_no_conditioning_MEAN_ONLY.png`

---

## Figure 7: Entropy Rate - With Conditioning ⭐ NEW BREAKDOWN

**Layout**: 4 rows × 5 columns

**Rows (conditioning types)**:
1. fHR accel - During fetal heart rate accelerations
2. fHR decel - During fetal heart rate decelerations
3. mHR accel - During maternal heart rate accelerations
4. mHR decel - During maternal heart rate decelerations

**Columns (groups)**: all | stressed | control | male fetus | female fetus

**Each subplot shows**:
- Blue box: mHR entropy rate
- Red box: fHR entropy rate

**Total subplots**: 20 (4 conditioning types × 5 groups)

**Data**: Mean values only (hAUC) - hmax not available

**File**: `Figure_7_ER_with_conditioning_MEAN_ONLY.png`

---

## Figure 11: Transfer Entropy - No Conditioning ⭐ NEW BREAKDOWN

**Layout**: 2 rows × 5 columns

**Rows**:
1. Top row: TEmax (maximal transfer entropy)
2. Bottom row: TEauc/mean (mean transfer entropy)

**Columns (groups)**: all | stressed | control | male fetus | female fetus

**Each subplot shows**:
- Single box: Net TE = TE(m→f) - TE(f→m)
- Red dashed line: Zero reference (no directional flow)
- P-value annotation: Tests H₀: mean net TE = 0

**Total subplots**: 10 (2 TE types × 5 groups)

**P-value interpretation**:
- One-sample t-test against 0
- H₀: mean net TE = 0 (no directional information flow)
- Tests whether maternal→fetal information flow differs significantly from zero

**File**: `Figure_11_TE_no_conditioning.png`

---

## Figure 12: Transfer Entropy - With Conditioning ⭐ NEW BREAKDOWN

**Layout**: 2 rows × 4 columns

**Rows**:
1. Top row: TEmax (maximal transfer entropy)
2. Bottom row: TEauc/mean (mean transfer entropy)

**Columns (conditioning types)**:
1. mHR accel - During maternal HR accelerations
2. mHR decel - During maternal HR decelerations
3. fHR accel - During fetal HR accelerations
4. fHR decel - During fetal HR decelerations

**Each subplot shows 5 color-coded boxes**:
- Gray: all (complete cohort)
- Red: stressed
- Blue: control
- Green: male fetus
- Orange: female fetus

**Total subplots**: 8 (2 TE types × 4 conditioning types)

**Within each subplot**: 5 boxes (one per group)

**P-value annotations**:
- Shows p-value for "all" group only (to avoid clutter)
- One-sample t-test H₀: mean net TE = 0
- Located in upper-left corner of each subplot

**File**: `Figure_12_TE_with_conditioning.png`

---

## P-Value Clarification

**What the p-values test**:
- **Null hypothesis (H₀)**: mean net TE = 0
- **Interpretation**: No directional information flow between maternal and fetal heart rates
- **Statistical test**: One-sample t-test against 0
- **Significance**: p < 0.05 indicates significant directional information flow

**Why test against 0?**
- Net TE is defined as: TE(maternal→fetal) - TE(fetal→maternal)
- If net TE = 0, information flows equally in both directions (no net directionality)
- If net TE > 0, dominant flow is maternal→fetal
- If net TE < 0, dominant flow is fetal→maternal

---

## Data Integrity Notes

**Ground Truth**: All group assignments verified against `groups_scores_new.xlsx`

**Sample Sizes**:
- Total: n=119 patients
- Stress groups: Control n=60, Stressed n=59
- Sex groups: Female n=70, Male n=49

**Data Limitations**:
- **Entropy Rate**: Only mean (hAUC) values available from `entropy_rate.txt`
  - Cannot reproduce hmax portions of Figures 6 & 7
  - Figures labeled with "⚠️ hmax not available"

- **Transfer Entropy**: Both max and mean values available from CSV files
  - Full reproduction of Figures 11 & 12 possible

**Missing Data Handling**:
- Some conditioning types have reduced sample sizes (e.g., fHR decel: n=25 male, n=37 female)
- Subplots show "n=0" or "Data not available" when insufficient data
- All box plots based on non-missing values only

---

## Key Findings from Sex/Group Breakdown

### Entropy Rate (Figures 6 & 7)
- Visual inspection shows minimal differences between stressed/control groups
- Some sex differences visible, particularly in fetal ER during mHR conditioning
- Consistent with statistical report: no significant stress effects, 4 nominal sex effects

### Transfer Entropy (Figures 11 & 12)
- Most groups show net TE slightly positive (maternal→fetal dominance)
- P-values generally > 0.05 across most groups and conditions
- Visual consistency with statistical report: no strong directional flow patterns

---

## Files Generated

```
analysis_output_corrected/manuscript_figures/
├── Figure_6_ER_no_conditioning_MEAN_ONLY.png
├── Figure_7_ER_with_conditioning_MEAN_ONLY.png
├── Figure_11_TE_no_conditioning.png
└── Figure_12_TE_with_conditioning.png
```

## References

- Statistical analysis: `CORRECTED_STATISTICAL_REPORT.md`
- Patient-level data: `analysis_output_corrected/patient_level_data_corrected.csv`
- Sex effects results: `analysis_output_corrected/sex_effects_corrected.csv`
- Exposure effects results: `analysis_output_corrected/exposure_effects_corrected.csv`
