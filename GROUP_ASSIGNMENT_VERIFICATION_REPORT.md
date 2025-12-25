# Group Assignment Verification Report
## Comparison of groups_scores_new.xlsx vs TE/ER Data Files

**Date:** December 17, 2025
**Analysis:** Group Assignment Cross-Validation
**Status:** 🚨 CRITICAL DISCREPANCIES FOUND

---

## Executive Summary

**CRITICAL FINDING:** The group assignments in the .npz data files **DO NOT match** the group assignments in `groups_scores_new.xlsx`.

### Key Discrepancies

1. **Patient Count Mismatch:**
   - Excel file (`groups_scores_new.xlsx`): **165 patients** (86 control, 79 stressed)
   - TE/ER data files (.npz): **120 patients** (58 control, 58 stressed)
   - **45 patients** in Excel file are not in TE/ER data

2. **Group Distribution Mismatch:**
   - For the 120 patients in TE/ER data:
     - **Excel shows:** 60 control, 59 stressed (based on entropy_rate.txt patient IDs)
     - **NPZ files contain:** 58 control, 58 stressed
   - **Discrepancy:** 2 fewer control, 1 fewer stressed in .npz vs expected from Excel

3. **Missing Patient:**
   - Patient **FS-004** appears in entropy_rate.txt but is **NOT in Excel file**
   - This suggests either:
     - Data from different time points/versions
     - Manual patient exclusion/inclusion

---

## Detailed Findings

### 1. Excel File Analysis (`groups_scores_new.xlsx`)

**Total Patients:** 165

**Group Distribution:**
- Group 0 (Control): 86 patients
- Group 1 (Stressed): 79 patients

**Data Completeness:**
- Patients with complete data (no missing values): 125
- Patients with missing data: 40
- Missing Cortisol values: 40 (24.2%)
- Missing PSS/PDQ scores: 1 patient each (0.6%)

**If we drop patients with missing data:**
- Remaining: 125 patients (68 control, 57 stressed)
- This does NOT match .npz file counts (120 patients, 58/58)

---

### 2. TE/ER Data Files Analysis

**Source Files Examined:**
- `TE_ER_data/*.npz` (22 files)
- `entropy_rate.txt` (patient ID mapping)

**Total Patients in TE/ER Data:** 120

**Group Distribution (from .npz files):**
- Control: 58 patients
- Stressed: 58 patients
- Male: 49 patients
- Female: 68 patients

**Patient IDs (from entropy_rate.txt):**
- 120 unique patient IDs extracted
- Format: FS-001, FS-002, FS-004, FS-005, ... FS-167
- Not consecutive (many gaps: e.g., FS-003, FS-007, FS-012 missing)

---

### 3. Cross-Reference Analysis

**Matching entropy_rate.txt IDs with Excel:**
- Patients in entropy_rate.txt: 120
- Matched to Excel: **119 patients**
- Not found in Excel: **FS-004** (1 patient)

**Group Counts for Matched 119 Patients:**
- Control (Group 0): 60
- Stressed (Group 1): 59

**Comparison with .npz files:**
```
Source                  Total    Control    Stressed
------------------------------------------------------
Excel (matched 119)     119      60         59
NPZ files               120      58         58
------------------------------------------------------
Discrepancy             +1       -2         -1
```

---

### 4. Identified Issues

#### Issue 1: Balanced Groups Suggest Manual Adjustment
The .npz files have exactly **58/58 (balanced)** groups, while Excel suggests **60/59 (unbalanced)** for the same patients.

**Implications:**
- Someone manually balanced the groups to 58/58
- This involved removing 2 control patients and 1 stressed patient
- No documentation found explaining which patients were excluded or why

#### Issue 2: Patient FS-004 Mystery
- Appears in `entropy_rate.txt` (data source)
- Does NOT appear in `groups_scores_new.xlsx`
- Suggests potential version mismatch between files

#### Issue 3: Statistical Analysis Validity
**The previous statistical analysis used group assignments from the .npz files (58 stressed, 58 control).**

**Questions:**
1. Are these the correct group assignments?
2. If we use Excel file groups (60/59 for the matched 119 patients), would results differ?
3. Which source is the "ground truth" for group assignments?

---

## Data Quality Issues Previously Identified

### Files with Identical Stressed/Control Data

The following 6 files contain **identical values** for stressed and control groups:

1. `TEmax_no-condioning.npz`
2. `TEmean_no-condioning.npz`
3. `hmax_fetus_no_conditoning.npz`
4. `hmax_mother_no_conditoning.npz`
5. `hmean_fetus_no_conditoning.npz`
6. `hmean_mother_no_conditoning.npz`

**Impact:** All "no conditioning" features return t = 0.000, p = 1.000 (no difference possible)

**Status:** This is a separate data generation error, independent of group assignment issues

---

## Critical Questions Requiring Clarification

### 1. Group Assignment Authority
**Question:** Which source contains the correct group assignments?
- Option A: `groups_scores_new.xlsx` (ground truth from study)
- Option B: `.npz files` (data as created for analysis)
- Option C: Another source not yet examined

**Action Required:** Verify with study team/data manager

### 2. Patient Selection Process
**Question:** How were the 120 patients selected from the 165 in the Excel file?

**Possible explanations:**
- Patients with insufficient TE/ER data quality were excluded
- Balanced matching was performed (58/58) for statistical reasons
- Only patients with complete heart rate recordings were included
- Specific exclusion criteria were applied

**Action Required:** Review data processing documentation or consult with analyst

### 3. FS-004 Patient Status
**Question:** Why does FS-004 appear in TE/ER data but not in Excel?

**Possible explanations:**
- Excel file is outdated (created before FS-004 was added)
- FS-004 was removed from Excel after TE/ER analysis (data quality issue)
- Files from different study phases

**Action Required:** Verify patient roster and data collection timeline

---

## Impact on Statistical Analysis

### Previous Analysis (STATISTICAL_ANALYSIS_REPORT.md)

**What was analyzed:**
- Stressed (n=58) vs Control (n=58) from .npz files
- Male (n=49) vs Female (n=68) from .npz files

**Results:**
- No significant differences found (all p > 0.05)
- All effect sizes negligible (|Cohen's d| < 0.2)

### Potential Issues if Group Assignments are Wrong

**If the Excel file is correct and .npz files have wrong groups:**

1. **Wrong patients in wrong groups:** Statistical comparisons are invalid
2. **Type II error:** True differences might be masked by misclassification
3. **Confounding:** Results cannot be trusted without proper group assignments

**However:**

The effect sizes are **uniformly negligible** (d < 0.2), which suggests:
- Even with some misclassification, effects are very small
- Major group differences would likely still be detected
- But precise estimates and p-values would be affected

---

## Recommendations

### Immediate Actions (Priority 1)

1. **✅ DONE:** Cross-reference patient IDs from entropy_rate.txt with Excel file
   - Output: `patient_group_mapping.csv`

2. **⚠️ URGENT:** Contact study team/data manager to clarify:
   - Which group assignment source is correct?
   - How were patients selected for TE/ER analysis (120 from 165)?
   - Why are groups balanced to 58/58 when Excel shows 60/59?
   - What is the status of patient FS-004?

3. **⚠️ URGENT:** Locate data processing documentation:
   - How were .npz files created?
   - Which patients were excluded and why?
   - Was manual group balancing performed?

### Short-Term Actions (Priority 2)

4. **Verify group assignments at patient level:**
   - Create patient-level dataset linking IDs to TE/ER values
   - Cross-check actual data values against group assignments
   - Look for patterns suggesting misclassification

5. **Re-generate .npz files if needed:**
   - If Excel is confirmed as ground truth
   - Use correct group assignments (60 control, 59 stressed for 119 patients)
   - Address FS-004 patient (include or exclude with justification)

6. **Re-run statistical analysis:**
   - With verified correct group assignments
   - Compare new results to original findings
   - Assess sensitivity of conclusions to group assignment corrections

### Long-Term Actions (Priority 3)

7. **Document data provenance:**
   - Create README documenting patient selection process
   - Document group assignment sources and verification
   - Maintain audit trail for data processing steps

8. **Implement quality checks:**
   - Automated cross-validation between Excel and data files
   - Group assignment verification before analysis
   - Patient ID consistency checks

---

## Files Generated

### Verification Outputs

1. **`verify_group_assignments.py`**
   - Python script for group assignment verification
   - Compares Excel file with .npz files
   - Location: Project root directory

2. **`patient_group_mapping.csv`**
   - Patient-level mapping of IDs to group assignments
   - 120 patients from entropy_rate.txt
   - Group assignments from Excel (where available)
   - Location: Project root directory

3. **`GROUP_ASSIGNMENT_VERIFICATION_REPORT.md`** (this file)
   - Comprehensive documentation of discrepancies
   - Findings, implications, and recommendations
   - Location: Project root directory

---

## Conclusions

### Critical Findings

1. **Group assignment mismatch confirmed**
   - Excel: 60 control, 59 stressed (for 119 matched patients)
   - NPZ: 58 control, 58 stressed (for 120 patients)
   - Difference: 2 control, 1 stressed patient discrepancy

2. **Statistical analysis validity uncertain**
   - Previous analysis used .npz group assignments
   - Cannot confirm correctness without verification
   - Results may need revision if Excel is correct

3. **Data provenance unclear**
   - No documentation found for patient selection process
   - No explanation for group balancing (58/58)
   - Missing patient (FS-004) suggests version mismatch

### Next Steps

**BEFORE proceeding with any further analysis or publication:**

1. ✅ Verify which group assignment source is correct
2. ✅ Clarify patient selection process (165 → 120)
3. ✅ Resolve FS-004 patient discrepancy
4. ✅ Re-generate data files if needed with correct groups
5. ✅ Re-run statistical analysis with verified groups
6. ✅ Document complete data provenance chain

**The statistical analysis should be considered preliminary until group assignments are verified.**

---

## Contact for Questions

- Verification script: `verify_group_assignments.py`
- Patient mapping: `patient_group_mapping.csv`
- Original analysis: `STATISTICAL_ANALYSIS_REPORT.md`
- This report: `GROUP_ASSIGNMENT_VERIFICATION_REPORT.md`

**For questions about this verification analysis, refer to the generated files above.**
