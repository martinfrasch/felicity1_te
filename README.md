# FELICITy1 Transfer Entropy Analysis

**Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester**

[![arXiv](https://img.shields.io/badge/arXiv-TBD-b31b1b.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📄 Manuscript Access

**arXiv Preprint**: [URL TBD - Coming Soon]

**Published Article**: [URL TBD - Coming Soon]

> **Note**: This repository contains analysis code and figures for reproducibility. The full manuscript is available via the links above.

---

## Overview

This repository provides the analysis code and publication figures for a study of maternal-fetal heart rate coupling using information-theoretical measures. The research examines how prenatal maternal stress affects physiological communication between mother and fetus through analysis of transfer entropy (TE), entropy rate (ER), and sample entropy (SE).

### Key Findings

- **Dual Coupling Mechanisms**: Stress-invariant state-dependent synchronization and stress-sensitive temporal information transfer
- **60% Coupling Strength**: Maternal heart rate decelerations exert approximately 60% coupling strength on fetal heart rate complexity
- **Sex-by-Stress Interaction**: Robust interaction in transfer entropy from mixed linear models
- **Optimal Sampling**: 4 Hz identified as optimal sampling rate for information flow capture

---

## Repository Structure

```
felicity1_te/
├── README.md                                    # This file
├── LICENSE                                      # MIT License
├── requirements.txt                             # Python dependencies
│
├── Analysis Scripts (16 files)
│   ├── mixed_linear_model_analysis.py          # MLM implementation
│   ├── generate_correlation_heatmaps.py        # Correlation analysis
│   ├── sample_entropy_mlm_analysis_simplified.py
│   ├── statistical_analysis_v2.py              # Statistical tests
│   ├── generate_figures.py                     # Figure generation
│   ├── reproduce_manuscript_figures.py         # Reproducibility script
│   └── ... (10 more scripts)
│
├── Figures (12 files)
│   ├── figures/accel_decel_summary_fs_20_tau_50.pdf
│   ├── figures/TE_accel_decel_boxplots_fs_20_tau_-1.pdf
│   ├── figures/boxplots_max_h_condition_foetus_fs_20.pdf
│   ├── figures/entropy_rate_ensemble_averaged_117_couples.pdf
│   ├── figures/cohort.pdf
│   └── ... (7 more figures)
│
└── Results (4 files)
    ├── mlm_accel_decel_results.csv             # MLM results
    ├── mlm_hmax_hmean_results.csv              # Entropy rate results
    ├── sample_entropy_mlm_results_simplified.csv
    └── sample_entropy_mlm_results_simplified.txt
```

**Total**: 37 files

---

## Study Design

### Cohort
- **N = 120** pregnant women in third trimester
  - 58 stressed group
  - 62 control group
- **Design**: Prospective cohort study
- **Measurements**: Maternal and fetal heart rate recordings

### Information-Theoretical Measures
- **Transfer Entropy (TE)**: Temporal information flow from maternal to fetal heart rate
- **Entropy Rate (ER)**: Intrinsic complexity of heart rate time series
- **Sample Entropy (SE)**: Regularity and predictability measures

### Conditioning Paradigms
- Full recording analysis
- Acceleration epochs (heart rate increases)
- Deceleration epochs (heart rate decreases)

### Statistical Analysis
- Mixed linear models with random intercepts (accounting for repeated measures)
- False Discovery Rate (FDR) correction for multiple comparisons
- Exploratory correlations with maternal cortisol and infant neurodevelopmental outcomes

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

**Note**: Raw data is not included in this repository. The scripts are provided for transparency and can be run with appropriately formatted data.

```bash
# Mixed Linear Model Analysis
python mixed_linear_model_analysis.py

# Correlation Analysis
python generate_correlation_heatmaps.py

# Sample Entropy Analysis
python sample_entropy_mlm_analysis_simplified.py

# Reproduce Manuscript Figures
python reproduce_manuscript_figures.py
```

### Expected Data Format

The analysis scripts expect data in the following format:
- CSV files with patient IDs, sex, stress group assignments
- Entropy measures (TE, ER, SE) for each conditioning paradigm
- Maternal cortisol and infant neurodevelopmental scores (for correlations)

---

## Key Results

### Coupling Strength
- Maternal heart rate decelerations → 60% coupling strength on fetal complexity
- Effect conserved across sex and stress groups
- Represents fundamental physiological coordination

### Transfer Entropy
- Sex-by-stress interaction (p < 0.05 in mixed linear models)
- Exploratory associations with maternal cortisol (not FDR-corrected)
- Requires independent replication

### Acceleration Predominance
- Universal pattern in maternal and fetal heart rates
- Stronger in fetal signals
- Independent of sex or stress status

### Methodological Insights
- Mixed linear models essential for repeated measures
- Initial t-test sex effects disappeared with proper statistical modeling
- Demonstrates importance of accounting for pseudoreplication

---

## Figures

All 12 publication figures included in `figures/`:

### Statistical Analysis
- Acceleration/deceleration summary statistics
- Fetal acceleration/deceleration point counts
- Maternal acceleration/deceleration point counts

### Transfer Entropy
- TE with acceleration/deceleration conditioning
- Sampling rate dependence analysis

### Entropy Rate
- ER conditioned on fetal state
- ER conditioned on maternal state
- Ensemble-averaged entropy rate

### Methods & Cohort
- Signal filtering methodology
- Study cohort description

---

## Citation

If you use this work, please cite the manuscript:

**arXiv**: [URL TBD - Coming Soon]

**Published Article**: [URL TBD - Coming Soon]

```bibtex
@article{felicity1_te_2025,
  title={Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester},
  author={[Authors]},
  journal={[Journal TBD]},
  year={2025},
  note={arXiv: [ID TBD]}
}
```

> **Note**: Citation information will be updated once the arXiv preprint and/or published article are available.

---

## Data Availability

**Raw patient data is excluded** from this repository to protect participant privacy.

**What's included**:
- ✅ All analysis code (Python scripts)
- ✅ Publication figures (PDF)
- ✅ Analysis results (CSV) for verification
- ✅ Software requirements and setup instructions

**Data sharing**: Anonymized data may be available upon reasonable request and appropriate ethics approval. Contact the corresponding author for inquiries.

---

## Reproducibility

This repository enables reproduction of:
1. **Statistical analyses** - All MLM, correlation, and entropy calculations
2. **Publication figures** - Scripts to regenerate all figures
3. **Result verification** - Result CSVs provided for comparison

To reproduce results with appropriate data:
1. Install dependencies: `pip install -r requirements.txt`
2. Format data according to expected structure (see Usage section)
3. Run analysis scripts in the provided order
4. Compare outputs with included result files

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For questions about this research:
- Corresponding author: [Contact information]
- Data requests: [Contact information]

---

## Keywords

Maternal-fetal coupling, transfer entropy, prenatal stress programming, fetal autonomic development, heart rate variability, bivariate phase-rectified signal averaging, mixed linear models, sex differences

---

**Repository Contents Summary**:
- 📊 16 Python analysis scripts
- 📈 12 publication figures (PDF)
- 📋 4 result files (CSV/TXT)
- 📄 1 README (this file)
- ⚖️ MIT License
- 📦 Python requirements

**Last Updated**: December 2025
