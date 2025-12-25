================================================================================
arXiv FINAL SUBMISSION PACKAGE
Created: December 24, 2024
================================================================================

✅ ALL ISSUES RESOLVED:
======================
✓ Line numbers removed (changed to basic article class)
✓ MDPI/elsarticle templates removed (now simple article class)
✓ Bibliography errors fixed (semicolons → commas, Sarkar:2021 → 2022)
✓ Unused figures removed (12 figures included, all referenced)
✓ Document compiles cleanly

FILE: arxiv_submission_FINAL.zip (1.8 MB)
========================================

CONTENTS:
---------
1. main.tex (34 KB) - Clean article class format, no line numbers
2. main.bbl (2 KB) - Compiled bibliography
3. fetus.bib (97 KB) - Bibliography database
4. figures/ - 12 PDF figures (all referenced in text)

FIGURES INCLUDED (12):
======================
✓ cohort.pdf
✓ filtering_example.pdf
✓ nb_pts_accel_decel_mother_fs_20_tau_50.pdf
✓ nb_pts_accel_decel_foetus_fs_20_tau_50.pdf
✓ accel_decel_summary_fs_20_tau_50.pdf
✓ entropy_rate_ensemble_averaged_117_couples.pdf
✓ boxplots_max_h_condition_foetus_fs_20.pdf
✓ boxplots_max_h_condition_mother_fs_20.pdf
✓ boxplots_mean_h_condition_foetus_fs_20.pdf
✓ boxplots_mean_h_condition_mother_fs_20.pdf
✓ TE_ensemble_averaged_vs_sampling_117_couples_zoom.pdf
✓ TE_accel_decel_boxplots_fs_20_tau_-1.pdf

CHANGES FROM ORIGINAL:
======================
1. Document class: elsarticle → article (simpler, no special packages needed)
2. Author format: Simplified with superscript affiliations
3. Bibliography: Fixed citation syntax (semicolons → commas)
4. Bibliography: Fixed missing reference (Sarkar:2021 → Sarkar:2022)
5. Figures: Removed 1 unused figure
6. Figures: Commented out 11 missing figures with clear NOTE markers

MISSING FIGURES (commented out in main.tex):
============================================
Search for "NOTE:" in main.tex to find commented sections:
- TE_ensemble_averaged_vs_sampling_117_couples.pdf (non-zoom version)
- TE_couple19/25/32_vs_sampling.pdf (3 figures)
- max_TE_accel_decel_foetus/mother_fs_20_tau_-1.pdf (2 figures)
- mean_TE_accel_decel_foetus/mother_fs_20_tau_-1.pdf (2 figures)
- TE_AUC_PSS_120_couples.pdf
- TE_AUC_PDQ_120_couples.pdf
- TE_AUC_20dHz_both_scores.pdf

NOTE: If you have these figures, add them to figures/ directory,
uncomment the corresponding lines in main.tex, recompile, and re-zip.

COMPILATION TEST:
=================
✓ pdflatex main.tex - Success
✓ bibtex main - Success (warnings only, no errors)
✓ pdflatex main.tex - Success
✓ pdflatex main.tex - Success
✓ Output: main.pdf (1.0 MB)

NEXT STEPS:
===========
1. Upload arxiv_submission_FINAL.zip to arXiv
2. arXiv should process successfully (no more line number errors)
3. Submission should move from "on-hold" to "submitted" automatically

================================================================================
