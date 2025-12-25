# arXiv Submission Instructions

## Problem Fixed

**Original Error:**
```
Missing file: pgfsysdriver not found
Status: [FAILED] at step "first_run" with xelatex
```

**Root Cause:**
1. arXiv was trying to use xelatex instead of pdflatex
2. Unicode × character (U+D7) not compatible with pdflatex
3. Wrong main file being compiled

**Solutions Applied:**
1. ✅ Created `00README.XXX` to force pdflatex compilation
2. ✅ Replaced all Unicode × with LaTeX `$\times$`
3. ✅ Renamed `main_final.tex` → `main.tex` (arXiv default)
4. ✅ Verified successful compilation with pdflatex

---

## Files to Submit to arXiv

### From Directory:
`Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester/`

### Required Files:

**Main LaTeX File:**
- `main.tex` (the revised manuscript with all fixes)

**Bibliography:**
- `fetus.bib`

**Document Class & Style Files:**
- `Definitions/` directory (entire folder with all contents:)
  - `mdpi.cls`
  - `mdpi.bst`
  - All logo files and other support files

**Figure Files (all 11 figures):**
- `accel_decel_summary_fs_20_tau_50.pdf`
- `boxplots__h_condition_foetus_fs_20.pdf`
- `boxplots__h_condition_mother_fs_20.pdf`
- `boxplots_h_no_conditioning_fs_20.pdf`
- `cohort.pdf`
- `correlation_heatmaps_exploratory.png`
- `correlation_heatmaps_sex_stratified.png`
- `correlation_heatmaps_sex_stress_stratified.png`
- `entropy_rate_ensemble_averaged_117_couples.pdf`
- `filtering_example.pdf`
- `nb_pts_accel_decel_foetus_fs_20_tau_50.pdf`
- `nb_pts_accel_decel_mother_fs_20_tau_50.pdf`
- `TE_accel_decel_boxplots_fs_20_tau_-1.pdf`
- `TE_ensemble_averaged_vs_sampling_117_couples_zoom.pdf`
- `TE_no_conditioning_boxplots_fs_20_tau_-1.pdf`

**Compilation Instructions:**
- `00README.XXX` (forces pdflatex usage)

---

## arXiv Submission Steps

1. **Create a ZIP or TAR archive** containing:
   - main.tex
   - fetus.bib
   - Definitions/ folder with all contents
   - All 11 figure files
   - 00README.XXX

2. **Upload to arXiv:**
   - Go to arXiv.org submission page
   - Upload your archive
   - arXiv will automatically detect main.tex as the main file
   - The 00README.XXX will force pdflatex compilation

3. **Processing:**
   - arXiv will compile with: `pdflatex main.tex`
   - Bibliography will be processed with: `bibtex main`
   - Final PDF will be generated

---

## Verification

**Local Compilation Test:**
```bash
cd "Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester"
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

**Expected Output:**
- ✅ main.pdf (40 pages, ~7.8MB)
- ✅ No critical errors
- ⚠️ Minor warnings about labels are normal

---

## Changes Made for arXiv Compatibility

1. **Unicode Fix:** All × (multiplication) replaced with `$\times$`
2. **Compiler Directive:** Added 00README.XXX to force pdflatex
3. **Main File:** Renamed main_final.tex → main.tex
4. **Document Class:** Already has `pdftex` option (line 3)

---

## Backup Files Created

- `main_original_backup.tex` - Original main.tex from Overleaf
- `main.tex.bak` - Backup before Unicode replacement
- `main_final_ARXIV_READY.pdf` - Final compiled PDF (in parent directory)

---

## If arXiv Still Fails

Try these additional steps:

1. **Check file structure:** Make sure Definitions/ is at the same level as main.tex
2. **Verify figure paths:** All figures should be in the same directory as main.tex
3. **Remove graphics path:** Comment out `\graphicspath{{./figures/}}` if figures are in root
4. **Contact arXiv support:** Provide the compilation log

---

## Summary

✅ **Ready for arXiv submission**
✅ **All Unicode characters fixed**
✅ **Forced pdflatex compilation**
✅ **Verified local compilation**
✅ **All files identified**

Good luck with your submission!
