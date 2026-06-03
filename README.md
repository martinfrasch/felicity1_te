# FELICITy1 Transfer Entropy Analysis

**Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester: impact of fetal sex and maternal chronic stress**

[![arXiv](https://img.shields.io/badge/arXiv-2512.22270-b31b1b.svg)](https://arxiv.org/abs/2512.22270)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Manuscript Access

**arXiv Preprint**: arXiv:2512.22270 [q-bio.QM]
                    https://doi.org/10.48550/arXiv.2512.22270

**Published Article**: [[published paper](https://doi.org/10.3390/biology15100749)]

> **Note**: This repository contains analysis code and figures for reproducibility. The full manuscript is available via the links above.

---

## Overview

This repository provides the analysis code and publication figures for a study of maternal-fetal heart rate coupling using information-theoretical measures. The research examines how prenatal maternal stress affects physiological communication between mother and fetus through analysis of transfer entropy (TE), entropy rate (ER), and sample entropy (SE).

### Key Findings

- **Dual Coupling Mechanisms**: Stress-invariant state-dependent synchronization and stress-sensitive temporal information transfer
- **60% Coupling Strength**: Maternal heart rate decelerations exert approximately 60% coupling strength on fetal heart rate complexity
- **Sex-by-Stress Interaction**: Robust interaction in transfer entropy from mixed linear models
- **4 Hz Sufficiency**: Standard fetal monitoring sampling rate sufficient to capture information flow
- **SE vs ER Dissociation**: Sample entropy does not detect cross-signal coupling despite adequate data quality, confirming SE and ER capture fundamentally different aspects of HR dynamics

---

## Repository Structure

```
felicity1_te/
├── README.md                                    # This file
├── LICENSE                                      # MIT License
├── requirements.txt                             # Python dependencies
│
├── Core Analysis Scripts
│   ├── corrected_group_analysis.py              # Patient data pipeline & group assignment
│   ├── mixed_linear_model_analysis_complete.py  # Complete MLM analysis (ER, SE, TE)
│   ├── mixed_linear_model_analysis.py           # MLM implementation (v1)
│   ├── mixed_linear_model_analysis_v2.py        # MLM implementation (v2)
│   ├── sensitivity_analysis_covariates.py       # Covariate sensitivity analysis (R2) *NEW*
│   ├── rerun_SE_MLM_new_data.py                 # SE MLM with recomputed SampEn (R2) *NEW*
│   ├── sample_entropy_mlm_analysis.py           # Sample entropy MLM
│   ├── sample_entropy_mlm_analysis_simplified.py # Simplified SE MLM
│   ├── statistical_analysis_v2.py               # Statistical tests
│   └── validate_data.py                         # Data validation & group verification
│
├── Figure & Visualization Scripts
│   ├── generate_figures.py                      # Figure generation
│   ├── generate_correlation_heatmaps.py         # Correlation heatmaps
│   ├── generate_correlation_heatmaps_sex_stratified.py
│   ├── generate_correlation_heatmaps_sex_stress.py
│   ├── generate_publication_materials.py        # Publication-ready tables/figures
│   ├── reproduce_manuscript_figures.py          # Reproducibility script
│   └── verify_group_assignments.py              # Group assignment verification
│
├── Figures (12 PDF files)
│   └── figures/
│
└── Results (4 files)
    ├── mlm_accel_decel_results.csv
    ├── mlm_hmax_hmean_results.csv
    ├── sample_entropy_mlm_results_simplified.csv
    └── sample_entropy_mlm_results_simplified.txt
```

---

## Study Design

### Cohort
- **N = 118** mother-fetus dyads in third trimester (analytical sample)
  - 59 stressed group (PSS ≥ 19)
  - 59 control group (PSS < 19)
  - 49 male fetuses, 69 female fetuses
- **Design**: Prospective matched cohort study
- **Measurements**: Transabdominal ECG (AN24 device) → SAVER-extracted maternal and fetal HR

### Exclusions
From the initial 165 participants, 47 dyads were excluded:
- 45 due to fHR indistinguishable from mHR (below 100 bpm)
- 1 (FS-004) lacking clinical records
- 1 (FS-144) missing PSS score precluding stress classification

Additionally, 1 participant (FS-124) was excluded from Table 2 only (net TE outlier, z-score = 23.7), yielding n = 117 for that analysis.

### Information-Theoretical Measures
- **Transfer Entropy (TE)**: Directed information flow from maternal to fetal heart rate
- **Entropy Rate (ER)**: Rate of new information generation in HR time series
- **Sample Entropy (SE)**: Signal regularity and complexity

### Conditioning Paradigms
- Full recording analysis (no conditioning)
- Acceleration epochs (HR increases)
- Deceleration epochs (HR decreases)
- Applied to both maternal and fetal HR → 50 features total

### Statistical Analysis
- Mixed linear models with random intercepts (accounting for repeated measures)
- Sensitivity analysis with covariates (gestational age, maternal age, BMI)
- False Discovery Rate (FDR) correction for multiple comparisons
- Exploratory correlations with maternal cortisol and infant neurodevelopmental outcomes
- Gaussian probability metric for Table 2 (proportion of cohort with reversed net TE)

---

## Requirements

### Installation

```bash
pip install -r requirements.txt
```

### Dependencies
- numpy >= 1.21.0
- pandas >= 1.3.0
- scipy >= 1.7.0
- statsmodels >= 0.13.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0

---

## Usage

### Running Analyses

**Note**: Raw data is not included in this repository due to privacy restrictions. The scripts are provided for transparency and can be run with appropriately formatted data.

```bash
# Core analyses
python corrected_group_analysis.py              # Build patient-level dataset
python mixed_linear_model_analysis_complete.py  # Run all MLMs (ER, SE, TE)
python sensitivity_analysis_covariates.py       # Covariate sensitivity (R2)
python rerun_SE_MLM_new_data.py                 # SE MLM with recomputed data (R2)

# Figures and visualizations
python generate_correlation_heatmaps.py
python generate_correlation_heatmaps_sex_stratified.py
python generate_correlation_heatmaps_sex_stress.py
python reproduce_manuscript_figures.py
```

### Expected Data Format

The analysis scripts expect:
- `patient_level_data_corrected.csv`: Patient IDs, sex, stress group, entropy features
- `.npz` files from Nicolas Garnier's entropy computation toolbox
- `FELICITy-Dataset-MixedModels.ods`: Clinical outcomes (Bayley, cortisol)

---

## Key Results

### Coupling Strength
- Maternal heart rate decelerations → 60% coupling strength on fetal complexity
- Effect conserved across sex and stress groups (p = 0.128 for stress effect)
- Represents fundamental physiological coordination

### Transfer Entropy
- Net TE significantly positive in all subgroups (p = 0.021–0.032, Table 2)
- Significant stress effect (p = 0.026) and sex-by-stress interaction (p = 0.009) in MLM
- Exploratory associations with maternal cortisol (not FDR-corrected)

### Sample Entropy vs Entropy Rate
- With recomputed SE (99.5% non-zero, 2,348 obs), SE still does not detect cross-signal coupling
- Confirms SE and ER capture fundamentally different aspects of HR dynamics
- SE sensitive to within-signal state changes, ER to cross-signal coupling

### Acceleration Predominance
- Universal pattern in maternal and fetal heart rates
- Stronger in fetal signals
- Independent of sex or stress status

---

## Revision History

### R2 (March 2025)
- Restructured manuscript: technical content moved to Supplementary Materials
- Added sensitivity analysis with covariates (GA, maternal age, BMI)
- Recomputed sample entropy with improved algorithm (286 → 2,348 observations)
- Data reconciliation: identified and excluded FS-004, FS-144, FS-124 (from Table 2)
- Final sample: N = 118 (117 for Table 2)
- Added "From Information Metrics to Physiological Meaning" Discussion section
- Corrected Table 2 statistical method description

### R1 (December 2024)
- Initial submission with complete analysis

---

## Citation

**arXiv**: arXiv:2512.22270 [q-bio.QM]
           https://doi.org/10.48550/arXiv.2512.22270

**Entropy metrics toolbox**: https://github.com/nbgarnier/entropy

```bibtex
@article{garnier2025felicity_te,
  title={Measuring the time-scale-dependent information flow between maternal
         and fetal heartbeats during the third trimester: impact of fetal sex
         and maternal chronic stress},
  author={Garnier, Nicolas B. and Molinet, Maria S. and Antonelli, Marta C.
          and Lobmaier, Silvia M. and Frasch, Martin G.},
  journal={Biology},
  year={2025},
  note={arXiv:2512.22270}
}
```

---

## Data Availability

**Raw patient data is excluded** from this repository to protect participant privacy.

**What's included**:
- All analysis code (Python scripts)
- Publication figures (PDF)
- Analysis results (CSV) for verification
- Software requirements and setup instructions

**Data sharing**: Anonymized data may be available upon reasonable request and appropriate ethics approval. Contact the corresponding author.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

- Nicolas B. Garnier: nicolas.garnier@ens-lyon.fr
- Martin G. Frasch: mfrasch@uw.edu

---

## Keywords

Maternal-fetal coupling, transfer entropy, entropy rate, sample entropy, prenatal stress programming, fetal autonomic development, heart rate variability, mixed linear models, sex differences, conditioning framework

---

**Last Updated**: March 2025
