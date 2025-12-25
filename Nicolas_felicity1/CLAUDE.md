# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Analysis of maternal-fetal heart rate entropy features in relation to clinical biomarkers. This project extends Section 3.4 ("TE in relation to other biomarkers") of the manuscript on measuring time-scale-dependent information flow between maternal and fetal heartbeats.

## Data Files

- `entropy_rate.txt` - Entropy rate estimates (11 columns: patient_code + 10 features)
- `SampEn.txt` - Sample entropy estimates (11 columns: patient_code + 10 features)
- `max_TE_fHR_conditioning.csv` - Max Transfer Entropy with fetal HR conditioning
- `max_TE_mHR_conditioning.csv` - Max Transfer Entropy with maternal HR conditioning
- `mean_TE_fHR_conditioning.csv` - Mean Transfer Entropy with fetal HR conditioning
- `mean_TE_mHR_conditioning.csv` - Mean Transfer Entropy with maternal HR conditioning
- `210716 EXCEL FILE FOR BAYLEY-STAN.xlsx` - Clinical outcomes (patient code format: "FS-XXX")

### TE File Structure (6 columns)
1. patient_code
2. sex (1=male, 0=female)
3. stress (1=stressed, 0=non-stressed)
4. all - Net TE using all points
5. accel - Net TE on acceleration points only
6. decel - Net TE on deceleration points only

### Feature Structure (columns 2-11 in txt files)
1. fetus_full - Fetus estimate using full data
2. mother_full - Mother estimate using full data
3-4. fetus/mother_fHR_accel - Estimates during fHR accelerations
5-6. fetus/mother_fHR_decel - Estimates during fHR decelerations
7-8. fetus/mother_mHR_accel - Estimates during mHR accelerations
9-10. fetus/mother_mHR_decel - Estimates during mHR decelerations

All estimates are AUC in the [0.5-2.5]s time interval.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run full analysis
python run_analysis.py

# Run analysis only (no plots)
python run_analysis.py --analysis-only

# Generate plots only
python run_analysis.py --plots-only
```

## Architecture

```
├── src/
│   ├── data_loader.py          # Data loading and merging utilities
│   ├── analysis.py             # Univariate analysis (correlations, group comparisons)
│   ├── visualization.py        # Plotting functions
│   └── multivariate_analysis.py # Multivariate models (Elastic Net, PCA, PLS, RF)
├── output/                     # Generated results (CSV files and PNG plots)
├── run_analysis.py             # Main entry point
└── requirements.txt            # Python dependencies
```

### Key Functions

- `data_loader.merge_all_data()` - Loads and merges all data sources by patient_code
- `analysis.test_normality()` - Shapiro-Wilk test for normality (α=0.05)
- `analysis.compute_correlations()` - Correlations with automatic method selection:
  - Tests normality of both variables using Shapiro-Wilk
  - Uses Pearson if both normal, Spearman otherwise
  - Reports method used and normality status in output
- `analysis.run_group_comparison()` - Mann-Whitney U tests for stressed vs control groups
- `analysis.get_stress_group()` - Categorizes subjects by PSS score (>=19 = stressed)

## Outcome Variables

**Stress indicators:** Mother Score_PSS, Mother Score PDQ, Mother CORTISOL
**Cognitive:** COG COMPOSITE SCORE
**Language:** LANG RECEPT SCORE, LANG EXPRES SCORE, LANG COMP SCORE
**Motor:** MOTOR FINE SKILLS SCORE, MOTOR GROSS SKILLS SCORE, MOTOR COMPOSITE SCORE

## Key Findings (as of latest analysis)

1. **TE correlates with cortisol only** (7 significant, r=0.21-0.31, all positive)
2. **ER/SE correlate with Bayley scores only** (6 significant with motor/language)
3. **Distinct pathways:** TE → stress physiology; ER/SE → development
4. **Sex effect:** Female fetuses show 9 TE correlations; males show 0
5. **Stress moderation:** Effect directions reverse between stressed/control groups
6. **Multivariate models underpowered:** n/k ratio ~1.0, need n>150 for 32 features

## Output Files

- `RESULTS_SUMMARY.md` - Main manuscript-style findings
- `MULTIVARIATE_RESULTS.md` - Multivariate analysis details
- `TE_CORRELATION_SUMMARY.md` - TE-specific findings
- `MANUSCRIPT_SECTIONS.md/.tex` - Full Methods/Results/Discussion for publication
- `SESSION_SUMMARY.md` - Detailed session summary for future reference
