# FELICITy1 Transfer Entropy Analysis

**Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester**

[![arXiv](https://img.shields.io/badge/arXiv-TBD-b31b1b.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📄 Manuscript Access

**arXiv Preprint**: [URL TBD - Coming Soon]

**Published Article**: [URL TBD - Coming Soon]

> **Note**: This repository contains analysis code and documentation. The full manuscript is available via the links above.

---

## Overview

This repository contains the complete research materials for an academic study analyzing maternal-fetal heart rate coupling using information-theoretical measures. The research examines how prenatal maternal stress affects physiological communication between mother and fetus through analysis of transfer entropy (TE), entropy rate (ER), and sample entropy (SE).

### Key Findings

- **Dual Coupling Mechanisms**: Identified stress-invariant state-dependent synchronization and stress-sensitive temporal information transfer
- **60% Coupling Strength**: Maternal heart rate decelerations exert approximately 60% coupling strength on fetal heart rate complexity
- **Sex-by-Stress Interaction**: Robust sex-by-stress interaction in transfer entropy from mixed linear models
- **Optimal Sampling**: 4 Hz identified as optimal sampling rate for information flow capture

## Project Structure

```
felicity1_te/
├── README.md                         # This file
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
│
├── figures/                          # Publication figures (15 total)
│   ├── accel_decel_summary_fs_20_tau_50.pdf
│   ├── TE_no_conditioning_boxplots_fs_20_tau_-1.pdf
│   ├── boxplots_h_no_conditioning_fs_20.pdf
│   └── [12 more figures]
│
├── analysis_scripts/                 # Statistical analysis code
│   ├── mixed_linear_model_analysis.py
│   ├── generate_correlation_heatmaps.py
│   ├── sample_entropy_mlm_analysis_simplified.py
│   └── statistical_analysis_v2.py
│
└── documentation/                    # Analysis summaries
    ├── COMPLETE_MLM_SUMMARY.md
    ├── CORRELATION_HEATMAPS_SUMMARY.md
    └── INTEGRATION_GUIDE_60_PERCENT_FINDING.md
```

## Abstract

Prenatal maternal stress alters maternal-fetal heart rate coupling, as demonstrated by the Fetal Stress Index derived from bivariate phase-rectified signal averaging. We extended this framework using information-theoretical measures to elucidate underlying mechanisms. In 120 third-trimester pregnancies (58 stressed, 62 control), we computed transfer entropy (TE), entropy rate (ER), and sample entropy (SE) under multiple conditioning paradigms, employing mixed linear models for repeated measures.

We identified dual coupling mechanisms: (1) stress-invariant state-dependent synchronization, with maternal decelerations exerting approximately 60% coupling strength—a fundamental coordination conserved across demographics; and (2) stress-sensitive temporal information transfer (TE), showing exploratory associations with maternal cortisol that require replication. A robust sex-by-stress interaction emerged in TE from mixed models, with exploratory female-specific coupling patterns absent in males.

Information-theoretical analysis reveals that maternal-fetal coupling operates through complementary pathways with differential stress sensitivity, extending the Fetal Stress Index by elucidating mechanistic foundations. Multiple entropy measures may improve stress assessment, with state-dependent coupling serving as a reference for pathological conditions.

## Methods

### Study Design
- **Cohort**: 120 pregnant women in third trimester
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

## Requirements

### Python Analysis Scripts
```bash
pip install -r requirements.txt
```

Required packages:
- numpy
- pandas
- scipy
- statsmodels
- matplotlib
- seaborn

## Usage

### Running Statistical Analysis

```bash
# Mixed Linear Model Analysis
python analysis_scripts/mixed_linear_model_analysis.py

# Correlation Heatmaps
python analysis_scripts/generate_correlation_heatmaps.py

# Sample Entropy Analysis
python analysis_scripts/sample_entropy_mlm_analysis_simplified.py
```

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

## Documentation

Comprehensive analysis documentation available in `/documentation`:

- **COMPLETE_MLM_SUMMARY.md**: Full mixed linear model results
- **CORRELATION_HEATMAPS_SUMMARY.md**: Exploratory correlation analysis
- **INTEGRATION_GUIDE_60_PERCENT_FINDING.md**: 60% coupling strength methodology
- **MLM_ANALYSIS_FINAL.md**: Final statistical analysis summary
- **SAMPLE_ENTROPY_MLM_SUMMARY.md**: Sample entropy analysis results

## Figures

All 15 publication-ready figures included:

### Statistical Analysis (3 figures)
- Acceleration/deceleration summary statistics
- Fetal point counts
- Maternal point counts

### Transfer Entropy (3 figures)
- TE without conditioning
- TE with accel/decel conditioning
- Sampling rate dependence

### Entropy Rate (4 figures)
- ER without conditioning
- ER conditioned on fetal state
- ER conditioned on maternal state
- Ensemble-averaged ER

### Correlation Heatmaps (3 figures)
- Exploratory correlations
- Sex-stratified correlations
- Sex and stress stratified

### Methods (2 figures)
- Signal filtering methodology
- Study cohort description

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Data Availability

**Note**: Raw patient data is excluded from this repository to protect participant privacy. Analysis scripts and statistical summaries are provided for transparency and reproducibility. Anonymized data may be available upon reasonable request and appropriate ethics approval.

## Contributing

This is a research manuscript repository. For questions or comments about the research, please contact the corresponding author.

## Acknowledgments

- FELICITy1 study participants
- Research team and collaborators
- Funding sources: [To be added]

## Contact

For questions about this research:
- Corresponding author: [Contact information]
- Study website: [If applicable]

## Version History

### 2025-12-24 - arXiv Submission
- Fixed 60% coupling strength terminology
- Unicode character fixes (× → $\times$)
- Created submission package
- Verified compilation

### 2025-12-24 - Manuscript Refinement
- Reduced redundancy (347 words)
- Consolidated FDR framework
- Added stress sensitivity cross-references

---

**Keywords**: Maternal-fetal coupling, transfer entropy, prenatal stress programming, fetal autonomic development, heart rate variability, bivariate phase-rectified signal averaging, mixed linear models, sex differences

---

## Repository Contents

This repository contains:
- ✅ Analysis code and scripts
- ✅ Publication figures
- ✅ Statistical results and summaries
- ✅ Documentation and methodology guides
- ❌ Manuscript files (see links above for manuscript access)
