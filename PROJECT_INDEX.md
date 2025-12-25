# FELICITy1 Transfer Entropy Paper - Project Index

**Title**: Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester

**Status**: ✅ Ready for arXiv submission

**Last Updated**: 2025-12-24

---

## 📋 Project Overview

Academic manuscript analyzing maternal-fetal heart rate coupling using information-theoretical measures (transfer entropy, entropy rate, sample entropy). Study of 120 third-trimester pregnancies examining stress-sensitive and stress-invariant coupling mechanisms.

### Key Findings
- Dual coupling mechanisms at short-term time scales (0.5-2.5s)
- 60% coupling strength: maternal decelerations on fetal heart rate complexity
- Sex-by-stress interaction in transfer entropy (TE)
- 4 Hz identified as optimal sampling rate for information flow capture

---

## 📁 Directory Structure

```
FELICITy1_TE_paper/
├── main.tex                                    # Main manuscript (ACTIVE - arXiv ready)
├── main_final.tex                              # Previous version (kept for reference)
├── fetus.bib                                   # Bibliography (1,182 entries)
├── references.bib                              # Alternative bibliography file
│
├── Measuring the time-scale.../                # arXiv Submission Directory ⭐
│   ├── main.tex                                # Submission-ready manuscript
│   ├── fetus.bib                               # Bibliography
│   ├── 00README.XXX                            # Compilation directive (pdflatex)
│   ├── abstract.txt                            # Plain text abstract (1,918 chars)
│   ├── abstract_arxiv.txt                      # arXiv-compliant abstract (1,917 chars)
│   ├── main.pdf                                # Compiled PDF (7.8 MB, 40 pages)
│   ├── Definitions/                            # MDPI template files
│   │   ├── mdpi.cls                            # Document class
│   │   ├── mdpi.bst                            # Bibliography style
│   │   └── journalnames.tex                    # Journal abbreviations
│   └── [15 figures - see Figures section]
│
├── Nicolas_felicity1/                          # Original analysis output
│   ├── output/MANUSCRIPT_SECTIONS.tex
│   └── SESSION_SUMMARY.md
│
├── analysis_output_corrected/                  # Statistical tables
│   └── publication_materials/
│       ├── Table1_Univariate_Complexity.tex
│       └── Table2_Transfer_Entropy.tex
│
└── claudedocs/                                 # Documentation (if exists)
```

---

## 📄 Main Files

### Manuscript Files

| File | Status | Purpose | Size |
|------|--------|---------|------|
| `main.tex` (root) | ⚠️ Older | Previous working version | - |
| `main_final.tex` | ⚠️ Reference | Pre-arXiv revision | - |
| `Measuring.../main.tex` | ✅ ACTIVE | arXiv submission manuscript | - |
| `main_original_backup.tex` | 📦 Backup | Original from Overleaf | - |
| `main_final_backup_20251224_110550.tex` | 📦 Backup | Pre-redundancy fix | - |

### Compiled Outputs

| File | Pages | Size | Notes |
|------|-------|------|-------|
| `main.pdf` (submission dir) | 40 | 7.8 MB | Final arXiv-ready PDF |
| `main_final.pdf` (submission dir) | 40 | 7.8 MB | Previous version |
| `information_flow_between...pdf` (root) | - | - | Earlier version |

### Bibliography

| File | Entries | Location | Status |
|------|---------|----------|--------|
| `fetus.bib` | 1,182 | Submission dir | ✅ Active |
| `references.bib` | - | Root | Alternative |

---

## 🖼️ Figures (15 total)

All figures located in submission directory. Required for arXiv submission.

### Statistical Analysis Figures
1. **accel_decel_summary_fs_20_tau_50.pdf** (100 KB)
   - Acceleration/deceleration summary statistics

2. **nb_pts_accel_decel_foetus_fs_20_tau_50.pdf** (100 KB)
   - Fetal acceleration/deceleration point counts

3. **nb_pts_accel_decel_mother_fs_20_tau_50.pdf** (104 KB)
   - Maternal acceleration/deceleration point counts

### Transfer Entropy Analysis
4. **TE_no_conditioning_boxplots_fs_20_tau_-1.pdf** (130 KB)
   - TE without conditioning

5. **TE_accel_decel_boxplots_fs_20_tau_-1.pdf** (142 KB)
   - TE with acceleration/deceleration conditioning

6. **TE_ensemble_averaged_vs_sampling_117_couples_zoom.pdf** (182 KB)
   - Sampling rate dependence analysis

### Entropy Rate Analysis
7. **boxplots_h_no_conditioning_fs_20.pdf** (132 KB)
   - Entropy rate without conditioning

8. **boxplots__h_condition_foetus_fs_20.pdf** (136 KB)
   - Entropy rate conditioned on fetal state

9. **boxplots__h_condition_mother_fs_20.pdf** (137 KB)
   - Entropy rate conditioned on maternal state

10. **entropy_rate_ensemble_averaged_117_couples.pdf** (149 KB)
    - Ensemble-averaged entropy rate

### Correlation Heatmaps
11. **correlation_heatmaps_exploratory.png**
    - Exploratory correlation analysis

12. **correlation_heatmaps_sex_stratified.png**
    - Sex-stratified correlations

13. **correlation_heatmaps_sex_stress_stratified.png**
    - Sex and stress stratified correlations

### Methods Illustrations
14. **filtering_example.pdf** (106 KB)
    - Signal filtering methodology

15. **cohort.pdf** (512 KB)
    - Study cohort description

---

## 📊 Documentation Files

### Analysis Summaries
- `COMPLETE_MLM_SUMMARY.md` - Comprehensive mixed linear model results
- `MLM_ANALYSIS_SUMMARY.md` - MLM analysis overview
- `MLM_ANALYSIS_FINAL.md` - Final MLM results
- `STATISTICAL_ANALYSIS_SUMMARY.md` - Statistical methods summary
- `SAMPLE_ENTROPY_MLM_SUMMARY.md` - Sample entropy MLM results

### Correlation Analysis
- `CORRELATION_HEATMAPS_SUMMARY.md` - Heatmap analysis summary
- `SEX_STRATIFIED_CORRELATION_SUMMARY.md` - Sex-stratified correlations

### Integration Guides
- `INTEGRATION_GUIDE_60_PERCENT_FINDING.md` - 60% coupling strength explanation
- `RESULTS_DISCUSSION_DECELERATION_COUPLING_FINAL.md` - Deceleration coupling results

### Session Logs
- `2025-12-18.md` - Session documentation
- `2025-12-19.md` - Session documentation
- `2025-12-23.md` - Session documentation
- `Nicolas_felicity1/SESSION_SUMMARY.md` - Analysis session summary

### Complete Documents
- `MANUSCRIPT_COMPLETE.md` - Complete manuscript in markdown

---

## 🚀 arXiv Submission Package

### Files Required
Located in: `Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester/`

✅ **Manuscript**
- `main.tex` - Main LaTeX file

✅ **Bibliography**
- `fetus.bib` - 1,182 references

✅ **Compilation Directive**
- `00README.XXX` - Forces pdflatex (prevents xelatex errors)

✅ **Template Files**
- `Definitions/mdpi.cls` - MDPI document class
- `Definitions/mdpi.bst` - MDPI bibliography style
- `Definitions/journalnames.tex` - Journal abbreviations
- `Definitions/` - All logo files and support files

✅ **Figures** (15 files)
- All PDF and PNG figures listed above

### Submission Archive
- **File**: `Measuring_the_time_scale_dependent_information_flow_between_maternal_and_fetal_heartbeats_during_the_third_trimester.zip`
- **Size**: ~9.6 MB
- **Contents**: 29 files (manuscript, bibliography, template, figures)

### Abstract (arXiv-compliant)
- **File**: `abstract_arxiv.txt`
- **Length**: 1,917 characters (under 1,920 limit)
- **Encoding**: ASCII-compliant (em dash → double hyphen)
- **Status**: ✅ Ready for copy/paste to arXiv

---

## 🔧 Technical Specifications

### LaTeX Compilation
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Document Class
- **Template**: MDPI (mdpi.cls)
- **Options**: `pdftex, article, submit, moreauthors, pdftex`
- **Journal**: Entropy
- **Type**: Article

### Key LaTeX Packages
- `tikz` - Graphics (via mdpi.cls)
- `amsmath, amssymb` - Mathematics
- `graphicx` - Figures
- `hyperref` - Cross-references
- `natbib` - Bibliography (author-year style)

### Statistics
- **Word count**: ~15,037 words (347 word reduction from original)
- **Pages**: 40
- **References**: 1,182 entries
- **Figures**: 15
- **Tables**: 2 (embedded in LaTeX)

---

## ✅ arXiv Submission Checklist

### Pre-Submission
- [x] Unicode characters fixed (× → $\times$, 47 replacements)
- [x] Compilation directive created (00README.XXX)
- [x] Main file renamed (main_final.tex → main.tex)
- [x] Local compilation verified (pdflatex)
- [x] Abstract character count verified (1,917 < 1,920)
- [x] Abstract ASCII-compliant (em dash removed)
- [x] All figures present (15/15)
- [x] Bibliography complete (fetus.bib)

### Critical Fixes Applied
1. **60% coupling strength correction** (lines 93, 541-549)
   - Changed: "reducing fetal entropy by approximately 60%"
   - To: "exerting approximately 60% coupling strength"

2. **FDR framework consolidation** (line 809)
   - Single comprehensive interpretive framework
   - Replaces 15+ scattered disclaimers

3. **Stress sensitivity cross-references** (lines 575, 1174, 1190, 1212, 1279)
   - Forward references instead of repetition

4. **Unicode encoding fix**
   - All × replaced with $\times$ (47 instances)
   - Prevents xelatex Unicode errors

### Submission Steps
1. Upload `Measuring_the_time_scale...zip` to arXiv
2. Copy/paste `abstract_arxiv.txt` into abstract field
3. Select category: q-bio.QM (Quantitative Methods) or physics.bio-ph
4. Add optional categories: stat.AP, physics.med-ph
5. Verify compilation log shows pdflatex usage
6. Check PDF preview matches local compilation

---

## 🔍 Key Manuscript Sections

### Abstract (Lines 89-98)
- 3 paragraphs
- 1,917 characters (arXiv-compliant)
- Key finding: dual coupling mechanisms with 60% coupling strength

### Introduction (Lines ~100-300)
- Background on maternal-fetal coupling
- Information-theoretical framework
- Study objectives

### Methods (Lines ~300-600)
- Cohort: 120 pregnancies (58 stressed, 62 control)
- Transfer entropy calculation
- Entropy rate and sample entropy
- Mixed linear models (MLM)
- Statistical analysis (FDR correction)

### Results (Lines ~600-1100)
- 60% coupling strength finding (maternal decel → fetal complexity)
- Sex-by-stress interaction in TE
- Acceleration predominance (maternal and fetal)
- Sampling rate dependence (4 Hz optimal)

### Discussion (Lines ~1100-1400)
- Dual coupling mechanisms interpretation
- Stress sensitivity differences (TE vs entropy)
- Clinical implications
- Limitations and future directions

### Supplementary Materials
- Box: 60% coupling strength calculation methodology
- Additional statistical details

---

## 📝 Version History

### 2025-12-24 - arXiv Submission Preparation
- **Fixed**: 60% coupling strength wording (abstract + results)
- **Fixed**: Unicode × → $\times$ (47 replacements)
- **Created**: 00README.XXX (pdflatex directive)
- **Renamed**: main_final.tex → main.tex
- **Created**: abstract_arxiv.txt (ASCII-compliant)
- **Created**: arxiv_submission.zip (29 files, 9.6 MB)
- **Verified**: Local compilation successful
- **Status**: ✅ Ready for arXiv submission

### 2025-12-24 - Redundancy Reduction
- **Reduced**: 347 words (15,384 → 15,037)
- **Consolidated**: FDR framework (15+ instances → 1)
- **Added**: Cross-references for stress sensitivity
- **Preserved**: Scientific accuracy and completeness
- **Status**: Completed, compiled successfully

### Earlier Versions
- Multiple analysis iterations documented in session logs
- Statistical analysis refinements in MLM summaries
- Correlation analysis explorations in heatmap summaries

---

## 🎯 Key Contacts & Resources

### Journal Information
- **Target**: arXiv preprint
- **Future submission**: Entropy (MDPI)
- **Article type**: Research Article
- **Subject area**: Bioinformatics, Information Theory, Perinatal Medicine

### arXiv Resources
- **Submission portal**: https://arxiv.org/submit
- **Help**: https://arxiv.org/help
- **TeX support**: https://arxiv.org/help/faq/texlive
- **Category browser**: https://arxiv.org

### Technical Support
- **MDPI template**: https://www.mdpi.com/authors/latex
- **Entropy journal**: https://www.mdpi.com/journal/entropy

---

## 📌 Important Notes

### Compilation Requirements
⚠️ **CRITICAL**: Must use **pdflatex**, NOT xelatex or lualatex
- arXiv defaults to xelatex without 00README.XXX
- Unicode characters (×) cause errors with xelatex
- TikZ package requires proper driver selection

### Character Encoding
- All text must be ASCII-compliant for arXiv
- Em dashes (—) replaced with double hyphens (--)
- Unicode multiplication (×) replaced with LaTeX $\times$

### 60% Coupling Strength
⚠️ **CRITICAL TERMINOLOGY**:
- NOT "60% reduction in fetal entropy"
- CORRECT: "60% coupling strength"
- Represents: β ratio = |β_decel| / (|β_decel| + |β_no_cond|)
- Mathematical basis: See Supplementary Box for detailed methodology

### FDR Correction
- 144 correlation tests performed
- 7 nominal p < 0.05 (expected ~7.2 false positives)
- **NONE survived FDR correction** (all q > 0.40)
- Exploratory findings require independent replication

---

## 🔗 Cross-References

### Related Documentation
- See `ARXIV_SUBMISSION_INSTRUCTIONS.md` for detailed submission guide
- See `INTEGRATION_GUIDE_60_PERCENT_FINDING.md` for coupling strength explanation
- See `COMPLETE_MLM_SUMMARY.md` for statistical analysis details

### Backup Files
- `main_original_backup.tex` - Original Overleaf version
- `main_final_backup_20251224_110550.tex` - Pre-edit backup
- `main.tex.bak` - Automated backup from sed Unicode fix

### Archive Files
- Root directory contains earlier PDF versions
- `Nicolas_felicity1/` contains original analysis output
- Session documentation provides revision history

---

## 📊 Project Statistics

- **Total files**: ~50+ (including figures, documentation, backups)
- **LaTeX files**: 9
- **PDF outputs**: 18 (figures + manuscripts)
- **Documentation**: 15+ markdown files
- **Submission package**: 29 files, 9.6 MB
- **Project duration**: Multi-session (Dec 18-24, 2025)
- **Final manuscript**: 40 pages, 15,037 words, 1,182 references

---

**Generated**: 2025-12-24
**Tool**: Claude Code `/sc:index`
**Purpose**: Comprehensive project documentation for arXiv submission workflow
