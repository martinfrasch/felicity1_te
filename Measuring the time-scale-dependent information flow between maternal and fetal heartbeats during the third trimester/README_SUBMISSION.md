# arXiv Submission Guide

**Manuscript**: Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester

**Status**: ✅ Ready for submission

---

## Quick Start

1. **Upload**: `arxiv_submission.zip` (or create new zip from this directory)
2. **Abstract**: Copy/paste from `abstract_arxiv.txt`
3. **Category**: q-bio.QM (Quantitative Methods)
4. **Verify**: Check compilation uses pdflatex

---

## Files in This Directory

### Required for arXiv

✅ **Main Manuscript**
- `main.tex` - Primary LaTeX file

✅ **Bibliography**
- `fetus.bib` - 1,182 references

✅ **Compilation Directive**
- `00README.XXX` - Forces pdflatex compilation (CRITICAL)

✅ **Template Files** (`Definitions/` directory)
- `mdpi.cls` - MDPI document class
- `mdpi.bst` - Bibliography style
- `journalnames.tex` - Journal abbreviations
- Logo files and support files

✅ **Figures** (15 total - all PDF/PNG)
- accel_decel_summary_fs_20_tau_50.pdf
- boxplots__h_condition_foetus_fs_20.pdf
- boxplots__h_condition_mother_fs_20.pdf
- boxplots_h_no_conditioning_fs_20.pdf
- cohort.pdf
- correlation_heatmaps_exploratory.png
- correlation_heatmaps_sex_stratified.png
- correlation_heatmaps_sex_stress_stratified.png
- entropy_rate_ensemble_averaged_117_couples.pdf
- filtering_example.pdf
- nb_pts_accel_decel_foetus_fs_20_tau_50.pdf
- nb_pts_accel_decel_mother_fs_20_tau_50.pdf
- TE_accel_decel_boxplots_fs_20_tau_-1.pdf
- TE_ensemble_averaged_vs_sampling_117_couples_zoom.pdf
- TE_no_conditioning_boxplots_fs_20_tau_-1.pdf

### Helper Files (Not Submitted)
- `abstract.txt` - Plain text abstract (original)
- `abstract_arxiv.txt` - arXiv-compliant abstract (use this)
- `main.pdf` - Compiled output (for reference)
- `main_final.pdf` - Previous version (for reference)

### Backup Files (Not Submitted)
- `main_original_backup.tex` - Original from Overleaf
- `main.tex.bak` - Automated backup

---

## Submission Steps

### 1. Create Archive (Optional)

If you need to recreate the submission zip:

```bash
cd "Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester"

zip -r arxiv_submission.zip \
  main.tex \
  fetus.bib \
  00README.XXX \
  Definitions/ \
  *.pdf \
  *.png \
  -x "main.pdf" -x "main_final.pdf" -x "*backup*" -x "*.bak"
```

### 2. Upload to arXiv

1. Go to: https://arxiv.org/submit
2. Login with your arXiv account
3. Start new submission
4. Upload: `arxiv_submission.zip` (or recreated archive)
5. Wait for arXiv to process files

### 3. Enter Metadata

**Title**:
```
Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester
```

**Abstract**: Copy from `abstract_arxiv.txt` (1,917 characters)
```
Prenatal maternal stress alters maternal-fetal heart rate coupling, as demonstrated by the Fetal Stress Index derived from bivariate phase-rectified signal averaging. Here, we extend this framework using information-theoretical measures to elucidate underlying mechanisms. In 120 third-trimester pregnancies (58 stressed, 62 control), we computed transfer entropy (TE), entropy rate (ER), and sample entropy (SE) under multiple conditioning paradigms, employing mixed linear models for repeated measures.
We identify dual coupling mechanisms at the short-term (0.5 - 2.5 s), but not long-term (2.5 - 5 s) time scales: (1) stress-invariant state-dependent synchronization, with maternal decelerations exerting approximately 60% coupling strength on fetal heart rate complexity--a fundamental coordination conserved across demographics; and (2) stress-sensitive temporal information transfer (TE), showing exploratory associations with maternal cortisol that require replication. A robust sex-by-stress interaction emerged in TE from mixed models, with exploratory female-specific coupling patterns absent in males. Universal acceleration predominance was observed in both maternal and fetal heart rates, stronger in fetuses and independent of sex or stress.
We provide insight into the dependence of these findings on the sampling rate of the underlying data, identifying 4 Hz, commonly used for ultrasound-derived fetal heart rate recordings, as the necessary and sufficient sampling rate regime to capture the information flow. Information-theoretical analysis reveals that maternal-fetal coupling operates through complementary pathways with differential stress sensitivity, extending the Fetal Stress Index by elucidating causal foundations. Future studies should explore additional information-theoretical conditional approaches to resolve stress-specific and time-scale-specific differences in information flow.
```

**Categories**:
- Primary: `q-bio.QM` (Quantitative Methods)
- Optional: `stat.AP` (Applications), `physics.bio-ph` (Biological Physics), `physics.med-ph` (Medical Physics)

### 4. Verify Compilation

After arXiv processes your submission:

1. Check compilation log shows:
   ```
   Processing with: pdflatex main.tex
   ```

2. Verify PDF preview:
   - 40 pages
   - All 15 figures appear correctly
   - Bibliography renders properly
   - No missing references or citations

3. Common issues:
   - ❌ If using xelatex: Check 00README.XXX is included
   - ❌ Missing figures: Verify all 15 PDF/PNG files uploaded
   - ❌ Bibliography errors: Check fetus.bib is included

### 5. Submit

- Review all metadata
- Confirm author list and affiliations
- Submit for moderation
- arXiv will email you when published

---

## Critical Technical Details

### Compilation Requirements

⚠️ **MUST use pdflatex, NOT xelatex**

The `00README.XXX` file forces pdflatex:
```
This submission requires pdflatex for compilation.

The main file is: main.tex

Please compile with: pdflatex main.tex

Do NOT use xelatex or lualatex.
```

**Why this matters**:
- arXiv defaults to xelatex without this file
- Unicode characters (×) cause errors with xelatex
- TikZ package (loaded by mdpi.cls) requires proper driver

### Character Encoding

All special characters replaced with LaTeX equivalents:

| Original | Replacement | Count |
|----------|-------------|-------|
| × (U+D7) | `$\times$` | 47 |
| — (em dash) | `--` (double hyphen) | 1 |

### Local Compilation Test

To verify everything works:

```bash
cd "Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester"

pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Expected output:
- ✅ `main.pdf` (7.8 MB, 40 pages)
- ✅ No critical errors
- ⚠️ Minor label warnings are normal

---

## Troubleshooting

### Error: Missing pgfsysdriver

**Cause**: arXiv using xelatex instead of pdflatex

**Fix**: Ensure `00README.XXX` is included in zip

### Error: Unicode character not set up

**Cause**: Unicode × or other special characters

**Fix**: All fixed in current version (47 replacements)

### Error: Missing figures

**Cause**: Figures not included in submission

**Fix**: Verify all 15 PDF/PNG files in zip

### Error: Bibliography not rendering

**Cause**: Missing fetus.bib or incorrect BibTeX processing

**Fix**:
1. Verify fetus.bib included
2. Check compilation log shows bibtex execution
3. Verify natbib package loaded (via mdpi.cls)

### Error: Cannot find Definitions/mdpi.cls

**Cause**: Directory structure not preserved in zip

**Fix**: Use `zip -r` to preserve directory structure

---

## Key Manuscript Changes for arXiv

### 1. 60% Coupling Strength Correction

**Previous (INCORRECT)**:
> "with maternal decelerations reducing fetal entropy by approximately 60%"

**Current (CORRECT)**:
> "with maternal decelerations exerting approximately 60% coupling strength on fetal heart rate complexity"

**Why**: 60% is a coupling strength ratio (β_decel / total β), NOT a percentage reduction

**Locations fixed**:
- Abstract (line 93)
- Results section (lines 541-549)

### 2. FDR Framework Consolidation

**Previous**: 15+ scattered disclaimers throughout results

**Current**: Single comprehensive framework (line 809):
> "All correlation analyses reported in this and subsequent sections (3.3.3-3.3.5) are exploratory. Of 144 correlation tests performed across all entropy features and outcomes, seven uncorrected associations (p < 0.05) were identified, matching the expected false positive rate of ~7.2 at α = 0.05... none survived FDR correction (all q-values > 0.40)."

### 3. Stress Sensitivity Cross-References

**Previous**: Repetitive explanations in multiple sections

**Current**: Forward references to detailed section:
> "This differential stress sensitivity between TE (stress-modulated) and conditioned entropy (stress-invariant) is explored in detail in Section 3.3.2."

**Locations**: Lines 575, 1174, 1190, 1212, 1279

---

## File Size Reference

| Component | Size |
|-----------|------|
| main.tex | ~200 KB |
| fetus.bib | 55 KB |
| Figures (total) | ~2.3 MB |
| Template files | ~500 KB |
| **Total archive** | **~9.6 MB** |
| Compiled PDF | 7.8 MB |

---

## Post-Submission

### arXiv Identifier

Once published, you'll receive an arXiv ID like: `arXiv:YYMM.NNNNN`

Example: `arXiv:2512.12345`

### DOI

arXiv will assign a DOI:
```
https://doi.org/10.48550/arXiv.YYMM.NNNNN
```

### Citation Format

```
@article{author2025maternal,
  title={Measuring the time-scale-dependent information flow between maternal and fetal heartbeats during the third trimester},
  author={[Author list]},
  journal={arXiv preprint arXiv:YYMM.NNNNN},
  year={2025}
}
```

### Next Steps

1. Share arXiv link with collaborators
2. Submit to journal (e.g., Entropy/MDPI)
3. Update preprint if revisions needed
4. Link arXiv version in journal submission

---

## Contact & Support

### arXiv Help
- Help page: https://arxiv.org/help
- Contact: https://arxiv.org/help/contact
- TeX support: https://arxiv.org/help/faq/texlive

### MDPI Support
- Template: https://www.mdpi.com/authors/latex
- Entropy: https://www.mdpi.com/journal/entropy

---

**Last Updated**: 2025-12-24
**Revision**: arXiv submission preparation complete
**Status**: ✅ Ready for upload
