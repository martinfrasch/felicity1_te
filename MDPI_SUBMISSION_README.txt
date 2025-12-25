================================================================================
arXiv SUBMISSION - MDPI STYLE (LINE NUMBERS REMOVED)
Created: December 24, 2024
================================================================================

✅ LINE NUMBERS SUCCESSFULLY REMOVED
===================================

CHANGE MADE:
------------
File: main.tex (in MDPI subdirectory)
Line 3: Changed documentclass option from "submit" to "accept"

Before: \documentclass[bioengineering,article,submit,pdftex,moreauthors]{Definitions/mdpi}
After:  \documentclass[bioengineering,article,accept,pdftex,moreauthors]{Definitions/mdpi}

REASON:
-------
The MDPI template class (mdpi.cls) automatically enables line numbers when using
the "submit" option via the command: \ifthenelse{\equal{\@status}{submit}}{\linenumbers}{}

Changing to "accept" disables line numbers while maintaining all MDPI formatting.

FILE: arxiv_submission_mdpi_FINAL.zip (9.6 MB)
==============================================

LOCATION:
---------
Source directory: "Measuring the time-scale-dependent information flow between
                  maternal and fetal heartbeats during the third trimester/"
Zip file copied to: Root directory for easy access

CONTENTS:
---------
1. main.tex (115 KB) - MDPI template with "accept" option (no line numbers)
2. main.bbl (14 KB) - Compiled bibliography
3. fetus.bib (55 KB) - Bibliography database
4. 16 figure files (PDF and PNG):
   - cohort.pdf
   - filtering_example.pdf
   - entropy_rate_ensemble_averaged_117_couples.pdf
   - nb_pts_accel_decel_mother_fs_20_tau_50.pdf
   - nb_pts_accel_decel_foetus_fs_20_tau_50.pdf
   - accel_decel_summary_fs_20_tau_50.pdf
   - boxplots__h_condition_foetus_fs_20.pdf
   - boxplots__h_condition_mother_fs_20.pdf
   - boxplots_h_no_conditioning_fs_20.pdf
   - TE_ensemble_averaged_vs_sampling_117_couples_zoom.pdf
   - TE_accel_decel_boxplots_fs_20_tau_-1.pdf
   - TE_no_conditioning_boxplots_fs_20_tau_-1.pdf
   - correlation_heatmaps_exploratory.png
   - correlation_heatmaps_sex_stratified.png
   - correlation_heatmaps_sex_stress_stratified.png
5. Definitions/ directory - Complete MDPI template files (11 files)
   - mdpi.cls (main template class)
   - mdpi.bst (bibliography style)
   - journalnames.tex
   - logo files (PDF and EPS)
   - Other MDPI support files

COMPILATION STATUS:
===================
✓ pdflatex main.tex - SUCCESS (no errors)
✓ bibtex main - SUCCESS
✓ pdflatex main.tex - SUCCESS (final compilation)
✓ Output: main.pdf (40 pages, 8.1 MB)
✓ Line numbers: REMOVED ✅

Minor warnings only (not errors):
- Unicode character warnings (→ symbol in text) - cosmetic only
- Overfull hbox warnings - formatting within acceptable limits

VERIFICATION:
=============
Local compilation: ✓ SUCCESS
Line numbers: ✓ REMOVED (changed submit→accept)
MDPI formatting: ✓ PRESERVED
All figures: ✓ INCLUDED (16 figures)
Bibliography: ✓ COMPILED

CRITICAL NOTES:
===============
1. This uses the CORRECT manuscript file (MDPI version in subdirectory)
2. Previous work on root directory main.tex was INCORRECT (old version)
3. MDPI template formatting is fully preserved
4. Only change: Line numbers removed for arXiv compliance

NEXT STEPS:
===========
1. Upload arxiv_submission_mdpi_FINAL.zip to arXiv
2. arXiv should compile successfully (line numbers removed)
3. Submission should move from "on-hold" to "submitted" automatically

This submission maintains MDPI formatting while removing line numbers
as required by arXiv submission guidelines.

================================================================================
